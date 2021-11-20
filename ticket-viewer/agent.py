from structure_functions import *
from user import *

from getpass import getpass


class Agent:
    def __init__(self) -> None:
        self.user = User()

    def start(self):
        """
        Driver function
        """
        title()
        signin()
        self.authenticate_user()
        viewer()
    

    def authenticate_user(self):
        """
        This function gets user credentials from existing config file
        or user input. 
        It is called recursively until valid credentials are inputted
        """
        try: 
            self.user.get_cred()
            print(f"Found credentials for {self.user.username}!")
        except Exception as e: 
            # print(e)
            self.user.subdomain = input("Enter Zendesk Subdomain: ") 
            self.user.username = input("Enter Zendesk Username or Email: ")
            self.user.password = getpass("Enter Password: ")
            self.user.expiry_time = -1
            self.user.create_cred()
        try:
            self.user.authenticate()
        except Exception as e:
            print(e)
            self.authenticate_user()    


               