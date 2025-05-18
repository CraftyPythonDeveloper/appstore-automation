import random
import re
import time
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# from exceptions.tempmail_exceptions import TempMailBadResponseException
# from utils.logger import logger
import logging

logger = logging.getLogger(__name__)

TempMailBadResponseException = Exception

@dataclass
class TempMailConstants:
    TEMP_MAIL_URL: str = "https://mailtemp-production.up.railway.app/api"
    EMAIL_ENDPOINT: str = "/email"
    MESSAGES_ENDPOINT: str = "/messages"


class TempMailService:
    def __init__(self):
        self.session = requests.Session()
        self.constants = TempMailConstants()
        self._email_id = None
        self._email_address = None

    def get(self, url, retry: int = 0):
        response = self.session.get(url)
        if not response.ok:
            logger.debug(f"Get request failed. url: {url}, status code {response.status_code} - {response.text}")
            if retry < 3:
                logger.debug(f"Retrying with retry count {retry}")
                time.sleep(1)
                return self.get(url, retry=retry+1)
            raise TempMailBadResponseException(
                response=response, readable_message="Get request failed after 3 retry."
            )
        return response

    def post(self, url: str, data: dict = None, retry: int = 0):
        response = self.session.post(url, json=data)
        if not response.ok:
            logger.debug(
                f"Post request failed url: {url}, payload: {data}, status code {response.status_code} - {response.text}"
            )
            if retry < 3:
                logger.debug(f"Retrying with retry count {retry}")
                time.sleep(1)
                return self.post(url, data=data, retry=retry+1)
            raise TempMailBadResponseException(
                response=response, readable_message="Post request failed after 3 retry"
            )
        return response

    def get_new_email_id(self):
        url = f"{self.constants.TEMP_MAIL_URL}{self.constants.EMAIL_ENDPOINT}"
        response = self.post(url=url)
        data = response.json()
        self._email_id = data["id"]
        self._email_address = data["address"]
        return self._email_address

    def get_amazon_message(self, wait_timeout: int = 60) -> str:
        url = f"{self.constants.TEMP_MAIL_URL}{self.constants.EMAIL_ENDPOINT}/{self._email_id}{self.constants.MESSAGES_ENDPOINT}"
        for i in range(wait_timeout):
            response = self.get(url)
            messages = response.json()
            if messages and messages[0]["subject"].lower() == "Verify your new Amazon account".lower():
                soup = BeautifulSoup(messages[0]["content"][0], "html.parser")
                return soup.find("td", {"class": "data"}).text
            print("No new messages")
            time.sleep(2)
        return ""


