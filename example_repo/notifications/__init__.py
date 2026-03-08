from notifications.emailer import send_welcome_email


def notify_signup(username):
    send_welcome_email(username)
