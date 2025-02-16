import os
from config.settings import settings
from utils.logger import logger


class CountryCodeMapping:
    canada = 1


def join_paths(*args: str):
    return os.path.join(settings.WRK_DIR, *args)


def get_temp_path():
    temp_path = join_paths("temp")
    os.makedirs(temp_path, exist_ok=True)
    return temp_path


def get_country_code(country: str):
    country = country.lower()
    if not hasattr(CountryCodeMapping, country):
        logger.error(f"Country code {country} is not available in country mapping")
        return None
    return getattr(CountryCodeMapping, country)
