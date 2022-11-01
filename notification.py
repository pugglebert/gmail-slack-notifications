from constants import CHANNEL_ID, DEFAULT_USERS, NOTIFICATION_BLOCKS, USER_NOTIFICATION_TEXT, TEAM_NOTIFICATION_TEXT, DEFAULT_USER_NOTIFICATION_TEXT


def send_notifications(slack_client, email_info):
    for message_info in email_info:
        text = _build_body_text(message_info)
        slack_client.chat_postMessage(
            channel=CHANNEL_ID,
            blocks=NOTIFICATION_BLOCKS(text),
            text=text
        )


def _build_body_text(message_info):
    if (len(message_info.user_ids) > 0):
        user_tag = _build_user_tag(message_info.user_ids)
        return USER_NOTIFICATION_TEXT(user_tag, message_info.subject, message_info.sender)
    elif (len(DEFAULT_USERS) > 0):
        user_tag = _build_user_tag(DEFAULT_USERS)
        return DEFAULT_USER_NOTIFICATION_TEXT(user_tag, message_info.subject, message_info.sender)
    else:
        return TEAM_NOTIFICATION_TEXT(message_info.subject, message_info.sender)


def _build_user_tag(user_ids):
    user_ids_formatted = []
    for user_id in user_ids:
        user_ids_formatted.append(f'<@{user_id}>')
    if len(user_ids_formatted) < 3:
        return ' and '.join(user_ids_formatted)
    return ', '.join(user_ids_formatted[:-1]) + ', and ' + user_ids_formatted[-1]
