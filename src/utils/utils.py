import csv
import os

import numpy as np
import pandas as pd
import pyotp
from faker import Faker

from config.settings import settings
from utils.logger import logger

fake = Faker()


def join_paths(*args: str) -> str:
    return str(os.path.join(settings.WRK_DIR, *args))


def get_temp_path():
    temp_path = join_paths("temp")
    os.makedirs(temp_path, exist_ok=True)
    return temp_path


def get_2fa_code(totp_secret: str):
    totp_secret = totp_secret
    return pyotp.TOTP(totp_secret).now()


def get_fake_name():
    """
    Generate a random fake name
    :return:
    """
    return fake.name()


def get_fake_password():
    """
    Generate a random password
    :return:
    """
    return fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)


def read_from_excel():
    filename = join_paths("accounts.xlsx")
    if not os.path.exists(filename):
        logger.error(f"File {filename} does not exist")
        return []

    df = pd.read_excel(filename)
    df = df.replace(np.nan, None)
    df["status"] = df["status"].astype(str)
    return df


def write_to_excel(index, **kwargs):
    filename = join_paths("accounts.xlsx")
    df = pd.read_excel(filename)
    row = df.iloc[index].to_dict()
    for key, value in kwargs.items():
        if key not in df.columns:
            logger.error(f"Key {key} not found in dataframe columns")
            continue
        row[key] = value

    df.iloc[index] = row
    df.to_excel(filename, index=False)
    return True
