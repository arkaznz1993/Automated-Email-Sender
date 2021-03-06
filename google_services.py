import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import constants


def google_service(service_type):
    """Returns a Google service object based
    on the service_type parameter passed
    Currently creates Sheets, Docs, and Gmail
    services.

    Args:
        service_type : Takes one of three values from the constants.py file

    Returns:
        A Google service object
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('venv/token.json'):
        creds = Credentials.from_authorized_user_file('venv/token.json', constants.SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'venv/credentials.json', constants.SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('venv/token.json', 'w') as token:
            token.write(creds.to_json())

    if service_type == constants.SHEETS:
        return build('sheets', 'v4', credentials=creds)
    elif service_type == constants.DOCS:
        return build('docs', 'v1', credentials=creds)
    else:
        return build('gmail', 'v1', credentials=creds)
