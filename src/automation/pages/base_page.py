import random
from time import sleep


class BasePage:

    def __init__(self):
        pass

    @staticmethod
    def random_sleep(min_wait: int = 1, max_wait: int = 5):
        sleep_seconds = random.randint(min_wait, max_wait)
        sleep(sleep_seconds)
        return True