class OutlookEmailService:
    def __init__(self, username, password, headless=False):
        """
        Initialize the OutlookEmailReader.

        Args:
            headless (bool): Whether to run the browser in headless mode.
        """
        self.driver = Driver(uc=True, headless=headless)
        self.is_logged_in = False
        self.logger = logger
        self.username = username
        self.password = password

        self.login()

    def _wait_and_find_element(self, by, selector, timeout=20):
        """
        Wait for an element to be present and return it.

        Args:
            by: The method to locate the element (e.g., By.ID)
            selector: The selector string
            timeout: Maximum time to wait in seconds

        Returns:
            The WebElement if found

        Raises:
            TimeoutException: If element is not found within the timeout period
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
        except TimeoutException:
            self.logger.error(f"Element not found: {selector}")
            raise

    def random_sleep(self, min_seconds=1, max_seconds=3):
        """
        Sleep for a random duration between min_seconds and max_seconds.

        Args:
            min_seconds (int): Minimum sleep time in seconds
            max_seconds (int): Maximum sleep time in seconds
        """
        sleep_time = random.uniform(min_seconds, max_seconds)
        self.logger.info(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)


    def login(self):
        """
        Sign in to Outlook with the provided credentials.

        Returns:
            bool: True if login was successful, False otherwise
        """
        try:
            self.logger.info("Navigating to Outlook login page")
            self.driver.get("https://login.live.com/login.srf")

            # Enter email
            self.logger.info("Entering email address")
            try:
                email_field = self._wait_and_find_element(By.ID, "i0116", timeout=5)
            except:
                email_field = self._wait_and_find_element(By.ID, "usernameEntry", timeout=5)
            email_field.clear()
            email_field.send_keys(self.username)
            email_field.send_keys(Keys.ENTER)
            self.random_sleep(3,6)

            # Enter password
            self.logger.info("Entering password")
            try:
                password_field = self._wait_and_find_element(By.ID, "i0118")
            except:
                password_field = self._wait_and_find_element(By.ID, "passwordEntry")
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.ENTER)
            self.random_sleep(3,6)

            # Handle "Stay signed in?" prompt
            try:
                self.logger.info("Handling 'Stay signed in' prompt")
                stay_signed_in = self._wait_and_find_element(By.XPATH, '//button[text()="Yes"]', timeout=5)
                stay_signed_in.click()
            except TimeoutException:
                self.logger.info("No 'Stay signed in' prompt detected")

            # Verify login success by checking for mailbox load
            self.logger.info("Navigating to Outlook inbox")
            self.driver.get("https://outlook.live.com/mail/0/inbox")
            self.random_sleep(3,6)
            self.driver.get("https://outlook.live.com/mail/0/inbox")

            try:
                self._wait_and_find_element(By.XPATH, "//button[text()='No, thanks']", timeout=3)
                self.random_sleep(3, 6)
            except TimeoutException:
                pass

            # Wait for the page to load and check if we're logged in
            try:
                self._wait_and_find_element(By.ID, "app", timeout=15)
                self.is_logged_in = True
                self.logger.info("Successfully logged in to Outlook")
                return True
            except TimeoutException:
                self.logger.error("Failed to login - couldn't detect Outlook app interface")
                return False

        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            return False

    def get_inbox_messages(self, limit=10):
        """
        Get a list of messages from the inbox.

        Args:
            limit (int): Maximum number of messages to retrieve

        Returns:
            list: List of message preview data (sender, subject, etc.)
        """
        if not self.is_logged_in:
            self.logger.error("Not logged in. Please log in first.")
            return []

        try:
            self.logger.info("Fetching inbox messages")
            # Ensure we're in the inbox
            # self.driver.get("https://outlook.live.com/mail/0/inbox")
            self.random_sleep(3, 5)

            # Wait for the mail list to load
            message_list = []

            # Different selectors to try for message items
            selectors = [
                (By.CSS_SELECTOR, "[role='option']"),
                (By.CSS_SELECTOR, ".zHQkBf"),
                (By.CSS_SELECTOR, ".IjzWp"),
                (By.CLASS_NAME, "S2NDX")
            ]

            message_items = None
            for by_method, selector in selectors:
                try:
                    message_items = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((by_method, selector))
                    )

                    if message_items:
                        break
                except TimeoutException:
                    continue

            if not message_items:
                self.logger.warning("No messages found in inbox")
                return []

            # Process messages
            count = 0
            for item in message_items:
                if count >= limit:
                    break

                try:
                    message_data = {
                        "text": item.text,
                        "element": item
                    }
                    message_list.append(message_data)
                    count += 1
                except Exception as e:
                    self.logger.warning(f"Error processing message: {str(e)}")

            self.logger.info(f"Retrieved {len(message_list)} messages from inbox")
            return message_list

        except Exception as e:
            self.logger.error(f"Error getting inbox messages: {str(e)}")
            return []

    def get_latest_message(self):
        """
        Get the most recent message in the inbox.

        Returns:
            dict: Message data including sender, subject, preview, or None if no messages
        """
        messages = self.get_inbox_messages(limit=1)
        if messages:
            return messages[0]
        return None

    def open_message(self, message_element):
        """
        Open a specific message to read its contents.

        Args:
            message_element: The WebElement of the message to open

        Returns:
            str: The content of the message body, or None if failed
        """
        if not self.is_logged_in:
            self.logger.error("Not logged in. Please log in first.")
            return None

        try:
            self.logger.info("Opening message")
            message_element.click()
            time.sleep(2)

            # Try different selectors for message body
            body_selectors = [
                (By.XPATH, '//div[@aria-label="Message body"]'),
                (By.XPATH, '//div[@role="main"]//div[@role="document"]'),
                (By.CSS_SELECTOR, ".x_ReadMsgBody"),
                (By.CSS_SELECTOR, ".allowTextSelection")
            ]

            for by_method, selector in body_selectors:
                try:
                    body_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((by_method, selector))
                    )
                    message_content = body_element.text
                    self.logger.info("Successfully retrieved message content")
                    return message_content
                except TimeoutException:
                    continue

            self.logger.warning("Could not find message body with any selector")
            return None

        except Exception as e:
            self.logger.error(f"Error opening message: {str(e)}")
            return None

    def read_latest_message(self):
        """
        Get and read the content of the latest message.

        Returns:
            dict: Message data including content, or None if failed
        """
        latest = self.get_latest_message()
        if not latest:
            return None

        content = self.open_message(latest["element"])
        if content:
            latest["content"] = content
            return latest
        return None

    def get_amazon_message(self, wait_timeout: int = 60) -> dict | None:
        self.random_sleep(5,10)

        for i in range(wait_timeout):
            latest_message = self.read_latest_message()
            print(latest_message)
            message_text = latest_message["text"]
            # validate if it's aws message, then parse the otp
            if "Verify your new Amazon account" in message_text and "One Time Password (OTP):" in message_text:
                match = re.search("One Time Password \(OTP\): (\d{6})", message_text)
                try:
                    otp = match.group(1)
                    return otp
                except AttributeError:
                    pass

            self.random_sleep(1, 2)
            self.logger.info("No new messages, retrying...")

        return None


    def close(self):
        """
        Close the browser and clean up resources.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.is_logged_in = False
            self.logger.info("Closed OutlookEmailReader")
#
# if __name__ == "__main__":
#
#     # Get login credentials
#     email = "nicholas_stephens408@outlook.com"
#     password = "Benefit@1708but"
#
#     # Initialize the email reader
#     reader = OutlookEmailService(email, password, headless=False)
#
#     try:
#         # Login
#         if reader.is_logged_in:
#             print("Login successful!")
#
#             # Get latest message
#             latest = reader.get_latest_message()
#             if latest:
#                 print("\nLatest message preview:")
#                 print(latest["text"])
#
#                 # Read the message content
#                 content = reader.open_message(latest["element"])
#                 if content:
#                     print("\nMessage content:")
#                     print(content)
#
#             # Search for messages (optional)
#             # search_term = input("\nEnter search term (or press Enter to skip): ")
#             # if search_term:
#             #     results = reader.search_messages(search_term)
#             #     print(f"\nFound {len(results)} messages matching '{search_term}'")
#
#             # Logout
#         else:
#             print("Login failed. Please check your credentials.")
#     finally:
#         # Always close the browser
#         # reader.close()
#         pass