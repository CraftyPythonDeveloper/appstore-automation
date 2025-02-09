from seleniumbase import Driver

from integrations.captcha_service import get_captcha_extension
from integrations.proxy_service import get_proxy_details


class BaseDriver:
    def __init__(self):
        """
        Initializes the BaseDriver with configuration options.

        """
        self.driver = None

    def get_driver(self, enable_captcha_solver=True, enable_proxy=False, **driver_options):
        """
        Returns a Selenium WebDriver instance based on the specified driver type.
        """
        driver_options["uc"] = driver_options.get("uc", True)

        if enable_captcha_solver:
            driver_options["extension_dir"] = get_captcha_extension()

        if enable_proxy:
            driver_options["proxy"] = get_proxy_details()

        self.driver = Driver(browser="chrome", **driver_options)

        return self.driver

    def quit_driver(self):
        """
        Quits the WebDriver if it has been initialized.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
