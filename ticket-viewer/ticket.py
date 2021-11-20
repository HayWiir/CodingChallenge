import requests
from math import floor

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
            req = f'https://{self.user.subdomain}.zendesk.com/api/v2/tickets/count'
            count_data = requests.get(req, auth=(self.user.username, self.user.password))
        except Exception as e:
            # print(e)
            print("API unreachable. Max retries exhausted. Try again later.")
            exit()

        self.ticket_count = count_data.json()["count"]["value"]    

        page_count = 1
        curr_count = 0
        while(True):
            try:
                req = f'https://{self.user.subdomain}.zendesk.com/api/v2/tickets.json?page={page_count}'
                tickets_data = requests.get(req, auth=(self.user.username, self.user.password))
            except Exception as e:
                # print(e)
                print("API unreachable. Max retries exhausted. Try again later.")
                exit()

            tickets_json = tickets_data.json()
            self.ticket_list += tickets_json["tickets"]

            curr_count = len(self.ticket_list)
            print(f"Receiving tickets... [Progress {floor(curr_count/self.ticket_count*100)}%]", end='\r')

            if tickets_json["next_page"]==None:
                break

            page_count+=1

        print()
        # print(f'There are {len(self.ticket_list)} tickets.')        

    # def display_all(self):
    #     print("\tSubject\t\tRequester\tRequested")