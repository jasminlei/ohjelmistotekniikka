from entities.year import AcademicYear
from database_connection import get_database_connection


class AcademicYearRepository:
    """Repository class for handling database operations related to academic years."""

    def __init__(self, connection):
        """
        Initializes the repository with a database connection.

        Args:
            connection: A SQLite database connection object.
        """
        self._connection = connection

    def create(self, start_year, end_year):
        """
        Creates a new academic year in the database.

        Args:
            start_year (int): The starting year of the academic year.
            end_year (int): The ending year of the academic year.

        Returns:
            AcademicYear: New AcademicYear object with an assigned ID.
        """
        academic_year = AcademicYear(None, start_year, end_year)

        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO academicyears (start_year, end_year) VALUES (?, ?)",
            (academic_year.start_year, academic_year.end_year),
        )
        self._connection.commit()

        academic_year.year_id = cursor.lastrowid
        return academic_year

    def find_all_from_studyplan(self, studyplan_id):
        """
        Retrieves all academic years linked to a given study plan.

        Args:
            studyplan_id (int): The ID of the study plan.

        Returns:
            list[AcademicYear]: A list of AcademicYear objects associated with the study plan.
        """

        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT a.id, a.start_year, a.end_year
            FROM academicyears a
            JOIN studyplan_academicyear sa ON a.id = sa.academicyear_id
            WHERE sa.studyplan_id = ?
        """,
            (studyplan_id,),
        )
        rows = cursor.fetchall()

        return [
            AcademicYear(row["id"], row["start_year"], row["end_year"]) for row in rows
        ]

    def exists_in_studyplan(self, studyplan_id, start_year, end_year):
        """
        Checks if an academic year with the given start and end year exists in a study plan.

        Args:
            studyplan_id (int): The ID of the study plan.
            start_year (int): The start year of the academic year.
            end_year (int): The end year of the academic year.

        Returns:
            bool: True if the academic year exists in the study plan, False if not.
        """

        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM studyplan_academicyear sa
            JOIN academicyears a ON sa.academicyear_id = a.id
            WHERE sa.studyplan_id = ? AND a.start_year = ? AND a.end_year = ?
            """,
            (studyplan_id, start_year, end_year),
        )

        return cursor.fetchone()[0] > 0

    def get_total_credits(self, academicyear_id):
        """
        Calculates the total number of credits for all courses in a given academic year.

        Args:
            academicyear_id (int): The ID of the academic year.

        Returns:
            int: The total number of credits.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT SUM(c.credits) as total_credits
            FROM courses c
            JOIN course_periods cp ON c.id = cp.course_id
            JOIN periods p ON cp.period_id = p.id
            JOIN academicyears ay ON p.academicyear_id = ay.id
            WHERE ay.id = ?
            """,
            (academicyear_id,),
        )
        result = cursor.fetchone()

        return result["total_credits"] if result and result["total_credits"] else 0

    def get_completed_credits(self, academicyear_id):
        """
        Calculates the total number of completed credits for a given academic year.

        Args:
            academicyear_id (int): The ID of the academic year.

        Returns:
            int: The total number of completed credits.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT SUM(c.credits) as completed_credits
            FROM courses c
            JOIN course_periods cp ON c.id = cp.course_id
            JOIN periods p ON cp.period_id = p.id
            JOIN academicyears ay ON p.academicyear_id = ay.id
            WHERE ay.id = ? AND c.is_completed = 1
            """,
            (academicyear_id,),
        )
        result = cursor.fetchone()

        return (
            result["completed_credits"] if result and result["completed_credits"] else 0
        )

    def delete_by_id(self, year_id):
        """
        Deletes an academic year and its data from the database.

        Args:
            year_id (int): The ID of the academic year to delete.
        """

        cursor = self._connection.cursor()

        cursor.execute("DELETE FROM periods WHERE academicyear_id = ?", (year_id,))
        cursor.execute(
            "DELETE FROM studyplan_academicyear WHERE academicyear_id = ?", (year_id,)
        )
        cursor.execute("DELETE FROM academicyears WHERE id = ?", (year_id,))

        self._connection.commit()


academicyear_repository = AcademicYearRepository(get_database_connection())
