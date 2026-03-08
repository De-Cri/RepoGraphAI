from utils import hash_token


class AuthService:
    def issue_token(self, username):
        base = build_token_payload(username)
        return hash_token(base)

    def check_token(self, token):
        return token_is_not_empty(token)


class ProfileService:
    def load_profile(self, username):
        profile = fetch_profile_data(username)
        return format_profile(profile)

    def save_profile(self, username):
        profile = fetch_profile_data(username)
        return persist_profile(profile)


def build_token_payload(username):
    return f"user:{username}"


def token_is_not_empty(token):
    return bool(token)


def fetch_profile_data(username):
    return {"username": username, "active": True}


def format_profile(profile):
    return profile


def persist_profile(profile):
    return profile
