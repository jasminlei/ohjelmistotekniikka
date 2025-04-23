from entities.period import Period
from repositories.period_repository import period_repository as period_repo


class PeriodService:
    """
    Handles logic related to periods within an academic year.
    """

    def __init__(self, period_repository):
        """
        Initializes the service with the given repository.

        Args:
            period_repository: Repository that handles period data in the database.
        """
        self._period_repository = period_repository

    def create(self, academic_year):
        """
        Creates five periods (1–5) for the given academic year.

        Args:
            academic_year (AcademicYear): The academic year to link the periods to.

        Returns:
            list[Period]: List of the created Period objects.
        """
        periods = []
        for period_number in range(1, 6):
            period = Period(None, academic_year.year_id, period_number)
            created_period = self._period_repository.create(period)
            periods.append(created_period)
        return periods

    def get_periods_by_academic_year(self, academic_year):
        """
        Fetches all periods linked to a specific academic year.

        Args:
            academic_year (AcademicYear): The academic year.

        Returns:
            list[Period]: List of Period objects for the academic year.
        """
        return self._period_repository.get_periods_by_academic_year(academic_year)


period_service = PeriodService(period_repo)
