from __future__ import print_function

import os, os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from slack_sdk import WebClient

from dotenv import load_dotenv

from notification import send_notifications
from gmail import get_email_info
from constants import SCOPES

def main():
    load_dotenv()
    slack_token = os.getenv('SLACK_TOKEN')
    gmail_creds = load_gmail_credentials()

    service = build('gmail', 'v1', credentials=gmail_creds)
    email_info = get_email_info(service)
    slack_client = WebClient(token=slack_token)
    send_notifications(slack_client, email_info)

def load_gmail_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

if __name__ == '__main__':
    main()