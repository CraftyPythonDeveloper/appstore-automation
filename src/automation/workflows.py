from automation.base_driver import BaseDriver
from automation.pages.amazon_homepage import AmazonHomePage
from automation.pages.amazon_signup_page import AmazonSignupPage
from automation.pages.amazon_profile_page import AmazonProfilePage
from integrations.virtual_number_service import OnlineSimService
from utils.logger import logger
from utils.utils import get_fake_name, get_fake_password


class AmazonAccountCreationWorkflow(BaseDriver):
    def __init__(self, name: str = None, password: str = None, phone_number: str = None, country: str = None):
        super().__init__()
        self.name = name
        self.password = password
        self.phone_number = phone_number
        self.totp_secret = None
        self.country = country or "canada"
        self.driver = self.get_driver(enable_captcha_solver=True, enable_proxy=True)

    def run(self):
        online_sim = OnlineSimService()
        tzid = online_sim.get_new_number()      # default number will be from canada
        self.phone_number = online_sim.get_number(tzid=tzid)
        self.name = get_fake_name()
        self.password = get_fake_password()
        logger.info(f"Generated new phone number: {self.phone_number}")

        home_page = AmazonHomePage(driver=self.driver)
        home_page.load_page()
        signup_url = home_page.get_signup_url()

        signup_page = AmazonSignupPage(driver=self.driver, signup_url=signup_url)
        signup_page.load_page()
        signup_page.fill_signup_form(
            name=self.name, phone_number=self.phone_number, password=self.password, country_name=self.country
        )

        # let Nopecha solve the captcha
        self.random_sleep(15, 20)

        if signup_page.does_account_already_exists():
            # self.quit_driver()
            return

        otp = None

        # try 3 times to get otp
        logger.info(f"Waiting for otp to arrive from amazon")
        for retry in range(3):
            otp = online_sim.get_message_with_wait(tzid=tzid)
            if otp is not None:
                break

            logger.info(f"Retrying again: retry count: {retry}")
            self.random_sleep()
            signup_page.resend_otp()

        if otp is None:
            logger.info("Did not receive otp after retrying 3 times, skipping this automation")
            return

        signup_page.enter_otp(code=otp)

        amazon_profile = AmazonProfilePage(self.driver, self.password)
        amazon_profile.get_accounts_page()
        amazon_profile.get_login_security()
        self.totp_secret = amazon_profile.setup_mfa()
        return self.name, self.phone_number, self.password, self.totp_secret

    def cleanup(self):
        self.quit_driver()
