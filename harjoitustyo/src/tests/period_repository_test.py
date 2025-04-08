import unittest
from entities.period import Period
from entities.year import AcademicYear
from initialize_database import initialize_database
from database_connection import get_database_connection
from repositories.period_repository import PeriodRepository


class TestPeriodRepository(unittest.TestCase):
    def setUp(self):
        initialize_database(test=True)
        self.connection = get_database_connection(test=True)
        self.period_repository = PeriodRepository(self.connection)

    def test_create_period(self):
        period = Period(1, 1, 2)
        self.period_repository.create(period)
        self.assertIsNotNone(period.period_id)
        self.assertEqual(period.academicyear_id, 1)
        self.assertEqual(period.period_number, 2)

    def test_get_periods_by_academic_year(self):
        academicyear = AcademicYear(1, 2021, 2022)

        period1 = Period(None, 1, 1)
        period2 = Period(None, 1, 2)
        period3 = Period(None, 2, 1)

        self.period_repository.create(period1)
        self.period_repository.create(period2)
        self.period_repository.create(period3)

        periods = self.period_repository.get_periods_by_academic_year(academicyear)

        self.assertEqual(len(periods), 2)
        self.assertEqual(periods[0].academicyear_id, 1)
        self.assertEqual(periods[1].period_number, 2)
