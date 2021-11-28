# Zendesk Ticket Viewer

Created as part of the Zendesk Coding Challenge.

  

---

## Features

- Connect to Zendesk API

- Request all the tickets for your account

- Display tickets in a list (with pagination)

- Display individual ticket details

  

---

## Design

The tool takes login credentials via environment variables or user input.

The environment variables are `ZENDESK_SUBDOMAIN`, `ZENDESK_USER`, `ZENDESK_TOKEN`.

  

NOTE: If env vars are set, they will always be picked up without user input.

  

The credentials are then stored in a config file with the token encrypted. They are authenticated by calling the API.

In case of failure, the config file is deleted and program quits.

  

For valid credentials, all the tickets for the user are pulled from the API (as per the requirements) using offset pagination. The user is provided with an input menu for the specified features.

  

Zendesk API can be found [here](https://developer.zendesk.com/api-reference).

  

## Setup

Clone repository
```console
git clone https://github.com/HayWiir/CodingChallenge && cd CodingChallenge
```
(Optional) Create virtual environment
```console
python3 -m venv test && source test/bin/activate
```

Create `.env` file for credentials.
```console
nano .env
```
We use [python-dotenv](https://pypi.org/project/python-dotenv/) for setting environment variables. The contents of `.env` should look like this and be in the root directory.
```console
ZENDESK_SUBDOMAIN=exampleDomain
ZENDESK_USER=user@example.com
ZENDESK_TOKEN=exampleexampleexampleexampleexample
```

Install all requirements for `python3`. Make sure to upgrade `pip` before.

```console

python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt

```

  

## Usage

```console

python3 main.py

```

The login credentials are picked from the `.env` file. These are stored locally in an encrypted Config.ini file.

This will be decrypted in future runs for ease of access.

  

![Alt Text](media/demo.gif)

  

## Testing

The `pytest` library is used for unit testing. Tests are under the `tests/` directory. For testing and coverage,

```console

python3 -m coverage run --source . -m pytest && python3 -m coverage report

```

The code has been tested on macOS 11.5.2 and CentOS 7.9. It has not been tested on Windows. However, the code does not contain OS specific libraries.
