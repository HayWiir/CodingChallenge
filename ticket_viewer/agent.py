from getpass import getpass

from structure_functions import *
from ticket import *
from user import *


class Agent:
    def __init__(self) -> None:
        self.user = User()
        self.tickets = None

    def start(self):
        """
        Driver function
        """
        title()
        signin()
        self.authenticate_user()
        self.tickets = Tickets(self.user)
        viewer()
        self.tickets.get_tickets()

        while True:
            menu()
            user_input = input(">> ")

            if user_input == "1":
                self.tickets.display_all()
            elif user_input == "2":
                number = int(input("Enter ticket number: "))
                self.tickets.display_ticket(number)
            elif user_input == "":
                pass
            else:
                break

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
            if e == Exception("Authentication Error"):
                self.authenticate_user()
            else:
                print(e)
                exit()
