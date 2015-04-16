# -*- coding: utf-8 -*-
__author__ = "panter.dsd@gmail.com"

from configparser import ConfigParser


class ApplicationSettings(object):
    _settings_file_name = "JointPurchasesAssistant.ini"

    def __init__(self):
        super().__init__()

        self._config = ConfigParser()
        try:
            self.__load()
        except FileNotFoundError:
            self.__init_default_config()

    def login(self) -> str:
        return self._config["LOGIN"]["login"]

    def set_login(self, login: str):
        self._config["LOGIN"]["login"] = login

    def password(self) -> str:
        return self._config["LOGIN"]["password"]

    def set_password(self, password: str):
        self._config["LOGIN"]["password"] = password

    def save(self):
        with open(self._settings_file_name, "w") as f:
            self._config.write(f)

    def __load(self):
        self._config.read(self._settings_file_name)

    def __init_default_config(self):
        self._config["LOGIN"] = {
            "Login": str(),
            "Password": str()
        }