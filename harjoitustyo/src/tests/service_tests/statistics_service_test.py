import unittest
from initialize_database import initialize_database
from database_connection import get_database_connection
from services.statistics_service import StatisticsService
from services.course_service import CourseService
from services.period_service import PeriodService
from services.academicyear_service import AcademicYearService
from services.studyplan_service import StudyPlanService
from repositories.course_repository import CourseRepository
from repositories.period_repository import PeriodRepository
from repositories.academicyear_repository import AcademicYearRepository
from repositories.studyplan_repository import StudyPlanRepository


class MockAuthenticationService:
    def __init__(self):
        self.logged_in_user_id = 1

    def get_logged_in_user_id(self):
        return self.logged_in_user_id


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        initialize_database(test=True)
        self.connection = get_database_connection(test=True)

        self.course_repository = CourseRepository(self.connection)
        self.period_repository = PeriodRepository(self.connection)
        self.academicyear_repository = AcademicYearRepository(self.connection)
        self.studyplan_repository = StudyPlanRepository(self.connection)

        self.auth_service = MockAuthenticationService()

        self.period_service = PeriodService(self.period_repository)
        self.course_service = CourseService(self.course_repository, self.auth_service)
        self.academicyear_service = AcademicYearService(
            self.academicyear_repository, None, self.period_service
        )
        self.studyplan_service = StudyPlanService(
            self.studyplan_repository,
            self.academicyear_service,
            self.period_service,
            self.course_service,
        )

        self.statistics_service = StatisticsService(
            self.course_service,
            self.period_service,
            self.studyplan_service,
        )

        self.test_course1 = self.course_service.add_course("TKT1", "Nimi1", 5)[1]
        self.test_course2 = self.course_service.add_course("TKT2", "Nimi2", 5)[1]
        self.test_course3 = self.course_service.add_course("TKT3", "Nimi3", 3)[1]
        self.test_course4 = self.course_service.add_course("TKT4", "Nimi4", 3)[1]

        self.test_studyplan = self.studyplan_service.create_studyplan(
            1, "Testisuunnitelma", 180
        )

        self.test_academicyear = self.studyplan_service.add_academic_year_to_plan(
            self.test_studyplan, 2025, 2026
        )[1]

        self.test_periods = self.period_service.get_periods_by_academic_year(
            self.test_academicyear
        )

        self.course_service.add_course_to_period(
            self.test_periods[0], self.test_course1
        )
        self.course_service.add_course_to_period(
            self.test_periods[1], self.test_course2
        )

    def test_get_total_credits(self):
        total_credits = self.statistics_service.get_total_credits(self.test_studyplan)
        self.assertEqual(total_credits, 10)

    def test_get_completed_credits(self):
        self.course_service.mark_as_completed(self.test_course1, 5, "2025-01-01")

        completed_credits = self.statistics_service.get_completed_credits(
            self.test_studyplan
        )
        self.assertEqual(completed_credits, 5)

    def test_get_percentage_completed(self):
        self.course_service.mark_as_completed(self.test_course2, 5, "2025-01-01")

        percentage = self.statistics_service.get_percentage_completed(
            self.test_studyplan
        )
        self.assertEqual(percentage, 2.78)

    def test_get_mean_grade(self):
        self.course_service.mark_as_completed(self.test_course1, 4, "2025-01-01")
        self.course_service.mark_as_completed(self.test_course2, 3, "2025-01-01")

        mean_grade = self.statistics_service.get_mean_grade(self.test_studyplan)
        self.assertEqual(mean_grade, 3.5)

    def test_get_mean_grade_retuns_none_if_no_completed_courses(self):
        mean_grade = self.statistics_service.get_mean_grade(self.test_studyplan)
        self.assertIsNone(mean_grade)

    def test_get_scheduled_credits_by_year(self):
        self.course_service.add_course_to_period(
            self.test_periods[4], self.test_course3
        )
        self.course_service.add_course_to_period(
            self.test_periods[3], self.test_course4
        )

        scheduled_credits = self.statistics_service.get_scheduled_credits_by_year(
            self.test_academicyear
        )
        self.assertEqual(scheduled_credits, 16)

    def test_get_completed_credits_by_year(self):
        self.course_service.add_course_to_period(
            self.test_periods[4], self.test_course3
        )

        self.course_service.add_course_to_period(
            self.test_periods[3], self.test_course4
        )

        self.course_service.mark_as_completed(self.test_course1, 5, "2025-01-01")
        self.course_service.mark_as_completed(self.test_course3, 5, "2025-01-01")

        completed_credits = self.statistics_service.get_completed_credits_by_year(
            self.test_academicyear
        )
        self.assertEqual(completed_credits, 8)

    def test_get_completed_credits_by_year_returns_zero_if_no_completed_courses(self):
        completed_credits = self.statistics_service.get_completed_credits_by_year(
            self.test_academicyear
        )
        self.assertEqual(completed_credits, 0)

    def test_get_credits_by_period(self):
        self.course_service.add_course_to_period(
            self.test_periods[4], self.test_course3
        )

        period_data = self.statistics_service.get_credits_by_period(
            self.test_academicyear
        )
        self.assertEqual(period_data, [(1, 5), (2, 5), (3, 0), (4, 0), (5, 3)])
