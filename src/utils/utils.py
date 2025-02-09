import os
from config.settings import settings

def join_paths(*args: str):
    return os.path.join(settings.WRK_DIR, *args)

def get_temp_path():
    temp_path = join_paths("temp")
    os.makedirs(temp_path, exist_ok=True)
    return temp_path
