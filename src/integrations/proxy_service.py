import random
from config.settings import settings


def get_proxy_details():
    """
    Get proxy details
    :return:
    """
    username = f"{settings.OXYLABS_USERNAME}-cc-CA-sessid-aa{random.random()}"
    proxy = f"{username}:{settings.OXYLABS_PASSWORD}@{settings.OXYLABS_IP}:{settings.OXYLABS_PORT}"
    "customer-webart_8fOBF-cc-CA-cc-CA-sessid-aa546:Password007_@pr.oxylabs.io:7777"
    return proxy
