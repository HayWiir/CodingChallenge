import os
import sys
from getpass import getpass
from pathlib import Path

import requests
from cryptography.fernet import Fernet

from ticket_viewer.helper import api_call
from ticket_viewer.errors import *


class User:
    def __init__(self):
        self.__username = ""
        self.__subdomain = ""
        self.__key = ""
        self.__token = ""
        self.__key_file = Path.home() / "key.key"
        self.__cred_filename = Path.home() / "CredFile.ini"

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        while username == "":
            username = input("Blank email is not accepted:")
        self.__username = username

    @property
    def subdomain(self):
        return self.__subdomain

    @subdomain.setter
    def subdomain(self, subdomain):
        while subdomain == "":
            subdomain = input("Blank subdomain is not accepted:")
        self.__subdomain = subdomain

    @property
    def token(self):
        fernet_key = Fernet(self.__key)
        return fernet_key.decrypt(self.__token.encode()).decode()

    @token.setter
    def token(self, token):
        self.__key = Fernet.generate_key()
        fernet_key = Fernet(self.__key)
        self.__token = fernet_key.encrypt(token.encode()).decode()

    def env_delete(self):
        """
        Deletes credential config file in case env vars are used.
        """
        env_vars = ["ZENDESK_SUBDOMAIN", "ZENDESK_USER", "ZENDESK_TOKEN"]
        for var in env_vars:
            if var in os.environ:
                self.delete_cred()

    def input_cred(self):
        """
        Checks for credentials in environment variables else asks for user input.
        """
        self.subdomain = (
            os.environ["ZENDESK_SUBDOMAIN"]
            if ("ZENDESK_SUBDOMAIN" in os.environ)
            else input("Enter Zendesk Subdomain: ")
        )
        self.username = (
            os.environ["ZENDESK_USER"]
            if ("ZENDESK_USER" in os.environ)
            else input("Enter Zendesk Username or Email: ")
        )
        self.token = (
            os.environ["ZENDESK_TOKEN"]
            if ("ZENDESK_USER" in os.environ)
            else getpass("Enter Token: ")
        )

    def create_cred(self):
        """
        This function is responsible for encrypting the token and create  key file for
        storing the key and create a credential file with user name and token
        """

        with open(self.__cred_filename, "w") as file_in:
            file_in.write(
                "#Credential file:\nUsername={}\nSubdomain={}\nToken={}\n".format(
                    self.__username, self.__subdomain, self.__token
                )
            )
            file_in.write("++" * 20)

        # If there exists an older key file, This will remove it.
        if os.path.exists(self.__key_file):
            os.remove(self.__key_file)

        # Open the Key.key file and place the key in it.
        try:

            with open(self.__key_file, "w") as key_in:
                key_in.write(self.__key.decode())

        except PermissionError:
            os.remove(self.__key_file)
            print("A Permission error occurred.\n")
            sys.exit()

    def get_cred(self):
        """
        This function checks for an existing config file and key and extracts
        credentials from it.
        """
        key = ""

        with open(self.__key_file, "r") as key_in:
            key = key_in.read().encode()

        fernet_key = Fernet(key)
        with open(self.__cred_filename, "r") as cred_in:
            lines = cred_in.readlines()
            config = {}
            for line in lines:
                tuples = line.rstrip("\n").split("=", 1)
                if tuples[0] in ("Username", "Token", "Subdomain"):
                    config[tuples[0]] = tuples[1]

        self.username = config["Username"]
        self.subdomain = config["Subdomain"]
        self.token = fernet_key.decrypt(config["Token"].encode()).decode()

    def delete_cred(self):
        if os.path.exists(self.__key_file):
            os.remove(self.__key_file)
        if os.path.exists(self.__cred_filename):
            os.remove(self.__cred_filename)

    def authenticate(self):
        """
        This function is responsible authenticating the user credentials.
        Raises an Exception in case of failure
        """

        auth = (self.username, self.token)
        user_data = api_call(self.subdomain, f"users/me.json", auth)

        try:
            user_json = user_data.json()

            if user_json["user"]["id"] == None:
                raise Exception("Invalid Credentials")
            else:
                print()
                print(f"Hello {user_json['user']['name']}!")

        except Exception as e:
            self.delete_cred()
            raise AutheticationError("Authentication Error. Check credentials.")

    def authenticate_driver(self):
        """
        This function gets user credentials from existing config file
        or user input.
        It is called recursively until valid credentials are inputted
        """
        try:
            self.get_cred()
            print(f"Found credentials for {self.username}!")
        except Exception as e:
            self.input_cred()
            self.create_cred()

        try:
            self.authenticate()
        except AutheticationError as e:
            print(e)
            self.delete_cred()
            exit()
        except UnvailableAPIError as e:
            print(e)
            exit()
