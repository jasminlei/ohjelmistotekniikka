from repositories.user_repository import user_repository
from entities.user import User


class UserService:
    def __init__(self, repository):
        """
        Handles user-related actions like creating users.
        """
        self._user_repository = repository

    def create_user(self, username, password):
        """
        Creates a new user if the username is not already taken.

        Args:
            username (str): Username.
            password (str): Password.

        Returns:
            User: The created user object.
        """
        existing_user = self._user_repository.find_by_username(username)

        if existing_user:
            raise ValueError(f"Käyttäjänimi {username} on jo varattu!")

        user = self._user_repository.create(User(username, password))
        return user


user_service = UserService(user_repository)
