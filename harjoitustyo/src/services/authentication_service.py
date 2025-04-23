from repositories.user_repository import user_repository as user_repo


class AuthenticationService:
    """Handles user authentication and session management,
    keeps track of the currently logged-in user."""

    def __init__(self, user_repository):
        """
        Initialize the service with a user repository.

        Args:
            user_repository: Repository for accessing user data.
        """
        self._user_repository = user_repository
        self.logged_in_user = None

    def log_in(self, username, password):
        """
        Log in a user with the given credentials.

        Args:
            username (str): username.
            password (str): password.

        Returns:
            User: The user object if credentials are correct, None otherwise.
        """
        user = self._user_repository.find_by_username(username)
        if user and user.password == password:
            self.logged_in_user = user
            return user
        return None

    def log_out(self):
        """
        Log out the current user.
        """
        self.logged_in_user = None

    def get_logged_in_user(self):
        """
        Get the currently logged-in user.

        Returns:
            User: The user object, or None if not logged in.
        """
        return self.logged_in_user

    def get_logged_in_user_id(self):
        """
        Get the ID of the currently logged-in user.

        Returns:
            user_id (int) or None: The user ID, or None if not logged in.
        """
        if self.logged_in_user:
            return self.logged_in_user.id
        return None


auth_service = AuthenticationService(user_repo)
