from database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        drop table if exists users;
    """)

    connection.commit()


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    connection.commit()


def initialize_database(test=False):
    connection = get_database_connection(test)

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()
