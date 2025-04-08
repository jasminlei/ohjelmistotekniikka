from repositories.user_repository import user_repository
from entities.user import User


class UserService:
    def __init__(self, repository):
        self._user_repository = repository

    def create_user(self, username, password):
        existing_user = self._user_repository.find_by_username(username)

        if existing_user:
            raise ValueError(f"Käyttäjänimi {username} on jo varattu!")

        user = self._user_repository.create(User(username, password))
        return user

    def get_all_users(self):
        return self._user_repository.find_all()


user_service = UserService(user_repository)
