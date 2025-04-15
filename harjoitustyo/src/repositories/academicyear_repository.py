from entities.year import AcademicYear
from database_connection import get_database_connection


class AcademicYearRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, start_year, end_year):
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


academicyear_repository = AcademicYearRepository(get_database_connection())
