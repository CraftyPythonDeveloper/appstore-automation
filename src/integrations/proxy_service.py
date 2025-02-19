import random
from config.settings import settings


def get_proxy_details():
    """
    Get proxy details
    :return:
    """
    username = f"{settings.OXYLABS_USERNAME}-cc-CA-sessid-aa{random.random()}"
    proxy = f"{username}:{settings.OXYLABS_PASSWORD}@{settings.OXYLABS_IP}:{settings.OXYLABS_PORT}"
    return proxy
