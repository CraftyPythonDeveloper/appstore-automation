from automation.base_driver import BaseDriver
from automation.pages.amazon_homepage import AmazonHomePage
from automation.pages.amazon_signup_page import AmazonSignupPage
from integrations.virtual_number_service import OnlineSimService
from utils.logger import logger


class AmazonAccountCreationWorkflow(BaseDriver):
    def __init__(self, name, password, country):
        super().__init__()
        self.name = name
        self.password = password
        self.country = country
        self.driver = self.get_driver(enable_captcha_solver=True, enable_proxy=True)

    def run(self):
        online_sim = OnlineSimService()
        tzid = online_sim.get_new_number()      # default number will be from canada
        phone_number = online_sim.get_number(tzid=tzid)
        logger.info(f"Generated new phone number: {phone_number}")

        home_page = AmazonHomePage(driver=self.driver)
        home_page.load_page()
        signup_url = home_page.get_signup_url()

        signup_page = AmazonSignupPage(driver=self.driver, signup_url=signup_url)
        signup_page.load_page()
        signup_page.fill_signup_form(
            name=self.name, phone_number=phone_number, password=self.password, country_name=self.country
        )
        # let Nopecha solve the captcha
        self.random_sleep(15, 20)
        otp = None

        # try 3 times to get otp
        for retry in range(3):
            for i in range(20):     # check every second until 20 second
                otp = online_sim.get_message(tzid=tzid)

                if otp is not None:
                    logger.debug("Received OTP: {}".format(otp))
                    break

                self.random_sleep(1, 1)

            logger.info(f"Did not receive otp in 20 seconds, retrying again: retry count: {retry}")
            self.random_sleep()
            signup_page.resend_otp()

        if otp is None:
            logger.info("Did not receive otp after retrying 3 times, skipping this automation")

        signup_page.enter_otp(code=otp)

        print("***** Stop!")
