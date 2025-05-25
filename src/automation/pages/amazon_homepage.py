from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from utils.logger import logger
from automation.pages.base_page import BasePage
from integrations.captcha_service import solve_text_captcha


class AmazonHomePageSelectors:
    START_HERE = "//a[@aria-label='New to Amazon? Start here to create an account']"
    CREATE_DEVELOPER_ACCOUNT_BTN = "//a[@data-ld-append='SDRP_HP_H']"
    CREATE_ACCOUNT_BTN = "#createAccountSubmit"
    CAPTCHA_IMAGE = "//img[contains(@src, 'https://images-na.ssl-images-amazon.com/captcha')]"
    CAPTCHA_INPUT = "#captchacharacters"
    SUBMIT_CAPTCHA = "//button[@type='submit']"


class AmazonHomePage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.homepage_url = "https://sell.amazon.com/?ld=AZFSSOA_FTSELL-C&ref_=footer_soa"
        super().__init__()

    def load_page(self):
        self.random_sleep()
        logger.debug("Loading amazon Developer Homepage")
        self.driver.get(self.homepage_url)

        if self.check_captcha():
            logger.error("Captcha detected!")
            img = self.driver.find_element(By.XPATH, AmazonHomePageSelectors.CAPTCHA_IMAGE)
            link = img.get_attribute("src")
            answer = solve_text_captcha(link)
            self.driver.type(AmazonHomePageSelectors.CAPTCHA_INPUT, answer)
            self.random_sleep()
            self.driver.find_element(By.XPATH, AmazonHomePageSelectors.SUBMIT_CAPTCHA).click()

        self.random_sleep()
        self.driver.switch_to_default_window()
        logger.debug("Amazon Developer Homepage loaded successfully")

    def get_signup_page(self):
        self.random_sleep()
        logger.debug("Getting amazon account signup link")
        # Just to ensure the page loads correctly we need to refresh twice
        self.driver.refresh()
        self.random_sleep()
        self.driver.refresh()

        self.driver.click(AmazonHomePageSelectors.CREATE_DEVELOPER_ACCOUNT_BTN)
        self.random_sleep()

        self.driver.click(AmazonHomePageSelectors.CREATE_ACCOUNT_BTN)
        self.random_sleep()
        logger.debug(f"Signing up page is open now..")

    def check_captcha(self):
        try:
            captcha = self.driver.find_element(By.TAG_NAME, "h4")
            if captcha and "Enter the characters you see" in captcha.text:
                return True
        except NoSuchElementException:
            pass

        return False
