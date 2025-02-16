from utils.logger import logger


class BadResponseException(Exception):

    def __init__(self, response, readable_message):
        message = f"Failed to get response from {response.url}, the status code received is {response.status_code} and body is {response.text}"
        logger.debug(message)
        super().__init__(readable_message)
