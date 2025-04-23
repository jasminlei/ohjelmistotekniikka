import unittest
from entities.user import User
from initialize_database import initialize_database
from database_connection import get_database_connection
from repositories.user_repository import UserRepository


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        initialize_database(test=True)
        self.connection = get_database_connection(test=True)
        self.user_repository = UserRepository(self.connection)
        self.user1 = User("user1", "pw1")
        self.user2 = User("user2", "pw2")
        self.first_user = self.user_repository.create(self.user1)
        self.second_user = self.user_repository.create(self.user2)

    def test_create_user(self):
        user = self.user_repository.create(User("user", "pw"))

        self.assertEqual(user.username, "user")
        self.assertEqual(user.password, "pw")
