from exceptions.base_exceptions import BadResponseException
from utils.logger import get_logger

logger = get_logger()


class OnlineSimBadResponseException(BadResponseException):
    pass


class MinimumBalanceException(Exception):
    def __init__(self, response, readable_message):
        logger.debug(f"The current balance is {response['balance']} which is lower than minimum required balance of $2")
        super().__init__(readable_message)
