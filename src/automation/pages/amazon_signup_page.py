from selenium.webdriver.common.by import By

from utils.logger import logger
from automation.pages.base_page import BasePage


class AmazonSignupPageLocators:
    USERNAME_INPUT = "#ap_customer_name"
    PASSWORD_INPUT = "#ap_password"
    PASSWORD_CHECK_INPUT = "#ap_password_check"
    PHONE_NUMBER_INPUT = "#ap_email"
    SUBMIT_BUTTON = "#continue"
    VERIFICATION_CODE_INPUT = "#cvf-input-code"
    SUBMIT_VERIFICATION = "//input[@aria-label='Verify OTP Button']"
    RESEND_VERIFICATION = "cvf-resend-link"
    EXISTING_ACCOUNT_MSG = "//h4[text()='Mobile number already in use']"


class AmazonSignupPage(BasePage):
    def __init__(self, driver, signup_url):
        self.driver = driver
        self.signup_url = signup_url
        super().__init__()

    def load_page(self):
        self.random_sleep()
        logger.debug("Loading amazon signup page")
        self.driver.get(self.signup_url)
        logger.debug("Amazon signup page loaded successfully")

    def enter_name(self, username):
        self.random_sleep()
        logger.debug(f"Typing username {username}")
        self.driver.type(AmazonSignupPageLocators.USERNAME_INPUT, username)
        logger.debug(f"Done entering username {username}")

    def enter_mobile_number(self, country_name, phone_number):
        self.random_sleep()
        logger.debug(f"Typing mobile number {phone_number}")
        self.driver.type(AmazonSignupPageLocators.PHONE_NUMBER_INPUT, phone_number)
        self.random_sleep()
        logger.debug(f"Done entering mobile number {phone_number}, selecting country {country_name}")
        self.driver.find_element(By.XPATH, "//div[@class='a-section country-picker']").click()
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
        self.driver.type(AmazonSignupPageLocators.PASSWORD_INPUT, password)
        self.random_sleep()
        self.driver.type(AmazonSignupPageLocators.PASSWORD_CHECK_INPUT, password)
        logger.debug(f"Done entering password {password}")

    def submit_form(self):
        self.random_sleep()
        self.driver.click(AmazonSignupPageLocators.SUBMIT_BUTTON)

    def fill_signup_form(self, name, password, phone_number, country_name):
        logger.info(f"Filling signup form")
        self.enter_name(username=name)
        self.enter_mobile_number(country_name=country_name, phone_number=phone_number)
        self.enter_password(password=password)
        self.submit_form()
        logger.info(f"Done filling signup form")

    def enter_otp(self, code):
        self.random_sleep()
        logger.info(f"Entering verification code")
        self.driver.type(AmazonSignupPageLocators.VERIFICATION_CODE_INPUT, code)
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
