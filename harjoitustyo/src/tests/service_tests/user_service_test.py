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
        success, user = self.user_service.create_user("test_user", "password123")

        self.assertTrue(success)
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.password, "password123")

    def test_create_existing_user_returns_false_and_error(self):
        self.user_service.create_user("test_user", "password")
        success, error = self.user_service.create_user("test_user", "password")
        self.assertFalse(success)
        self.assertEqual(error, "Käyttäjänimi test_user on jo varattu!")

    def test_create_user_too_short_usernaem_returns_false_and_error(self):
        success, error = self.user_service.create_user("pp", "password")
        self.assertFalse(success)
        self.assertEqual(error, "Käyttäjänimen tulee olla 3–30 merkkiä pitkä!")

    def test_create_user_too_long_usernaem_returns_false_and_error(self):
        username = "p" * 31
        success, error = self.user_service.create_user(username, "password")
        self.assertFalse(success)
        self.assertEqual(error, "Käyttäjänimen tulee olla 3–30 merkkiä pitkä!")
