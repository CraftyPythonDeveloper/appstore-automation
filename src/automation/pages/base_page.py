import random
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class BasePage:

    def __init__(self):
        pass

    @staticmethod
    def random_sleep(min_wait: int = 1, max_wait: int = 5):
        sleep_seconds = random.randint(min_wait, max_wait)
        sleep(sleep_seconds)
        return True

    def start_typing(self, elem, text, selector="css"):
        by_selector = By.CSS_SELECTOR
        if selector == "xpath":
            by_selector = By.XPATH
        if selector == "tag":
            by_selector = By.TAG_NAME

        if isinstance(elem, str):
            elem = self.driver.find_element(by_selector)

        action = ActionChains(self.driver)
        action.move_to_element(elem).click()
        for i in text:
            action.send_keys(i)
            action.perform()
            sleep(random.uniform(0.2, 0.5))
        return True

