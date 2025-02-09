import requests
from config.settings import settings
from utils.logger import get_logger
from exceptions.virtual_number_exceptions import OnlineSimBadResponseException, MinimumBalanceException

logger = get_logger()


class OnlineSimService:
    api_key = settings.ONLINE_SIM_APIKEY
    api_base_url = "https://onlinesim.io/api"
    tzid = None
    country = 1

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

    def get_new_number(self):

        current_balance = self.get_current_balance()
        if current_balance < 2:
            msg = "The balance in your onlinesms account is less than $2. Please recharge your account to generate new numbers"
            logger.error(msg)
            raise MinimumBalanceException(current_balance, msg)

        url = f"{self.api_base_url}/getNum.php"
        url += f"?lang=en&service=amazon&country={self.country}&number=true"

        response = requests.get(self._add_auth(url))
        if not response.ok:
            msg = "There was an error while creating new number from onlinesim"
            logger.error(msg)
            raise OnlineSimBadResponseException(response, msg)

        response = response.json()
        self.tzid = response["tzid"]
        return self.tzid

    def get_message(self, tzid=None):
        url = f"{self.api_base_url}/getState.php"

        if tzid is None:
            tzid = self.tzid

        url += f"?lang=en&message_to_code=true&msg_list=false&tzid={tzid}"

        response = requests.get(self._add_auth(url))
        if not response.ok:
            msg = "There was an error while creating new number from onlinesim"
            logger.error(msg)
            raise OnlineSimBadResponseException(response, msg)

        response = response.json()
        return response.get("msg")
