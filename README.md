# Zendesk Ticket Viewer
Created as part of the Zendesk Coding Challenge.

---
## Features
- Connect to Zendesk API
- Request all the tickets for your account
- Display tickets in a list (with pagination)
- Display individual ticket details

---

## Setup
Install all requirements for `python3`
```console
pip install -r requirements.txt
```

## Usage
```console
python3 main.py
```
You will be asked for login credentials on first run. These are stored locally in an encrypted Config.ini file. 
This will be decrypted in future runs for ease of access.
![Alt Text](media/demo.gif)