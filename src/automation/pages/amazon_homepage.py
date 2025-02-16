from selenium.webdriver.common.by import By

from utils.logger import logger
from automation.pages.base_page import BasePage
from integrations.captcha_service import solve_text_captcha


class AmazonHomePageSelectors:
    START_HERE = "//a[@aria-label='New to Amazon? Start here to create an account']"


class AmazonHomePage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.homepage_url = "https://www.amazon.com"
        super().__init__()

    def load_page(self):
        self.random_sleep()
        logger.debug("Loading amazon Homepage")
        self.driver.get(self.homepage_url)

        if self.check_captcha():
            logger.error("Captcha detected!")
            img = self.driver.find_element(By.XPATH,
                                      "//img[contains(@src, 'https://images-na.ssl-images-amazon.com/captcha')]")
            link = img.get_attribute("src")
            answer = solve_text_captcha(link)
            print(answer)
            self.driver.type("#captchacharacters", answer)
            self.random_sleep()
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        self.random_sleep()
        self.driver.switch_to_default_window()
        logger.debug("Amazon Homepage loaded successfully")

    def get_signup_url(self):
        self.random_sleep()
        logger.debug("Getting amazon account signup link")
        # Just to ensure the page loads correctly we need to refresh twice
        self.driver.refresh()
        self.random_sleep()
        self.driver.refresh()

        signup_url = self.driver.get_attribute(AmazonHomePageSelectors.START_HERE, "href", by="xpath")
        logger.debug(f"Extracted signup link {signup_url}")
        return signup_url

    def check_captcha(self):
        captcha = self.driver.find_element(By.TAG_NAME, "h4")
        if captcha and "Enter the characters you see" in captcha.text:
            return True
        return False
