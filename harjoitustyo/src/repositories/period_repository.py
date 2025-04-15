from database_connection import get_database_connection
from entities.period import Period


class PeriodRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, period):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO periods (academicyear_id, period_number) VALUES (?, ?)",
            (period.academicyear_id, period.period_number),
        )
        self._connection.commit()
        period.period_id = cursor.lastrowid
        return period

    def get_periods_by_academic_year(self, academic_year):
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT id, academicyear_id, period_number FROM periods
            WHERE academicyear_id = ?
            """,
            (
                academic_year.year_id,
            ),
        )
        rows = cursor.fetchall()
        return [Period(row[0], row[1], row[2]) for row in rows]


period_repository = PeriodRepository(get_database_connection())
