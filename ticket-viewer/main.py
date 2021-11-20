from structure_functions import *
from user import *

from getpass import getpass

title()
signin_menu()
signin_input = str(input('>>> '))

if signin_input=='1':
    user_cred = User()

    try: 
        user_cred.get_cred()
        print(f"Found credentials for {user_cred.username}!")
    except Exception as e: 
        # print(e)
        user_cred.subdomain = input("Enter Zendesk Subdomain: ") 
        user_cred.username = input("Enter Zendesk Username or Email: ")
        user_cred.password = getpass("Enter Password: ")
        user_cred.expiry_time = -1
        user_cred.create_cred()

    user_cred.authenticate()    

else:
    exit()



    
