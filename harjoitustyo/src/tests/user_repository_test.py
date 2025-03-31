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

    def test_create_user(self):
        first_user = self.user_repository.create(self.user1)
        second_user = self.user_repository.create(self.user2)

        self.assertEqual(first_user.username, "user1")
        self.assertEqual(first_user.password, "pw1")
        self.assertEqual(second_user.username, "user2")
        self.assertEqual(second_user.password, "pw2")

    def test_find_by_username_existing_user(self):
        self.user_repository.create(self.user1)
        found_user = self.user_repository.find_by_username("user1")
        self.assertEqual(found_user.username, "user1")
        self.assertEqual(found_user.password, "pw1")

    def test_find_by_username_nonexistent_user(self):
        found_user = self.user_repository.find_by_username("nonexistent_user")
        self.assertIsNone(found_user)

    def test_find_all(self):
        self.user_repository.create(self.user1)
        self.user_repository.create(self.user2)

        users = self.user_repository.find_all()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].username, "user1")
        self.assertEqual(users[1].username, "user2")
