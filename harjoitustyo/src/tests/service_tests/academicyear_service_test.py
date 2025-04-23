import unittest
from initialize_database import initialize_database
from database_connection import get_database_connection
from services.academicyear_service import AcademicYearService
from services.course_service import CourseService
from services.period_service import PeriodService
from repositories.academicyear_repository import AcademicYearRepository
from repositories.course_repository import CourseRepository
from repositories.period_repository import PeriodRepository


class MockAuthenticationService:
    def __init__(self):
        self.logged_in_user_id = 1

    def get_logged_in_user_id(self):
        return self.logged_in_user_id


class TestAcademicYearService(unittest.TestCase):
    def setUp(self):
        initialize_database(test=True)
        self.connection = get_database_connection(test=True)
        self.academic_year_repository = AcademicYearRepository(self.connection)
        self.course_repository = CourseRepository(self.connection)
        self.period_repository = PeriodRepository(self.connection)

        self.auth_service = MockAuthenticationService()
        self.course_service = CourseService(self.course_repository, self.auth_service)
        self.period_service = PeriodService(self.period_repository)
        self.academicyear_service = AcademicYearService(
            self.academic_year_repository, self.course_service, self.period_service
        )

        self.test_academicyear = self.academicyear_service.create(2023, 2024)[1]

    def test_years_are_valid_method_returns_true_if_years_are_correct(self):
        result = self.academicyear_service._years_are_valid(2023, 2024)
        self.assertTrue(result[0])
        self.assertEqual(result[1], None)

    def test_years_are_valid_method_returns_false_and_error_for_invalid_format(self):
        result = self.academicyear_service._years_are_valid(23, 2024)
        self.assertFalse(result[0])
        self.assertEqual(result[1], "Vuosien on oltava muotoa YYYY (esim. 2023).")

    def test_years_are_valid_non_consecutive(self):
        result = self.academicyear_service._years_are_valid(2023, 2025)
        self.assertFalse(result[0])
        self.assertEqual(
            result[1],
            "Vuosien on oltava peräkkäisiä.",
        )

    def test_create_valid_academic_year_returns_true_and_year(self):
        success, academic_year = self.academicyear_service.create(2024, 2025)
        self.assertTrue(success)
        self.assertEqual(academic_year.start_year, 2024)
        self.assertEqual(academic_year.end_year, 2025)
        self.assertEqual(academic_year.year_id, 2)

    def test_create_invalid_academic_year_returns_false_and_error(self):
        success, error = self.academicyear_service.create("xks", "ksakd")
        self.assertFalse(success)
        self.assertEqual(error, "Vuosien on oltava muotoa YYYY (esim. 2023).")
