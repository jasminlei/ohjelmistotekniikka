from entities.course import Course
from database_connection import get_database_connection


class CourseRepository:
    """Repository class for handling all database operations related to courses."""

    def __init__(self, connection):
        """
        Initializes the repository with a database connection.

        Args:
            connection: A SQLite database connection object.
        """
        self._connection = connection

    def find_all_by_user(self, user_id):
        """
        Retrieves all courses created by a specific user.

        Args:
            user_id (int): The user's ID.

        Returns:
            list[Course]: A list of the user's Course objects.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM courses WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        return [Course(*row) for row in rows]

    def find_by_id(self, course_id):
        """
        Retrieves a course by its ID.

        Args:
            course_id (int): The ID of the course.

        Returns:
            Course | None: The Course object if found, otherwise None.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
        row = cursor.fetchone()
        if row:
            return Course(*row)
        return None

    def create(self, course):
        """
        Inserts a new course into the database.

        Args:
            course (Course): The course object that is added.

        Returns:
            Course: The created course object with an assigned ID.
        """
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
        """
        Retrieves all courses assigned to a specific period.

        Args:
            period: The period object.

        Returns:
            list[Course]: A list of Course objects in the period.
        """
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
        """
        Assigns a course to a specific period.

        Args:
            period: The period object.
            course: The course object.

        Returns:
            bool: True if operation was successful.
        """
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
        """
        Removes a course from a specific period.

        Args:
            period: The period object.
            course: The course object.

        Returns:
            bool: True if operation was successful.
        """

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
        """
        Retrieves all courses that belong to a specific academic year.

        Args:
            academicyear: The academic year object.

        Returns:
            list[Course]: A list of Course objects.
        """
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
        """
        Marks a course as completed with a grade and completion date.

        Args:
            course: The course object.
            grade (str): The grade.
            date (str): The date of completion.

        Returns:
            bool: True if update was successful.
        """

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

    def get_courses_by_studyplan(self, studyplan):
        """
        Retrieves all courses assigned to a specific study plan.

        Args:
            studyplan: The study plan object.

        Returns:
            list[Course]: A list of Course objects.
        """

        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT c.*
            FROM courses c
            JOIN course_periods cp ON c.id = cp.course_id
            JOIN periods p ON cp.period_id = p.id
            JOIN academicyears ay ON p.academicyear_id = ay.id
            JOIN studyplan_academicyear spa ON ay.id = spa.academicyear_id
            JOIN studyplans sp ON spa.studyplan_id = sp.id
            WHERE sp.id = ?;
        """,
            (studyplan.plan_id,),
        )

        rows = cursor.fetchall()
        return [Course(*row) for row in rows]

    def delete(self, course_id):
        """
        Deletes a course and all of its associations.

        Args:
            course_id (int): The ID of the course to delete.
        """

        cursor = self._connection.cursor()

        cursor.execute("DELETE FROM course_periods WHERE course_id = ?", (course_id,))
        cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))

        self._connection.commit()

    def get_course_timing(self, course):
        """
        Retrieves timing information for a course that is assigned to a plan, including
        studyplan, academic year, and period.

        Args:
            course: The course object.

        Returns:
            list[dict]: A list of timing details for the course, or an empty list if not found.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT sp.id as studyplan_id, sp.plan_name,
                ay.id as academicyear_id, ay.start_year || '-' || ay.end_year as year,
                p.id as period_id, p.period_number as period_name
            FROM courses c
            JOIN course_periods cp ON c.id = cp.course_id
            JOIN periods p ON cp.period_id = p.id
            JOIN academicyears ay ON p.academicyear_id = ay.id
            JOIN studyplan_academicyear spa ON ay.id = spa.academicyear_id
            JOIN studyplans sp ON spa.studyplan_id = sp.id
            WHERE c.id = ?
            """,
            (course.course_id,),
        )
        rows = cursor.fetchall()

        if not rows:
            return []

        return [
            {
                "studyplan": {
                    "studyplan_id": row[0],
                    "plan_name": row[1],
                },
                "academicyear": {
                    "academicyear_id": row[2],
                    "year": row[3],
                },
                "period": {"period_id": row[4], "period_name": f"Periodi {row[5]}"},
            }
            for row in rows
        ]


course_repository = CourseRepository(get_database_connection())
