from automation.base_driver import BaseDriver
from automation.pages.amazon_homepage import AmazonHomePage
from automation.pages.amazon_signup_page import AmazonSignupPage
from automation.pages.amazon_profile_page import AmazonProfilePage
from automation.pages.amazon_developer_registration import AmazonDevRegistrationPage
from integrations.virtual_number_service import OnlineSimService
from integrations.tempmail_service import TempMailService
from utils.logger import logger
from utils.utils import get_fake_name, get_fake_password


class AmazonAccountCreationWorkflow(BaseDriver):
    def __init__(self, name: str = None, email:str = None, password: str = None, phone_number: str = None, country: str = None):
        super().__init__()
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.totp_secret = None
        self.country = country or "canada"
        self.driver = self.get_driver(enable_captcha_solver=True, enable_proxy=True)

    def run(self):
        temp_mail_service = TempMailService()
        self.email = temp_mail_service.get_new_email_id()

        self.name = get_fake_name()
        self.password = get_fake_password()

        home_page = AmazonHomePage(driver=self.driver)
        home_page.load_page()
        home_page.get_signup_page()

        signup_page = AmazonSignupPage(driver=self.driver)
        signup_page.fill_signup_form(
            name=self.name, email=self.email, phone_number=self.phone_number, password=self.password,
            country_name=self.country
        )

        # let Nopecha solve the captcha
        self.random_sleep(15, 20)

        otp = None

        # try 3 times to get otp
        logger.info(f"Waiting for email otp to arrive from amazon")
        for retry in range(3):
            otp = temp_mail_service.get_amazon_message()
            # otp = online_sim.get_message_with_wait(tzid=tzid)
            if otp is not None:
                break

            logger.info(f"No OTP in email, Retrying again: retry count: {retry}")
            self.random_sleep()
            signup_page.resend_otp()

        if otp is None:
            logger.info("Did not receive email otp after retrying 3 times, skipping this automation")
            return

        signup_page.enter_otp(code=otp)

        # phone verification logic
        online_sim = OnlineSimService()
        tzid = online_sim.get_new_number()  # default number will be from canada
        self.phone_number = online_sim.get_number(tzid=tzid)

        signup_page.enter_mobile_number(country_name=self.country, phone_number=self.phone_number)
        signup_page.submit_phone_number()

        logger.info(f"Waiting for phone otp to arrive from amazon")
        for retry in range(3):
            otp = online_sim.get_message_with_wait(tzid=tzid)
            if otp is not None:
                break

            logger.info(f"No OTP in phone, Retrying again: retry count: {retry}")
            self.random_sleep()
            signup_page.resend_otp()

        if otp is None:
            logger.info("Did not receive email otp after retrying 3 times, skipping this automation")
            return

        signup_page.enter_otp(code=otp)
        self.random_sleep()
        signup_page.submit_form()

        if signup_page.does_account_already_exists():
            # self.quit_driver()
            return

        developer_page = AmazonDevRegistrationPage(self.driver)
        developer_page.fill_registration_form(phone=self.phone_number)

        amazon_profile = AmazonProfilePage(self.driver, self.password)
        amazon_profile.get_accounts_page()
        amazon_profile.get_login_security()
        self.totp_secret = amazon_profile.setup_mfa()
        return self.name, self.phone_number, self.password, self.totp_secret

    def cleanup(self):
        self.quit_driver()
