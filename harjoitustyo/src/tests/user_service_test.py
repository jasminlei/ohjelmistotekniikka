import unittest
from services.user_service import UserService


class MockUserRepository:
    def __init__(self):
        self.users = []

    def find_by_username(self, username):
        return next((user for user in self.users if user.username == username), None)

    def create(self, user):
        if self.find_by_username(user.username):
            raise Exception("User already exists")
        self.users.append(user)
        return user

    def find_all(self):
        return self.users


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MockUserRepository()
        self.user_service = UserService(self.mock_repository)

    def test_create_user(self):
        user = self.user_service.create_user("test_user", "password123")
        self.assertEqual(user.username, "test_user")

    def test_create_existing_user_raises_exception(self):
        self.user_service.create_user("test_user", "password")
        with self.assertRaises(Exception):
            self.user_service.create_user("test_user", "password2")

    def test_find_all_users(self):
        self.user_service.create_user("user1", "pass1")
        self.user_service.create_user("user2", "pass2")
        users = self.user_service.get_all_users()

        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].username, "user1")
        self.assertEqual(users[1].username, "user2")
