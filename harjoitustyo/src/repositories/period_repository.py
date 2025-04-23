from database_connection import get_database_connection
from entities.period import Period


class PeriodRepository:
    """Repository class for handling database operations related to periods."""

    def __init__(self, connection):
        """
        Initializes the repository with a database connection.

        Args:
            connection: A SQLite database connection object.
        """
        self._connection = connection

    def create(self, period):
        """
        Inserts a new period into the database.

        Args:
            period (Period): The Period object to insert.

        Returns:
            Period: The inserted Period object with the generated ID.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO periods (academicyear_id, period_number) VALUES (?, ?)",
            (period.academicyear_id, period.period_number),
        )
        self._connection.commit()
        period.period_id = cursor.lastrowid
        return period

    def get_periods_by_academic_year(self, academic_year):
        """
        Retrieves all periods that belong to a specific academic year.

        Args:
            academic_year: The AcademicYear object.

        Returns:
            list[Period]: A list of Period objects associated with the academic year.
        """

        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT id, academicyear_id, period_number FROM periods
            WHERE academicyear_id = ?
            """,
            (academic_year.year_id,),
        )
        rows = cursor.fetchall()
        return [Period(row[0], row[1], row[2]) for row in rows]


period_repository = PeriodRepository(get_database_connection())
