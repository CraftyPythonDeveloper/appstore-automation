from faker import Faker
from utils.logger import logger
from automation.pages.base_page import BasePage


class AmazonDevRegistrationPageLocators:
    FIRST_NAME = "#first_name"
    LAST_NAME = "#last_name"
    COUNTRY = "#country_code"
    BUSINESS_NAME = "#company_name"
    ADDRESS_LINE1 = "#address_line"
    CITY = "#city"
    STATE = "#state"
    ZIP_CODE = "#postal_code"
    SAME_EMAIL_CHECKBOX = "#ckbx_company_sup_email"
    PHONE_NUMBER = "#company_phone"
    CONTINUE_BTN = "#phonemenu"


class AmazonDevRegistrationPage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.faker = Faker("en_CA")     # for canada specific fake info
        super().__init__()

    def enter_first_name(self, first_name):
        self.random_sleep()
        logger.info(f"Entering first name: {first_name}")
        self.driver.type(AmazonDevRegistrationPageLocators.FIRST_NAME, first_name)
        logger.info(f"Entered first name: {first_name}")

    def enter_last_name(self, last_name):
        self.random_sleep()
        logger.info(f"Entering last name: {last_name}")
        self.driver.type(AmazonDevRegistrationPageLocators.LAST_NAME, last_name)
        logger.info(f"Entered last name: {last_name}")

    def enter_country_code(self, country_code):
        self.random_sleep()
        logger.info(f"Entering country: {country_code}")
        self.driver.type(AmazonDevRegistrationPageLocators.COUNTRY, country_code)
        logger.info(f"Entered country: {country_code}")

    def enter_business_name(self, business_name):
        self.random_sleep()
        logger.info(f"Entering business name: {business_name}")
        self.driver.type(AmazonDevRegistrationPageLocators.BUSINESS_NAME, business_name)
        logger.info(f"Entered business name: {business_name}")

    def enter_address_line1(self, address_line1):
        self.random_sleep()
        logger.info(f"Entering address line1: {address_line1}")
        self.driver.type(AmazonDevRegistrationPageLocators.ADDRESS_LINE1, address_line1)
        logger.info(f"Entered address line1: {address_line1}")

    def enter_city(self, city):
        self.random_sleep()
        logger.info(f"Entering city: {city}")
        self.driver.type(AmazonDevRegistrationPageLocators.CITY, city)
        logger.info(f"Entered city: {city}")

    def enter_state(self, state):
        self.random_sleep()
        logger.info(f"Entering state: {state}")
        self.driver.type(AmazonDevRegistrationPageLocators.STATE, state)
        logger.info(f"Entered state: {state}")

    def enter_zip_code(self, zip_code):
        self.random_sleep()
        logger.info(f"Entering zip code: {zip_code}")
        self.driver.type(AmazonDevRegistrationPageLocators.ZIP_CODE, zip_code)
        logger.info(f"Entered zip code: {zip_code}")

    def primary_email_check(self):
        pass

    def enter_phone(self, phone):
        self.random_sleep()
        logger.info(f"Entering phone number: {phone}")
        self.driver.type(AmazonDevRegistrationPageLocators.ZIP_CODE, phone)
        logger.info(f"Entered phone number: {phone}")

    def submit_registration(self):
        self.random_sleep()
        logger.info(f"Clicking Submit button")
        self.driver.click(AmazonDevRegistrationPageLocators.CONTINUE_BTN)
        logger.info(f"Clicked Submit button")

    def fill_registration_form(
            self,
            first_name: str = None,
            last_name: str = None,
            country: str = None,
            business_name: str = None,
            address_line1: str = None,
            city: str = None,
            state: str = None,
            zip_code: str = None,
            phone: str = None
    ):
        logger.info(f"Filling the Registration form")
        self.enter_first_name(first_name or self.faker.first_name())
        self.enter_last_name(last_name or self.faker.last_name())
        self.enter_country_code(country or self.faker.country_code())
        self.enter_business_name(business_name or self.faker.company())
        self.enter_address_line1(address_line1 or self.faker.street_address())
        self.enter_city(city or self.faker.city())
        self.enter_state(state or self.faker.province())
        self.enter_zip_code(zip_code or self.faker.postalcode())
        self.enter_phone(phone or self.faker.phone_number().replace(".", ""))
