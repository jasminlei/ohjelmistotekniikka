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

    def find_by_id(self, course_id):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
        row = cursor.fetchone()
        if row:
            return Course(*row)
        return None

    def create(self, course):
        cursor = self._connection.cursor()
        cursor.execute(
            """INSERT INTO courses (user_id, code, name, credits, description, 
                    is_completed)
                    VALUES (?, ?, ?, ?, ?, ?)""",
            (
                course.user_id,
                course.code,
                course.name,
                course.credits,
                course.description,
                course.is_completed,
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
                c.is_completed, c.grade, c.completion_date
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

    def remove_from_period(self, period, course):
        cursor = self._connection.cursor()
        cursor.execute(
            """
        DELETE FROM course_periods
        WHERE course_id = ? AND period_id = ?
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
            WHERE p.academicyear_id = ?
            """,
            (academicyear.year_id,),
        )
        rows = cursor.fetchall()
        return [Course(*row) for row in rows]

    def mark_completed(self, course, grade, date):
        cursor = self._connection.cursor()
        cursor.execute(
            """
        UPDATE courses
        SET grade = ?, is_completed = ?, completion_date = ?
        WHERE id = ?
        """,
            (grade, True, date, course.course_id),
        )
        self._connection.commit()
        return True

    def get_courses_not_in_period(self, period, user_id):
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT c.id, c.user_id, c.code, c.name, c.credits, c.description,
                c.is_completed, c.grade, c.completion_date
            FROM courses c
            LEFT JOIN course_periods cp ON c.id = cp.course_id AND cp.period_id = ?
            WHERE cp.course_id IS NULL AND c.user_id = ?
            """,
            (period.period_id, user_id),
        )

        rows = cursor.fetchall()
        return [Course(*row) for row in rows]


course_repository = CourseRepository(get_database_connection())
