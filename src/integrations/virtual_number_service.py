import random

import requests
from config.settings import settings
from utils.logger import logger
from exceptions.virtual_number_exceptions import OnlineSimBadResponseException, MinimumBalanceException


class OnlineSimService:
    api_key = settings.ONLINE_SIM_APIKEY
    api_base_url = "https://onlinesim.io/api"
    tzid = None
    service = "amazon"

    def _add_auth(self, url):
        if "?" in url:
            return url + f"&apikey={self.api_key}"

        return url + f"?apikey={self.api_key}"

    def get_current_balance(self):
        url = f"{self.api_base_url}/getBalance.php"
        response = requests.get(self._add_auth(url))

        if not response.ok:
            msg = "There was an error while fetching current balance from onlinesim"
            logger.error(msg)
            raise OnlineSimBadResponseException(response, msg)

        response = response.json()
        return float(response["balance"])

    def check_minimum_balance(self):

        if self.get_current_balance() < 2:
            return False

        return True

    def get_new_number(self, country_code: int = None):
        if country_code is None:
            # country_code = self.get_cheapest_service_country()
            country_code = 1000     # code for canada

        logger.debug(f"getting number from country_code: {country_code}")
        current_balance = self.get_current_balance()
        if current_balance < 2:
            msg = ("The balance in your onlinesms account is less than $2. Please recharge your account to generate "
                   "new numbers")
            logger.error(msg)
            raise MinimumBalanceException(current_balance, msg)

        url = f"{self.api_base_url}/getNum.php"
        url += f"?lang=en&service=amazon&country={country_code}&number=true"

        response = requests.get(self._add_auth(url))
        if not response.ok:
            msg = "There was an error while creating new number from onlinesim"
            logger.error(msg)
            raise OnlineSimBadResponseException(response, msg)

        response = response.json()
        self.tzid = response["tzid"]
        return self.tzid

    def get_status(self, tzid=None):
        url = f"{self.api_base_url}/getState.php"

        if tzid is None:
            tzid = self.tzid

        url += f"?lang=en&message_to_code=true&msg_list=false&tzid={tzid}"

        response = requests.get(self._add_auth(url))
        if not response.ok:
            msg = "There was an error while creating new number from onlinesim"
            logger.error(msg)
            logger.debug(f"Response from onlinesim status_code: {response.status_code} and text: {response.text}")
            return None

        response = response.json()
        return response[0]

    def get_number(self, tzid=None, with_cc: bool = False):
        status = self.get_status(tzid=tzid)
        if with_cc:
            return status["number"]

        return status["number"][-10:]

    def get_message(self, tzid=None):
        status = self.get_status(tzid=tzid)
        return status.get("msg")

    def get_cheapest_service_country(self):
        url = f"{self.api_base_url}/v2/getNumberStat"
        url += f"?service={self.service}&page=1&lang=en"

        response = requests.get(self._add_auth(url))
        if not response.ok:
            msg = "There was an error while getting cheapest country from onlinesim"
            logger.error(msg)
            raise OnlineSimBadResponseException(response, msg)

        response = response.json()
        data = response["data"]
        countries = {record["code"]: record["price"] for idx, record in data["countries"].items()}
        countries.update({record["code"]: record["price"] for record in data["favorite_countries"]})

        sorted_country_code = sorted(countries, key=lambda c: countries[c])

        # randomly pick any 3 lowest price countries
        return random.choice(sorted_country_code[:5])
