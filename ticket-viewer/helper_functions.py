from user import *

def user_credentials():
    user_cred = User()

    try: 
        user_cred.get_cred()
        print(f"Found credentials for {user_cred.username}!")
    except Exception as e:    
        print(e)
        user_cred.username = input("Enter Zendesk Username or Email: ")
        user_cred.password = getpass("Enter Password: ")
        user_cred.expiry_time = -1
        user_cred.create_cred()
