from ticket_viewer.helper import *
from ticket_viewer.ticket import *
from ticket_viewer.user import *


class Agent:
    def __init__(self) -> None:
        self.user = User()
        self.tickets = None

    def welcome(self):
        title()
        signin()

    def user_sigin(self):
        self.user.authenticate_driver()

        continue_with_existing_acc()
        user_input = input()
        if user_input.lower() == "n":
            self.user.delete_cred()
            self.user.authenticate_driver()
        else:
            pass

    def user_tickets(self):

        viewer()
        self.tickets = Tickets(self.user)
        self.tickets.get()

        print()
        print()
        print(f"There are {self.tickets.ticket_count} tickets")

    def viewer_menu(self):

        while True:
            menu()
            user_input = input(">> ")

            if user_input == "1":
                self.tickets.display_all()

            elif user_input == "2":
                number = int(input("Enter ticket number: "))
                try:
                    self.tickets.display_ticket(number)
                except Exception as e:
                    print(e)

            elif user_input == "":
                pass
            else:
                self.user.env_delete()
                break

    def start(self):
        """
        Driver function
        """
        self.welcome()
        self.user_sigin()
        self.user_tickets()
        self.viewer_menu()
