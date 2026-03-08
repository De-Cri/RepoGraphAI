from models import AuthService
from utils import normalize_username


def login_user(raw_username):
    username = normalize_username(raw_username)
    service = AuthService()
    token = service.issue_token(username)
    audit_login(token)


def audit_login(token):
    store_audit_entry(token)


def store_audit_entry(token):
    return token
