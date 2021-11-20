from ticket_viewer import ticket
from ticket_viewer.ticket import *
from ticket_viewer.user import *
import json
import re

def test_ticket_count(requests_mock):
    user = User()
    user.username = "Wrong@example.com"
    user.password = "Incorrect"
    user.subdomain = "baddomain"
    # user.create_cred()

    # req1 = f"https://{user.subdomain}.zendesk.com/api/v2/tickets/count"
    # requests_mock.get(req1, json=json.load(open('ticket_viewer/tests/dummy_tickets.json')))

    req2 = f"https://{user.subdomain}.zendesk.com/api/v2/tickets/count"
    requests_mock.get(req2, json=json.load(open('ticket_viewer/tests/dummy_count.json')))


    ticket = Tickets(user)

    assert ticket.get_ticket_count() == 100

def test_ticket_list(requests_mock):
    user = User()
    user.username = "Wrong@example.com"
    user.password = "Incorrect"
    user.subdomain = "baddomain"
    # user.create_cred()

    req = f"https://{user.subdomain}.zendesk.com/api/v2/tickets.json?page=1"
    requests_mock.get(req, json=json.load(open('ticket_viewer/tests/dummy_tickets.json')))

    ticket = Tickets(user)
    ticket.ticket_count = 100

    assert len(ticket.get_tickets()) == 100    
