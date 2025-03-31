import unittest
from services.authentication_service import AuthenticationService
from entities.user import User


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


class TestAuthenticationService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MockUserRepository()
        self.auth_service = AuthenticationService(self.mock_repository)
        self.test_user = User(username="testuser", password="testpassword")
        self.mock_repository.create(self.test_user)

    def test_log_in_with_correct_credentials(self):
        user = self.auth_service.log_in("testuser", "testpassword")
        self.assertEqual(user.username, "testuser")

    def test_log_in_with_wrong_password(self):
        user = self.auth_service.log_in("testuser", "wrongpassword")
        self.assertIsNone(user)

    def test_log_in_with_wrong_username(self):
        user = self.auth_service.log_in("wrongusernaem", "password")
        self.assertIsNone(user)

    def test_log_out(self):
        self.auth_service.log_in("testuser", "testpassword")
        self.auth_service.log_out()
        self.assertIsNone(self.auth_service.get_logged_in_user())

    def test_get_logged_in_user(self):
        self.auth_service.log_in("testuser", "testpassword")
        user = self.auth_service.get_logged_in_user()
        self.assertEqual(user.username, "testuser")
