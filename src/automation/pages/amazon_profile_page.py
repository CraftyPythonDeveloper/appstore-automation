from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utils.logger import logger
from automation.pages.base_page import BasePage
from utils.utils import get_2fa_code


class AmazonProfilePageSelectors:
    ACCOUNT = "//a[contains(@href, 'AccountFlyout_ya')]"
    LOGIN_SECURITY = "//div[@data-card-identifier='SignInAndSecurity_C']"
    PASSWORD_INPUT = "#ap_password"
    PASSWORD_SUBMIT = "signInSubmit"
    MFA_LINK_TEXT = "Turn on"
    AUTHENTICATOR_RADIO = "#sia-otp-accordion-totp-header"
    SCAN_BARCODE_LINK_TEXT = "Can't scan the barcode?"
    MFA_SECRET_KEY = "#sia-auth-app-formatted-secret"
    TOTP_INPUT = "#ch-auth-app-code-input"
    VERIFY_TOTP_BUTTON = "#ch-auth-app-submit"
    SUBMIT_MFA_FORM_BUTTON = "#enable-mfa-form-submit"


class AmazonProfilePage(BasePage):
    def __init__(self, driver, password):
        self.driver = driver
        self.password = password
        self.account_page_link = "https://www.amazon.com/gp/css/homepage.html?ref_=nav_AccountFlyout_ya"
        super().__init__()

    def get_accounts_page(self):
        self.random_sleep()
        self.driver.get(self.account_page_link)

    def get_login_security(self):
        self.random_sleep()
        self.submit_password()
        login_security = self.driver.find_element(By.XPATH, AmazonProfilePageSelectors.LOGIN_SECURITY)
        login_security.click()
        self.submit_password()

    def submit_password(self):
        self.random_sleep()
        try:
            self.driver.type(AmazonProfilePageSelectors.PASSWORD_INPUT, self.password)
            self.random_sleep()
            self.driver.find_element(By.ID, AmazonProfilePageSelectors.PASSWORD_SUBMIT).click()
        except:     # just skip if there is no password to enter on a page.
            pass

    def setup_mfa(self):
        self.random_sleep()
        self.driver.click_link(AmazonProfilePageSelectors.MFA_LINK_TEXT)
        self.random_sleep()
        self.driver.click(AmazonProfilePageSelectors.AUTHENTICATOR_RADIO)
        self.driver.click_link(AmazonProfilePageSelectors.SCAN_BARCODE_LINK_TEXT)
        totp_secret = self.driver.get_text(AmazonProfilePageSelectors.MFA_SECRET_KEY)
        totp_secret = totp_secret.replace(" ", "")
        self.random_sleep()
        self.driver.click(AmazonProfilePageSelectors.TOTP_INPUT)
        self.driver.type(AmazonProfilePageSelectors.TOTP_INPUT, get_2fa_code(totp_secret))
        self.random_sleep()
        self.driver.click(AmazonProfilePageSelectors.VERIFY_TOTP_BUTTON)
        self.random_sleep()
        self.driver.click(AmazonProfilePageSelectors.SUBMIT_MFA_FORM_BUTTON)
        return totp_secret
