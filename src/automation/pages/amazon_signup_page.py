from selenium.webdriver.common.by import By

from utils.logger import logger
from automation.pages.base_page import BasePage


class AmazonSignupPageLocators:
    NEW_ACCOUNT_BTN = "#createAccountSubmit"
    EMAIL_INPUT = "#ap_email"
    USERNAME_INPUT = "#ap_customer_name"
    PASSWORD_INPUT = "#ap_password"
    PASSWORD_CHECK_INPUT = "#ap_password_check"
    PHONE_NUMBER_INPUT = "#cvfPhoneNumber"
    COUNTRY_DROPDOWN = "//span[@class='a-button-text a-declarative']"
    SUBMIT_BUTTON = "#continue"
    VERIFICATION_CODE_INPUT = "#cvf-input-code"
    SUBMIT_VERIFICATION = "//input[@aria-label='Verify OTP Button']"
    RESEND_VERIFICATION = "cvf-resend-link"
    EXISTING_ACCOUNT_MSG = "//h4[text()='Mobile number already in use']"
    SUBMIT_PHONE_NUMBER = "//input[@type='submit']"


class AmazonSignupPage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        super().__init__()
    #
    # def load_page(self):
    #     self.random_sleep()
    #     logger.debug("Loading amazon signup page")
    #     self.driver.get(self.signup_url)
    #     logger.debug("Amazon signup page loaded successfully")

    def enter_email(self, email):
        """
        step 1
        :param email:
        :return:
        """
        self.random_sleep()
        logger.debug(f"Typing email {email}")
        self.start_typing(AmazonSignupPageLocators.EMAIL_INPUT, email)
        logger.debug(f"Done typing email {email}")

    def enter_name(self, username):
        self.random_sleep()
        logger.debug(f"Typing username {username}")
        self.start_typing(AmazonSignupPageLocators.USERNAME_INPUT, username)
        logger.debug(f"Done entering username {username}")

    def enter_mobile_number(self, country_name, phone_number):
        self.random_sleep()
        logger.debug(f"Typing mobile number {phone_number}")
        self.start_typing(AmazonSignupPageLocators.PHONE_NUMBER_INPUT, phone_number)
        self.random_sleep()
        logger.debug(f"Done entering mobile number {phone_number}, selecting country {country_name}")
        self.driver.find_element(By.XPATH, AmazonSignupPageLocators.COUNTRY_DROPDOWN).click()
        self.random_sleep()
        country_dropdown = self.driver.find_elements(By.TAG_NAME, "a")
        for element in country_dropdown:
            if element.text and country_name.lower() in element.text.lower():
                element.click()
                logger.debug(f"Selected country {country_name} from phone dropdown")
                break

        logger.debug(f"Done entering mobile number {phone_number}")

    def enter_password(self, password):
        self.random_sleep()
        logger.debug(f"Typing password {password}")
        self.start_typing(AmazonSignupPageLocators.PASSWORD_INPUT, password)
        self.random_sleep()
        self.start_typing(AmazonSignupPageLocators.PASSWORD_CHECK_INPUT, password)
        logger.debug(f"Done entering password {password}")

    def submit_form(self):
        self.random_sleep()
        self.driver.click(AmazonSignupPageLocators.SUBMIT_BUTTON)

    def submit_phone_number(self):
        self.random_sleep()
        self.driver.click(AmazonSignupPageLocators.SUBMIT_PHONE_NUMBER, "xpath")
        self.random_sleep()

    def fill_signup_form(self, name, email, password, phone_number, country_name):
        logger.info(f"Filling signup form, {name}, {email}, {password}, {phone_number}, {country_name}")
        self.enter_name(username=name)
        self.enter_email(email=email)
        # self.enter_mobile_number(country_name=country_name, phone_number=phone_number)
        self.enter_password(password=password)
        self.submit_form()
        try:

            existing_account = self.driver.find_element(By.XPATH, '//div[contains(text(), " but an account already exists with the email address")]')
        except:
            existing_account = None

        if existing_account:
            logger.info(f"Account already exists with the email address {email}")
            self.signin(email=email, password=password)

        logger.info(f"Done filling signup form")

    def signin(self, email, password):
        self.driver.click('//a[contains(text(), "Sign in")]')
        self.enter_email(email=email)
        self.submit_form()
        self.enter_password(password=password)
        self.driver.click("#signInSubmit")


    def enter_otp(self, code):
        self.random_sleep()
        logger.info(f"Entering verification code")
        self.start_typing(AmazonSignupPageLocators.VERIFICATION_CODE_INPUT, code)
        self.random_sleep()
        self.driver.find_element(By.XPATH, AmazonSignupPageLocators.SUBMIT_VERIFICATION).click()
        logger.info(f"Submitted verification code")

    def resend_otp(self):
        self.random_sleep()
        self.driver.find_element(By.ID, AmazonSignupPageLocators.RESEND_VERIFICATION).click()
        logger.info(f"Resent verification code")

    def does_account_already_exists(self):
        self.random_sleep()
        try:
            self.driver.find_element(By.XPATH, AmazonSignupPageLocators.EXISTING_ACCOUNT_MSG)
            logger.info(f"Account is already registered!")
            return True
        except:
            return False

#
# class AmazonSellerSignup(AmazonSignupPage):
