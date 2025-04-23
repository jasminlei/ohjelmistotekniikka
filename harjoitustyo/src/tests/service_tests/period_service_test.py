import unittest
from initialize_database import initialize_database
from database_connection import get_database_connection
from services.period_service import PeriodService
from repositories.period_repository import PeriodRepository
from entities.year import AcademicYear


class TestPeriodService(unittest.TestCase):
    def setUp(self):
        initialize_database(test=True)
        self.connection = get_database_connection(test=True)
        self.period_repository = PeriodRepository(self.connection)
        self.period_service = PeriodService(self.period_repository)

        self.test_academicyear = AcademicYear(1, 2023, 2024)
        self.test_periods = self.period_service.create(self.test_academicyear)

    def test_create_creates_five_periods(self):
        year = AcademicYear(2, 2024, 2025)
        periods = self.period_service.create(year)

        self.assertEqual(len(periods), 5)

    def test_create_creates_periods_with_correct_period_numbers(self):
        period_numbers = [period.period_number for period in self.test_periods]

        self.assertCountEqual(period_numbers, [1, 2, 3, 4, 5])

    def test_get_periods_by_academic_year_returns_correct_periods(self):
        result = self.period_service.get_periods_by_academic_year(
            self.test_academicyear
        )

        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].period_number, 1)
        self.assertEqual(result[1].period_number, 2)
        for period in result:
            self.assertEqual(period.academicyear_id, 1)
