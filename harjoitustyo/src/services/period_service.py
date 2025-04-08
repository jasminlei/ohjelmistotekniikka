from entities.period import Period
from repositories.period_repository import period_repository as period_repo


class PeriodService:
    def __init__(self, period_repository):
        self._period_repository = period_repository

    def create(self, academic_year):
        for period_number in range(1, 6):
            period = Period(None, academic_year.year_id, period_number)
            self._period_repository.create(period)

    def get_periods_by_academic_year(self, academic_year):
        return self._period_repository.get_periods_by_academic_year(academic_year)


period_service = PeriodService(period_repo)
