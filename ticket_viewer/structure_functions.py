# This file contains functions which print menu or related stuff


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
