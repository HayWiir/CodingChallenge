import textwrap
from datetime import datetime
from math import floor

from tabulate import tabulate
from ticket_viewer.errors import UnvailableAPIError

from ticket_viewer.helper import api_call


class Tickets:
    def __init__(self, user):
        self.user = user
        self.ticket_count = 0
        self.ticket_list = []

    def get_ticket_count(self):
        """
        This function queries the API to get a complete ticket count.
        """

        try:
            auth = (self.user.username, self.user.password)
            count_data = api_call(self.user.subdomain, f"tickets/count", auth)
        except UnvailableAPIError as e:
            print(e)
            exit()

        return count_data.json()["count"]["value"]

    def get_tickets(self):
        """
        This function queries the API for all tickets avaialable.
        It provides a progss bar as it receives tickets.
        """
        ticket_list = []

        page_count = 1
        curr_count = 0
        while True:

            auth = (self.user.username, self.user.password)
            try:
                tickets_data = api_call(
                    self.user.subdomain, f"tickets.json?page={page_count}", auth
                )
            except Exception as e:
                print(e)
                exit()

            tickets_json = tickets_data.json()
            ticket_list += tickets_json["tickets"]

            curr_count = len(ticket_list)
            print(
                f"Receiving tickets... [Progress {floor(curr_count/self.ticket_count*100)}%]",
                end="\r",
            )

            if tickets_json["next_page"] == None:
                break

            page_count += 1

        return ticket_list

    def display_all(self):
        """
        Displays tickets in a list. In case of more than 25 tickets,
        pages are created.
        """
        simplified_data = []
        for ticket in self.ticket_list:
            id = ticket["id"]
            subject = ticket["subject"]
            status = ticket["status"]
            last_update = datetime.strptime(ticket["updated_at"], "%Y-%m-%dT%H:%M:%Sz")
            last_update_str = datetime.strftime(last_update, "%B %d %Y %H:%M:%S")

            simplified_data.append([id, subject, status, last_update_str])

        if self.ticket_count <= 25:
            print(
                tabulate(
                    simplified_data, headers=["ID", "Subject", "Status", "Last Updated"]
                )
            )

        else:
            curr_start = 0

            while curr_start < self.ticket_count:

                print(
                    tabulate(
                        simplified_data[curr_start : curr_start + 25],
                        headers=["ID", "Subject", "Status", "Last Updated"],
                        tablefmt="fancy_grid",
                    )
                )
                print(f"Page {(curr_start+25)//25}")

                curr_start += 25
                if curr_start >= self.ticket_count:
                    print("This was the last page")
                    break

                user_input = input(
                    "To see more tickets, press Enter (Any other key to go back): "
                )
                if user_input != "":
                    break

    def ticket_tabulate(self, ticket):
        """
        Returns chosen attributes for a ticket in pretty format
        """
        attribute_list = [
            "id",
            "subject",
            "description",
            "status",
            "created_at",
            "updated_at",
            "tags",
            "url",
        ]
        ticket_data = []
        for attribute in attribute_list:
            if attribute == "description":
                ticket[attribute] = "\n".join(
                    textwrap.wrap(ticket[attribute], width=60, replace_whitespace=False)
                )
            ticket_data.append([attribute.capitalize(), ticket[attribute]])
        return tabulate(ticket_data, tablefmt="fancy_grid")

    def display_ticket(self, number):
        """
        Prints data for a given ticket number
        """
        index = number - 1
        if index >= self.ticket_count or index < 0:
            raise Exception("Invalid Ticket Number")

        else:
            print(self.ticket_tabulate(self.ticket_list[index]))
