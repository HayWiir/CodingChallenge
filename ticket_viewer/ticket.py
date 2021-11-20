import textwrap
from datetime import datetime
from math import floor

import requests
from tabulate import tabulate


class Tickets:
    def __init__(self, user):
        self.user = user
        self.ticket_list = []
        self.ticket_count = 0

    def get_tickets(self):
        """
        This function queries the API for all tickets avaialable.
        It provides a progss bar as it receives tickets.
        """
        try:
            req = f"https://{self.user.subdomain}.zendesk.com/api/v2/tickets/count"
            count_data = requests.get(
                req, auth=(self.user.username, self.user.password)
            )
        except Exception as e:
            # print(e)
            print("API unreachable. Max retries exhausted. Try again later.")
            exit()

        self.ticket_count = count_data.json()["count"]["value"]

        page_count = 1
        curr_count = 0
        while True:
            try:
                req = f"https://{self.user.subdomain}.zendesk.com/api/v2/tickets.json?page={page_count}"
                tickets_data = requests.get(
                    req, auth=(self.user.username, self.user.password)
                )
            except Exception as e:
                # print(e)
                print("API unreachable. Max retries exhausted. Try again later.")
                exit()

            tickets_json = tickets_data.json()
            self.ticket_list += tickets_json["tickets"]

            curr_count = len(self.ticket_list)
            print(
                f"Receiving tickets... [Progress {floor(curr_count/self.ticket_count*100)}%]",
                end="\r",
            )

            if tickets_json["next_page"] == None:
                break

            page_count += 1

        print()
        # print(f'There are {len(self.ticket_list)} tickets.')

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

    def ticket_printer(self, ticket):
        """
        Prints chosen attributes for a ticket
        """
        attribute_list = ["id", "subject", "description", "status", "tags", "url"]
        ticket_data = []
        for attribute in attribute_list:
            if attribute == "description":
                ticket[attribute] = "\n".join(
                    textwrap.wrap(ticket[attribute], width=60, replace_whitespace=False)
                )
            ticket_data.append([attribute.capitalize(), ticket[attribute]])

        print(tabulate(ticket_data, tablefmt="fancy_grid"))

    def display_ticket(self, number):
        """
        Prints data for a given ticket number
        """
        index = number - 1
        if index >= self.ticket_count or index < 0:
            print()
            print(
                f"INVALID TICKET NUMBER. Please enter a valid number. There are {self.ticket_count} tickets."
            )

        else:
            self.ticket_printer(self.ticket_list[index])
