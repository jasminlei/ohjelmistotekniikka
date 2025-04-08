import unittest
from services.period_service import PeriodService
from entities.year import AcademicYear
from entities.period import Period


class MockPeriodRepository:
    def __init__(self):
        self.created_periods = []
        self.periods_with_academicyears = [
            Period(1, 1, 1),
            Period(2, 1, 2),
            Period(3, 2, 1),
        ]

    def create(self, period):
        self.created_periods.append(period)
        period.period_id = len(self.created_periods)
        return period

    def get_periods_by_academic_year(self, academic_year):
        return [
            period
            for period in self.periods_with_academicyears
            if period.academicyear_id == academic_year.year_id
        ]


class TestPeriodService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MockPeriodRepository()
        self.period_service = PeriodService(self.mock_repo)

    def test_create_creates_five_periods(self):
        academic_year = AcademicYear(1, 2023, 2024)
        self.period_service.create(academic_year)

        self.assertEqual(len(self.mock_repo.created_periods), 5)

        for i, period in enumerate(self.mock_repo.created_periods, start=1):
            self.assertEqual(period.academicyear_id, academic_year.year_id)
            self.assertEqual(period.period_number, i)

    def test_get_periods_by_academic_year_returns_correct_periods(self):
        year = AcademicYear(1, 2023, 2024)

        result = self.period_service.get_periods_by_academic_year(year)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].period_number, 1)
        self.assertEqual(result[1].period_number, 2)
        for period in result:
            self.assertEqual(period.academicyear_id, 1)
