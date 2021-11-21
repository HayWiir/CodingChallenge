# This file contains helper functions
import requests


def title():
    print()
    print("*" * 100)
    print("|", " " * 96, "|")
    print(
        """
                 .&&&&&&&&&&&&&&&&&&&&#   &&&&&&&&&&&&&&&&&&&&                  
                  &&&&&&&&&&&&&&&&&&&&    &&&&&&&&&&&&&&&&&&                    
                    &&&&&&&&&&&&&&&&*     &&&&&&&&&&&&&&&&                      
                      &&&&&&&&&&&&        &&&&&&&&&&&&&&                        
                                     &&   &&&&&&&&&&&&                          
                                   &&&&   &&&&&&&&&&                            
                                 &&&&&&   &&&&&&&&                              
                              /&&&&&&&&   &&&&&%                                
                            &&&&&&&&&&&   &&&*                                  
                          &&&&&&&&&&&&&   &                                     
                        &&&&&&&&&&&&&&&       &&&&&&&&&&&&&                     
                      &&&&&&&&&&&&&&&&&     &&&&&&&&&&&&&&&&&&                  
                    &&&&&&&&&&&&&&&&&&&   .&&&&&&&&&&&&&&&&&&&&                 
                  &&&&&&&&&&&&&&&&&&&&&   &&&&&&&&&&&&&&&&&&&&&
    """
    )

    print("|", " " * 96, "|")
    print("*" * 100)


def signin():
    print()
    print()
    print("Sign in to your Zendesk Account")
    print()


def continue_with_existing_acc():
    print()
    print("Press N to sign in with a different account | Anything else to continue: ")
    print()


def viewer():
    print()
    print(
        """
Welcome to Zendesk Ticket Viewer!
    """
    )
    print()


def menu():
    print()
    print()
    print(
        """
    Enter 1 to view all tickets
    Enter 2 to view a specific ticket
    Any other key to exit
  """
    )
    print()


def api_call(subdomain, suffix, auth):
    try:
        req = f"https://{subdomain}.zendesk.com/api/v2/{suffix}"
        data = requests.get(req, auth=auth)
        return data
    except Exception as e:
        raise Exception("API unreachable. Max retries exhausted. Try again later.")
