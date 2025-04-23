from entities.user import User
from database_connection import get_database_connection


def get_user_by_row(row):
    """
    Converts a database row into a User object.

    Args:
        row (sqlite3.Row): A row from the users table.

    Returns:
        User | None: A User object if row is not None, otherwise None.
    """
    return (
        User(id=row["id"], username=row["username"], password=row["password"])
        if row
        else None
    )


class UserRepository:
    """Repository class for handling user-related database operations."""

    def __init__(self, connection):
        """
        Initializes the repository with a database connection.

        Args:
            connection: A SQLite database connection object.
        """
        self._connection = connection

    def find_by_username(self, username):
        """
        Finds a user by their username.

        Args:
            username (str): The username to search for.

        Returns:
            User | None: The user if found, otherwise None.
        """
        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

        row = cursor.fetchone()

        return get_user_by_row(row)

    def create(self, user):
        """
        Inserts a new user into the database.

        Args:
            user (User): The User object to insert.

        Returns:
            User: The inserted User object with an assigned ID.
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, user.password),
        )

        self._connection.commit()
        user.id = cursor.lastrowid
        return user


user_repository = UserRepository(get_database_connection())
