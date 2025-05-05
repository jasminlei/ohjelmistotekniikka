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
        Creates a new user if the username is not already taken and meets length constraints.

        Args:
            username (str): Username.
            password (str): Password.

        Returns:
            tuple: (bool, User|str),
                   - True, User if successful
                   - False, error message if failed
        """
        if len(username) < 3 or len(username) > 30:
            return False, "Käyttäjänimen tulee olla 3–30 merkkiä pitkä!"

        existing_user = self._user_repository.find_by_username(username)

        if existing_user:
            return False, f"Käyttäjänimi {username} on jo varattu!"

        user = self._user_repository.create(User(username, password))
        return True, user


user_service = UserService(user_repository)
