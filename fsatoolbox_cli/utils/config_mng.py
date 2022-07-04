import configparser
import os

filename = "config.ini"


def create_config(**kwargs):
    config = configparser.ConfigParser()
    config.read(filename)

    try:
        config.add_section("DIRECTORY SETTINGS")
    except configparser.DuplicateSectionError:
        pass

    path = kwargs.get('cwdir') if kwargs.get('cwdir') else os.getcwd()

    config.set("DIRECTORY SETTINGS", "cwdir", path)

    with open(filename, "w") as config_file:
        config.write(config_file)


def change_cwdir(new_dir):
    if not os.path.exists(filename):
        raise FileNotFoundError

    config = configparser.ConfigParser()
    config.read(filename)

    try:
        config.set("DIRECTORY SETTINGS", "cwdir", new_dir)

    except configparser.NoSectionError:
        config.add_section("DIRECTORY SETTINGS")
        config.set("DIRECTORY SETTINGS", "cwdir", new_dir)

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def read_cwdir():
    if not os.path.exists(filename):
        raise FileNotFoundError

    config = configparser.ConfigParser()
    config.read(filename)

    value = config.get("DIRECTORY SETTINGS", "cwdir")
    return value