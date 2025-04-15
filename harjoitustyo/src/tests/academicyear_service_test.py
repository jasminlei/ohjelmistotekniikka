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

    def test_years_are_valid_correct(self):
        result = self.academicyear_service.years_are_valid(2023, 2024)
        self.assertTrue(result[0])
        self.assertEqual(result[1], None)

    def test_years_are_valid_invalid_format(self):
        result = self.academicyear_service.years_are_valid(23, 2024)
        self.assertFalse(result[0])
        self.assertEqual(result[1], "Vuosien on oltava muotoa YYYY (esim. 2023).")

    def test_years_are_valid_non_consecutive(self):
        result = self.academicyear_service.years_are_valid(2023, 2025)
        self.assertFalse(result[0])
        self.assertEqual(
            result[1],
            "Vuosien on oltava peräkkäisiä.",
        )

    def test_create_valid_academic_year(self):
        success, academic_year = self.academicyear_service.create(2023, 2024)
        self.assertTrue(success)
        self.assertEqual(academic_year.start_year, 2023)
        self.assertEqual(academic_year.end_year, 2024)
        self.assertEqual(academic_year.year_id, 1)

    def test_get_total_credits_returns_correct_value(self):
        success, academicyear = self.academicyear_service.create(2023, 2024)
        self.assertTrue(success)

        periods = self.period_service.get_periods_by_academic_year(academicyear)
        self.assertGreater(len(periods), 0)

        course1 = self.course_service.add_course("TKT1", "Nimi1", 5)[1]
        course2 = self.course_service.add_course("TKT2", "Nimi2", 5)[1]
        course3 = self.course_service.add_course("TKT3", "Nimi3", 5)[1]

        self.course_service.add_course_to_period(periods[0], course1)
        self.course_service.add_course_to_period(periods[0], course2)
        self.course_service.add_course_to_period(periods[0], course3)

        total_credits = self.academicyear_service.get_total_credits(academicyear)
        self.assertEqual(total_credits, 15)

    def test_get_total_credits_returns_zero_if_no_courses(self):
        success, academicyear = self.academicyear_service.create(2023, 2024)
        self.assertTrue(success)

        total_credits = self.academicyear_service.get_total_credits(academicyear)
        self.assertEqual(total_credits, 0)

    def test_get_completed_credits_returns_correct_value(self):
        success, academicyear = self.academicyear_service.create(2023, 2024)
        self.assertTrue(success)

        periods = self.period_service.get_periods_by_academic_year(academicyear)
        self.assertGreater(len(periods), 0)

        course1 = self.course_service.add_course("TKT1", "Nimi1", 5)[1]
        course2 = self.course_service.add_course("TKT2", "Nimi2", 5)[1]
        course3 = self.course_service.add_course("TKT3", "Nimi3", 5)[1]

        self.course_service.add_course_to_period(periods[0], course1)
        self.course_service.add_course_to_period(periods[0], course2)
        self.course_service.add_course_to_period(periods[0], course3)

        self.course_service.mark_as_completed(course1, 5, "2025-01-01")
        self.course_service.mark_as_completed(course2, 4, "2025-01-02")

        total_credits = self.academicyear_service.get_completed_credits(academicyear)
        self.assertEqual(total_credits, 10)
