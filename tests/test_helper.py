from ticket_viewer.helper import *
from ticket_viewer.user import *
from ticket_viewer.errors import *


def test_auth_no_api(socket_disabled, capfd):
    """
    Checks authetication when API unavailable.
    Uses pytest-socket to disable socket requests.
    """
    user = "Wrong@example.com"
    psswd = "Incorrect"
    subdomain = "baddomain"
    suffix = "tickets"

    try:
        api_call(subdomain, suffix, (user, psswd))
        assert False
    except UnvailableAPIError:
        assert True

def test_title():
    try:
        title()
        assert True
    except Exception as e:
        assert False

def test_signin():
    try:
        signin()
        assert True
    except Exception as e:
        assert False   

def test_continue_with_existing_acc():
    try:
        continue_with_existing_acc()
        assert True
    except Exception as e:
        assert False

def test_viewer():
    try:
        viewer()
        assert True
    except Exception as e:
        assert False

def test_menu():
    try:
        menu()
        assert True
    except Exception as e:
        assert False
            