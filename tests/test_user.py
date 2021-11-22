from ticket_viewer.user import *
from ticket_viewer.errors import *

def test_get_cred_fail():
    """
    get_cred() should fail when it cannot find
    the required .ini and .key files
    """

    user = User()

    user.username = "Wrong@example.com"
    user.password = "Incorrect"
    user.subdomain = "baddomain"

    try:
        user.get_cred()
        assert False
    except Exception as e:
        assert True


def test_get_cred_pass():
    """
    get_cred() should fail when it cannot find
    the required .ini and .key files
    """

    user = User()

    user.username = "Wrong@example.com"
    user.password = "Incorrect"
    user.subdomain = "baddomain"

    user.create_cred()

    try:
        user.get_cred()
        assert True
    except Exception as e:
        assert False


def test_auth_wrong_cred():
    """
    Checks authentication with incorrect credentials
    """
    user = User()
    user.username = "Wrong@example.com"
    user.password = "Incorrect"
    user.subdomain = "baddomain"

    user.create_cred()
    try:
        user.authenticate()
        assert False
    except AutheticationError:
        assert True
