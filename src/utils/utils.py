import csv
import os
import pyotp
from faker import Faker

from config.settings import settings
from utils.logger import logger

fake = Faker()


def join_paths(*args: str):
    return os.path.join(settings.WRK_DIR, *args)


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


def write_to_csv(name, phone_number, password, totp):
    filename = join_paths("accounts.csv")
    file_exists = os.path.exists(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Name", "Phone Number", "Password", "TOTP"])

        writer.writerow([name, phone_number, password, totp])
