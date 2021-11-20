import os
import sys
from pathlib import Path

import requests
from cryptography.fernet import Fernet


class User:
    def __init__(self):
        self.__username = ""
        self.__subdomain = ""
        self.__key = ""
        self.__password = ""
        self.__key_file = Path.home() / "key.key"
        self.__time_of_exp = -1
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
            username = input("Blank subdomain is not accepted:")
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

    @property
    def expiry_time(self):
        return self.__time_of_exp

    @expiry_time.setter
    def expiry_time(self, exp_time):
        if exp_time >= 2:
            self.__time_of_exp = exp_time

    def create_cred(self):
        """
        This function is responsible for encrypting the password and create  key file for
        storing the key and create a credential file with user name and password
        """

        with open(self.__cred_filename, "w") as file_in:
            file_in.write(
                "#Credential file:\nUsername={}\nSubdomain={}\nPassword={}\nExpiry={}\n".format(
                    self.__username,
                    self.__subdomain,
                    self.__password,
                    self.__time_of_exp,
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

    def authenticate(self):
        """
        This function is responsible authenticating the user credentials.
        Raises an Exception in case of failure
        """
        try:
            req = f"https://{self.subdomain}.zendesk.com/api/v2/users/me.json"
            user_data = requests.get(req, auth=(self.username, self.password))

        except Exception as e:
            raise Exception("API unreachable. Max retries exhausted. Try again later.")

        try:
            user_json = user_data.json()

            if user_json["user"]["id"] == None:
                raise Exception("Invalid Credentials")
            else:
                print(f"Hello {user_json['user']['name']}!")

        except Exception as e:

            if os.path.exists(self.__key_file):
                os.remove(self.__key_file)
            if os.path.exists(self.__cred_filename):
                os.remove(self.__cred_filename)

            raise Exception("Authentication Error")
