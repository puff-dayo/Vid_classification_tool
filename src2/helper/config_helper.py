import configparser
import os

from src2.helper.app_path_helper import CONFIG_FILE, EXE_PATH


def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config['main'] = {
            'db_file': os.path.join(EXE_PATH, 'vct_db.json'),
        }
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(CONFIG_FILE)
    return config


def save_config(config):
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
