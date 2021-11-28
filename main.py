from ticket_viewer.agent import *
from dotenv import load_dotenv



if __name__ == "__main__":
    load_dotenv()

    agent = Agent()
    agent.start()
