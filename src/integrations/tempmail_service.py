import time
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup

from exceptions.tempmail_exceptions import TempMailBadResponseException
from utils.logger import logger


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
