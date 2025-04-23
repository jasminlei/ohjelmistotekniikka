import unittest
from initialize_database import initialize_database
from database_connection import get_database_connection
from services.user_service import UserService
from repositories.user_repository import UserRepository


class TestUserService(unittest.TestCase):
    def setUp(self):
        initialize_database(test=True)
        self.connection = get_database_connection(test=True)
        self.user_repository = UserRepository(self.connection)
        self.user_service = UserService(self.user_repository)

    def test_create_user(self):
        user = self.user_service.create_user("test_user", "password123")
        self.assertEqual(user.username, "test_user")

    def test_create_existing_user_raises_exception(self):
        self.user_service.create_user("test_user", "password")
        with self.assertRaises(Exception):
            self.user_service.create_user("test_user", "password2")
