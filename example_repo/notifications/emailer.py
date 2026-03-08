from utils import normalize_username


class Mailer:
    def deliver_message(self, username):
        clean_username = normalize_username(username)
        body = compose_body(clean_username)
        return smtp_send(body)


def send_welcome_email(username):
    mailer = Mailer()
    mailer.deliver_message(username)


def compose_body(username):
    return f"Welcome {username}"


def smtp_send(body):
    return body
