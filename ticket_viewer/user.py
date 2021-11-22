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
        self.__password = ""
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
    def password(self):
        fernet_key = Fernet(self.__key)
        return fernet_key.decrypt(self.__password.encode()).decode()

    @password.setter
    def password(self, password):
        self.__key = Fernet.generate_key()
        fernet_key = Fernet(self.__key)
        self.__password = fernet_key.encrypt(password.encode()).decode()

    def input_cred(self):
        self.subdomain = input("Enter Zendesk Subdomain: ")
        self.username = input("Enter Zendesk Username or Email: ")
        self.password = getpass("Enter Password: ")

    def create_cred(self):
        """
        This function is responsible for encrypting the password and create  key file for
        storing the key and create a credential file with user name and password
        """

        with open(self.__cred_filename, "w") as file_in:
            file_in.write(
                "#Credential file:\nUsername={}\nSubdomain={}\nPassword={}\n".format(
                    self.__username, self.__subdomain, self.__password
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
                if tuples[0] in ("Username", "Password", "Subdomain"):
                    config[tuples[0]] = tuples[1]

        self.username = config["Username"]
        self.subdomain = config["Subdomain"]
        self.password = fernet_key.decrypt(config["Password"].encode()).decode()

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

        auth = (self.username, self.password)
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
            raise AutheticationError("Authentication Error")

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
            self.authenticate_driver()
        except UnvailableAPIError as e:
            print(e) 
            exit()