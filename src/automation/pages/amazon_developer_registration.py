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
    SAME_EMAIL_CHECKBOX = "//p[text()='Same as primary email address']"
    PHONE_NUMBER = "#company_phone"
    PHONE_COUNTRY = "#phonemenu"
    SUBMIT_BTN = "#registrationSubmit"


class AmazonDevRegistrationPage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.faker = Faker("en_US")  # for canada specific fake info
        super().__init__()

    # def enter_first_name(self, first_name):
    #     self.random_sleep()
    #     logger.info(f"Entering first name: {first_name}")
    #     self.driver.type(AmazonDevRegistrationPageLocators.FIRST_NAME, first_name)
    #     logger.info(f"Entered first name: {first_name}")
    #
    # def enter_last_name(self, last_name):
    #     self.random_sleep()
    #     logger.info(f"Entering last name: {last_name}")
    #     self.driver.type(AmazonDevRegistrationPageLocators.LAST_NAME, last_name)
    #     logger.info(f"Entered last name: {last_name}")

    def generate_address(self):
        pattern = r'^(?P<address_line1>.+)\n(?P<city>.+), (?P<state>[A-Z]{2}) (?P<postal_code>\d{5})$'
        for i in range(30):
            match = re.match(pattern, faker.address())
            if match:
                return match.groupdict()

    def enter_country_code(self, country_code):
        self.random_sleep()
        logger.info(f"Entering country: {country_code}")
        self.driver.click("#country_code")
        self.random_sleep()
        self.driver.click("//div[text()='United States']")
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
        self.driver.click("#state")
        try:
            self.driver.click(f"//div[text()='{state}']")
            return state
        except:
            self.driver.click(f"//div[text()='Arizona']")
            return "Arizona"

    def enter_zip_code(self, zip_code):
        self.random_sleep()
        logger.info(f"Entering zip code: {zip_code}")
        self.driver.type(AmazonDevRegistrationPageLocators.ZIP_CODE, zip_code)
        logger.info(f"Entered zip code: {zip_code}")

    def primary_email_check(self):
        self.driver.click(AmazonDevRegistrationPageLocators.SAME_EMAIL_CHECKBOX)

    def enter_phone(self, phone):
        self.random_sleep()
        logger.info(f"Entering phone number: {phone}")
        self.driver.click(AmazonDevRegistrationPageLocators.PHONE_COUNTRY)
        self.driver.click("//div[text()='US (+1)']")
        self.driver.type(AmazonDevRegistrationPageLocators.PHONE_NUMBER, phone)
        logger.info(f"Entered phone number: {phone}")

    def submit_registration(self):
        self.random_sleep()
        logger.info(f"Clicking Submit button")
        self.driver.click(AmazonDevRegistrationPageLocators.SUBMIT_BTN)
        logger.info(f"Clicked Submit button")

    def skip_verification():
        self.driver.click("#Ivv_later_btn")

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
        address = self.generate_address()
        logger.info(f"Filling the Registration form")
        # self.enter_first_name(first_name or self.faker.first_name())
        # self.enter_last_name(last_name or self.faker.last_name())
        self.enter_country_code(country or self.faker.country_code())
        self.enter_business_name(business_name or self.faker.company())
        self.enter_address_line1(address_line1 or address["address_line1"])
        self.enter_city(city or address["city"])
        state = self.enter_state(state or address["state"])
        if state == "Arizona":
            address["postal_code"] = "85010"
        self.enter_zip_code(zip_code or address["postal_code"])
        self.enter_phone(phone or self.faker.msisdn()[3:])
        self.primary_email_check()
        self.submit_registration()
        self.random_sleep()
        self.skip_verification()
