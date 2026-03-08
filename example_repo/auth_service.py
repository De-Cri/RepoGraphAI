class AuthService:
    def authenticate(self, user_id):
        self.get_user(user_id)

    def get_user(self, user_id):
        return {"id": user_id}


def helper_function():
    return None
