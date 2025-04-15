import unittest
from initialize_database import initialize_database
from database_connection import get_database_connection
from services.studyplan_service import StudyPlanService
from services.academicyear_service import AcademicYearService
from services.period_service import PeriodService
from services.course_service import CourseService
from repositories.studyplan_repository import StudyPlanRepository
from repositories.academicyear_repository import AcademicYearRepository
from repositories.course_repository import CourseRepository
from repositories.period_repository import PeriodRepository


class MockAuthenticationService:
    def __init__(self):
        self.logged_in_user_id = 1

    def get_logged_in_user_id(self):
        return self.logged_in_user_id


class TestStudyPlanService(unittest.TestCase):
    def setUp(self):
        initialize_database(test=True)
        self.connection = get_database_connection(test=True)
        self.studyplan_repository = StudyPlanRepository(self.connection)
        self.academicyear_repository = AcademicYearRepository(self.connection)
        self.period_repository = PeriodRepository(self.connection)
        self.course_repository = CourseRepository(self.connection)

        self.auth_service = MockAuthenticationService()
        self.period_service = PeriodService(self.period_repository)
        self.academicyear_service = AcademicYearService(
            self.academicyear_repository, None, self.period_service
        )
        self.studyplan_service = StudyPlanService(
            self.studyplan_repository, self.academicyear_service, self.period_service
        )

        self.course_service = CourseService(self.course_repository, self.auth_service)

        self.test_studyplan = self.studyplan_service.create_studyplan(1, "Suunnitelma")
        success, self.test_academicyear = (
            self.studyplan_service.add_academic_year_to_plan(
                self.test_studyplan, 2024, 2025
            )
        )
        self.test_periods = self.period_service.get_periods_by_academic_year(
            self.test_academicyear
        )

    def test_create_studyplan(self):
        studyplan = self.studyplan_service.create_studyplan(3, "Testi suunnitelma")

        self.assertEqual(studyplan.plan_name, "Testi suunnitelma")
        self.assertEqual(studyplan.user_id, 3)
        self.assertEqual(studyplan.plan_id, 2)

    def test_add_academic_year_to_plan(self):
        studyplan = self.studyplan_service.create_studyplan(
            2, "Toinen testi suunnitelma"
        )

        success, result = self.studyplan_service.add_academic_year_to_plan(
            studyplan, 2024, 2025
        )

        self.assertTrue(success)
        self.assertEqual(result.start_year, 2024)
        self.assertEqual(result.end_year, 2025)

    def test_get_all_credits_returns_correct_number_one_academic_year(self):
        success, course1 = self.course_service.add_course("TKT1", "Nimi1", 5)
        self.assertTrue(success)
        success, course2 = self.course_service.add_course("TKT2", "Nimi2", 5)
        self.assertTrue(success)
        success, course3 = self.course_service.add_course("TKT3", "Nimi3", 5)
        self.assertTrue(success)

        self.course_service.add_course_to_period(self.test_periods[0], course1)
        self.course_service.add_course_to_period(self.test_periods[0], course2)
        self.course_service.add_course_to_period(self.test_periods[0], course3)

        credits = self.studyplan_service.get_total_credits(self.test_studyplan)
        self.assertEqual(credits, 15)

    def test_get_all_credits_returns_correct_number_two_academic_years(self):
        success, other_academicyear = self.studyplan_service.add_academic_year_to_plan(
            self.test_studyplan, 2025, 2026
        )
        self.assertTrue(success)

        periods = self.period_service.get_periods_by_academic_year(other_academicyear)

        success, course1 = self.course_service.add_course("TKT1", "Nimi1", 5)
        self.assertTrue(success)
        success, course2 = self.course_service.add_course("TKT2", "Nimi2", 5)
        self.assertTrue(success)

        self.course_service.add_course_to_period(self.test_periods[0], course1)
        self.course_service.add_course_to_period(self.test_periods[0], course2)

        success, course3 = self.course_service.add_course("TKT3", "Nimi3", 3)
        self.assertTrue(success)
        success, course4 = self.course_service.add_course("TKT4", "Nimi4", 5)
        self.assertTrue(success)

        self.course_service.add_course_to_period(periods[0], course3)
        self.course_service.add_course_to_period(periods[0], course4)

        credits = self.studyplan_service.get_total_credits(self.test_studyplan)
        self.assertEqual(credits, 18)
