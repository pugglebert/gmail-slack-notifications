# Slack notifications for shared Gmail account

## Setup

IMPORTANT: Your `.env`, `credentials.json` and `token.json` files should never be checked in to version control.

Prerequisists:
1. A Gmail account which you want to get notifications from
1. A Google Cloud account associated with your Gmail address
1. A Slack workspace which you have permission to add apps to
1. Python 3
1. The pip package management tool

Instructions:
1. Clone the project
1. Enable the [Google Cloud Gmail API](https://console.cloud.google.com/flows/enableapi?apiid=gmail.googleapis.com)
1. Create your Google Cloud Credentials
    1. If your project does not have an OAuth consent screen, create one via the [Google Cloud Console](https://console.cloud.google.com/apis/credentials/consent)
    1. Go to the [credentials screen](https://console.cloud.google.com/apis/credentials) and select Create Credentials -> OAuth client ID
    1. Select Application type -> Desktop app
    1. Fill out the other fields and click Create
    1. Download your credentials and save them to the project root as `credentials.json`
1. Create your Slack app
1. Install the necessary python libraries by running the following command

    ```
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib slack_sdk dotenv croniter
    ```
1. Create a `.env` file with the following content.
    ```
    SLACK_TOKEN=<OAuth token from your Slack app>
    ```
1. Modify the `constants.py` file to match your Gmail account and Slack workspace
1. Run the script using `python main.py`

## Resources:
- [Gmail API](https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/index.html)
- [Slack SDK](https://slack.dev/python-slack-sdk/)