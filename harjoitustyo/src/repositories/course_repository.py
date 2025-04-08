from entities.course import Course
from database_connection import get_database_connection


class CourseRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_all(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM courses")
        rows = cursor.fetchall()
        return [Course(*row) for row in rows]

    def find_all_by_user(self, user_id):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM courses WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        return [Course(*row) for row in rows]

    def create(self, course):
        cursor = self._connection.cursor()
        cursor.execute(
            """INSERT INTO courses (user_id, code, name, credits, description, 
                    is_completed, is_scheduled)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                course.user_id,
                course.code,
                course.name,
                course.credits,
                course.description,
                course.is_completed,
                course.is_scheduled,
            ),
        )
        self._connection.commit()
        course.course_id = cursor.lastrowid
        return course

    def get_courses_by_period(self, period):
        cursor = self._connection.cursor()
        cursor.execute(
            """
                SELECT c.id, c.user_id, c.code, c.name, c.credits, c.description,
                c.is_completed, c.is_scheduled, c.grade, c.completion_date
                FROM courses c
                JOIN course_periods cp ON c.id = cp.course_id
                WHERE cp.period_id = ?
                """,
            (period.period_id,),
        )
        rows = cursor.fetchall()
        return [Course(*row) for row in rows]

    def add_to_period(self, period, course):
        cursor = self._connection.cursor()
        cursor.execute(
            """
            INSERT INTO course_periods (course_id, period_id)
            VALUES (?, ?)
            """,
            (course.course_id, period.period_id),
        )
        self._connection.commit()
        return True

    def get_courses_by_academicyear(self, academicyear):
        cursor = self._connection.cursor()
        cursor.execute(
            """
                SELECT c.*
                FROM courses c
                JOIN course_periods cp ON c.id = cp.course_id
                JOIN periods p ON cp.period_id = p.id
                JOIN academicyears ay ON p.academicyear_id = ay.id
                WHERE ay.id = ?
                """,
            (academicyear.year_id,),
        )
        rows = cursor.fetchall()
        return [Course(*row) for row in rows]

    def mark_as_completed(self, course_id):
        pass


course_repository = CourseRepository(get_database_connection())
