import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

dirname = os.path.dirname(__file__)


def get_database_connection(test=False):
    db_filename = (
        os.environ.get("TEST_DATABASE_FILENAME", "test_database.sqlite")
        if test
        else os.environ.get("DATABASE_FILENAME", "database.sqlite")
    )

    db_path = os.path.join(dirname, "..", "data", db_filename)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection
