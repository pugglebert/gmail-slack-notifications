import base64
import string
from collections import namedtuple
from croniter import croniter
from datetime import datetime

from constants import GMAIL_QUERY_STRING, USERS, EMAIL, SIGNATURES, CRON

MessageInfo = namedtuple("MessageInfo", "user_ids sender subject")

def get_email_info(service):
    results = service.users().messages().list(userId='me', q=_get_email_query(CRON)).execute()
    messages = results.get('messages', [])
    email_info = []

    for i in range(len(messages)):
        message_id = messages[i]['id']
        message = service.users().messages().get(userId='me', id=message_id).execute()
        email_info.append(_get_message_info(service, message))

    return email_info

def _get_email_query(cron):
    now = datetime.now()
    iter = croniter(cron, now)
    before = int(iter.get_prev())
    after = int(iter.get_prev())
    return GMAIL_QUERY_STRING(before, after)

def _get_message_info(service, message):
    userIds = _find_user_ids(service, message)
    
    headers = message['payload']['headers']
    sender = [i['value'] for i in headers if i["name"]=="From"][0]
    subject = [i['value'] for i in headers if i["name"]=="Subject"][0]
    
    return MessageInfo(userIds, sender, subject)

def _find_user_ids(service, message):
    userIds = _find_user_ids_from_greeting(message)
    if len(userIds) > 0:
        return userIds
    previous_messages = _get_previous_messages_in_thread(service, message)
    for previous_message in previous_messages:
        userIds = _find_user_ids_from_signature(previous_message)
        if len(userIds) > 0:
            return userIds
    return []

def _get_previous_messages_in_thread(service, message):
    thread = service.users().threads().get(userId='me', id=message['threadId']).execute()
    messages_to_return = []
    for thread_message in thread['messages']:
        headers = thread_message['payload']['headers']
        sender = [i['value'] for i in headers if i["name"]=="From"][0]
        if EMAIL not in sender:
            continue
        messages_to_return.append(thread_message)
    return messages_to_return
    
def _find_user_ids_from_greeting(message):
    body = _find_message_body_text(message)
    lines = body.splitlines()
    for line in lines:
        if not line.isspace():
            return _find_user_ids_from_line(line)
    return []
                
def _find_user_ids_from_signature(message):
    body = _find_message_body_text(message)
    lines = body.splitlines()
    for i in range(len(lines)):
        line = lines[i]
        for signature in SIGNATURES:
            if signature in line and i+1 < len(lines):
                return _find_user_ids_from_line(lines[i+1])
    return []

def _find_message_body_text(message):
    payload = message['payload']
    parts = [payload]
    i = 0
    while i < len(parts):
        part = parts[i]
        if part['mimeType'] in ['text/plain', 'text/html']:
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
        elif 'parts' in part.keys() and part['parts'] != None:
            parts.extend(part['parts'])
        i += 1
    return ''


def _find_user_ids_from_line(line):
    userIds = []
    words = line.split()
    for word in words:
        potential_name = word.translate(str.maketrans('', '', string.punctuation)).strip().lower()
        if potential_name in USERS:
            userIds.append(USERS[potential_name])
    return userIds