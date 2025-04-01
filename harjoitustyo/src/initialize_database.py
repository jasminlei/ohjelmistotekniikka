from database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        drop table if exists users;
    """)

    cursor.execute("""
        DROP TABLE IF EXISTS courses;
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS periods;
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS courseperiods;
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS academicyears;
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS studyplans;
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

    cursor.execute("""
    CREATE TABLE courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        name TEXT NOT NULL,
        credits INTEGER NOT NULL,
        description TEXT,
        is_scheduled BOOLEAN DEFAULT FALSE,
        is_completed BOOLEAN DEFAULT FALSE
    );
    """)

    cursor.execute("""
    CREATE TABLE periods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        academicyear_id INTEGER,
        period_number INTEGER,
        FOREIGN KEY (academicyear_id) REFERENCES academicyears(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE courseperiods (
        course_id INTEGER,
        period_id INTEGER,
        FOREIGN KEY (course_id) REFERENCES courses(id),
        FOREIGN KEY (period_id) REFERENCES periods(id),
        PRIMARY KEY (course_id, period_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE academicyears (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_year INTEGER NOT NULL,
        end_year INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE studyplans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_name TEXT,
        user_id INTEGER,
        academicyear_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (academicyear_id) REFERENCES academicyears(id)
        );
    """)

    connection.commit()


def initialize_database(test=False):
    connection = get_database_connection(test)

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()
