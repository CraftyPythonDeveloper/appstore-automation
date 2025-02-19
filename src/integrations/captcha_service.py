import json
import os
from pathlib import Path
from amazoncaptcha import AmazonCaptcha
from config.settings import settings
from utils.logger import logger


def get_captcha_extension():
    logger.debug("Getting captcha extension path")
    current_path = Path(__file__).resolve().parents[0]

    captcha_ext_path = os.path.join(current_path, "nopecha")
    if settings.NOPECHA_API_KEY:
        logger.debug("Found api key for nopecha in config, going to use the api key now")
        captcha_ext_path = os.path.join(current_path, "nopecha-auto")
        manifest_file = os.path.join(captcha_ext_path, "manifest.json")
        with open(manifest_file, "r") as fp:
            manifest = json.load(fp)

        manifest["nopecha"]["key"] = settings.NOPECHA_API_KEY

        with open(manifest_file, "w") as fp:
            logger.debug("Writing the changes to manifest file of nopecha")
            json.dump(manifest, fp, indent=4)

    logger.debug(f"Captcha extension path is {captcha_ext_path}")
    return captcha_ext_path


def solve_text_captcha(link):
    captcha = AmazonCaptcha.fromlink(link)
    text = captcha.solve(keep_logs=True)
    return text
