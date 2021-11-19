from structure_functions import *
from classes import *

from getpass import getpass

title()
signin_menu()
signin_input = str(input('>>> '))
if signin_input=='1':
    user_cred = User()

    user_cred.username = input("Enter Zendesk Username or Email: ")
    user_cred.password = getpass("Enter Password: ")
    print("Enter the expiry time for key file in minutes, [default:Will never expire]")
    user_cred.expiry_time = int(input("Enter time:") or '-1')
    user_cred.create_cred()

else:
    exit()

    
