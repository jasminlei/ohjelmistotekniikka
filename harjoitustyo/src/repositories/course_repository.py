from entities.course import Course
from database_connection import get_database_connection


class CourseRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM courses")
        rows = cursor.fetchall()
        return [
            Course(
                course_id=row["id"],
                code=row["code"],
                name=row["name"],
                credits=row["credits"],
                description=row["description"],
                is_scheduled=row["is_scheduled"],
                is_completed=row["is_completed"],
            )
            for row in rows
        ]

    def create(self, course):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO courses (code, name, credits, description, is_scheduled, is_completed) VALUES (?, ?, ?, ?, ?, ?)",
            (
                course.code,
                course.name,
                course.credits,
                course.description,
                course.is_scheduled,
                course.is_completed,
            ),
        )
        self._connection.commit()
        course.course_id = cursor.lastrowid
        return course


course_repository = CourseRepository(get_database_connection())
