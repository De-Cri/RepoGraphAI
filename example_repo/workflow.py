from auth import login_user
from models import ProfileService
from notifications.emailer import send_welcome_email


def run_user_onboarding(username):
    login_user(username)
    profile_service = ProfileService()
    profile_service.save_profile(username)
    send_welcome_email(username)
