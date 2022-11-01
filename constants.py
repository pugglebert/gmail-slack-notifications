SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
USERS = {'milly': 'U0XXXXXXXXX', 'molly': 'U0XXXXXXXXX', 'mandy': 'U0XXXXXXXXX'} # Change me
EMAIL = 'example@gmail.com' # Change me
SIGNATURES = ['Cheers', 'Thanks', 'Best', 'Regards']
CRON = '0 17 * * *'
CHANNEL_ID = "C0XXXXXXXXX" # Change me
DEFAULT_USERS = []

def GMAIL_QUERY_STRING(before, after): return f'before:{before} after:{after}'

def USER_NOTIFICATION_TEXT(user_tag, subject, sender): return f'There is a new message for {user_tag}!\nSubject: {subject}\nSender: {sender}'

def TEAM_NOTIFICATION_TEXT(subject, sender): return f'There is a new message for the team!\nSubject: {subject}\nSender: {sender}'

def DEFAULT_USER_NOTIFICATION_TEXT(user_tag, subject, sender): return f'There is a new message for the team (attention {user_tag})!\nSubject: {subject}\nSender: {sender}'

def NOTIFICATION_BLOCKS(text): return [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }
]