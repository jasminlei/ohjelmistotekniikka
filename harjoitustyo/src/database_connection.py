import os
import sqlite3

dirname = os.path.dirname(__file__)


def get_database_connection(test=False):
    if test:
        connection = sqlite3.connect(
            os.path.join(dirname, "..", "data", "test_database.sqlite")
        )
    else:
        connection = sqlite3.connect(
            os.path.join(dirname, "..", "data", "database.sqlite")
        )

    connection.row_factory = sqlite3.Row
    return connection
