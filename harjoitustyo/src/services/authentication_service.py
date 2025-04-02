from repositories.user_repository import user_repository


class AuthenticationService:
    def __init__(self, user_repository):
        self.user_repository = user_repository
        self.logged_in_user = None

    def log_in(self, username, password):
        user = self.user_repository.find_by_username(username)
        if user and user.password == password:
            self.logged_in_user = user
            return user
        return None

    def log_out(self):
        self.logged_in_user = None

    def get_logged_in_user(self):
        return self.logged_in_user

    def get_logged_in_user_id(self):
        if self.current_user:
            return self.current_user.user_id
        return None


auth_service = AuthenticationService(user_repository)
