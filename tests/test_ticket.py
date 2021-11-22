from ticket_viewer import ticket
from ticket_viewer.ticket import *
from ticket_viewer.user import *
import json
from tabulate import tabulate


def dummy_ticket_user(requests_mock):
    user = User()
    user.username = "Wrong@example.com"
    user.password = "Incorrect"
    user.subdomain = "baddomain"

    req = f"https://{user.subdomain}.zendesk.com/api/v2/tickets.json?page=1"
    requests_mock.get(req, json=json.load(open("tests/dummy_tickets.json")))

    ticket = Tickets(user)
    ticket.ticket_count = 100
    ticket.ticket_list = ticket.get_tickets()

    return user, ticket


def test_ticket_count(requests_mock):
    user = User()
    user.username = "Wrong@example.com"
    user.password = "Incorrect"
    user.subdomain = "baddomain"
    # user.create_cred()

    # req1 = f"https://{user.subdomain}.zendesk.com/api/v2/tickets/count"
    # requests_mock.get(req1, json=json.load(open('tests/dummy_tickets.json')))

    req2 = f"https://{user.subdomain}.zendesk.com/api/v2/tickets/count"
    requests_mock.get(req2, json=json.load(open("tests/dummy_count.json")))

    ticket = Tickets(user)

    assert ticket.get_ticket_count() == 100


def test_ticket_list(requests_mock):
    user, ticket = dummy_ticket_user(requests_mock)

    assert len(ticket.ticket_list) == 100


def test_ticket_printer(requests_mock, capfd):

    user, ticket = dummy_ticket_user(requests_mock)

    test_print_data = [
        ["Id", 1],
        ["Subject", "Sample ticket: Meet the ticket"],
        [
            "Description",
            "Hi there,\n\nI’m sending an email because I’m having a problem\nsetting up your new product. Can you help me troubleshoot?\nThanks,\n The Customer",
        ],
        ["Status", "open"],
        ["Created_at", "2021-11-19T19:24:50Z"],
        ["Updated_at", "2021-11-19T19:24:51Z"],
        ["Tags", ["sample", "support", "zendesk"]],
        ["Url", "https://zcckjoshi.zendesk.com/api/v2/tickets/1.json"],
    ]

    test_ticket = {
        "url": "https://zcckjoshi.zendesk.com/api/v2/tickets/1.json",
        "id": 1,
        "external_id": None,
        "via": {
            "channel": "sample_ticket",
            "source": {"from": {}, "to": {}, "rel": None},
        },
        "created_at": "2021-11-19T19:24:50Z",
        "updated_at": "2021-11-19T19:24:51Z",
        "type": "incident",
        "subject": "Sample ticket: Meet the ticket",
        "raw_subject": "Sample ticket: Meet the ticket",
        "description": "Hi there,\n\nI’m sending an email because I’m having a problem setting up your new product. Can you help me troubleshoot?\n\nThanks,\n The Customer\n\n",
        "priority": "normal",
        "status": "open",
        "recipient": None,
        "requester_id": 1903484768407,
        "submitter_id": 421863573032,
        "assignee_id": 421863573032,
        "organization_id": None,
        "group_id": 1900001798247,
        "collaborator_ids": [],
        "follower_ids": [],
        "email_cc_ids": [],
        "forum_topic_id": None,
        "problem_id": None,
        "has_incidents": False,
        "is_public": True,
        "due_at": None,
        "tags": ["sample", "support", "zendesk"],
        "custom_fields": [],
        "satisfaction_rating": None,
        "sharing_agreement_ids": [],
        "fields": [],
        "followup_ids": [],
        "ticket_form_id": 1900000495447,
        "brand_id": 1900000303707,
        "allow_channelback": False,
        "allow_attachments": True,
    }

    assert ticket.ticket_tabulate(test_ticket) == tabulate(
        test_print_data, tablefmt="fancy_grid"
    )


def test_display_ticket_wrong(requests_mock):
    user, ticket = dummy_ticket_user(requests_mock)

    try:
        ticket.display_ticket(300)
        assert False
    except Exception as e:
        assert True


def test_display_ticket_correct(requests_mock):
    user, ticket = dummy_ticket_user(requests_mock)

    try:
        ticket.display_ticket(12)
        assert True
    except Exception as e:
        assert False

def test_display_all(requests_mock, monkeypatch):
    user, ticket = dummy_ticket_user(requests_mock)

    monkeypatch.setattr('builtins.input', lambda _: "e")

    try:
        ticket.display_all()
        assert True
    except Exception as e:
        assert False                