import unittest
from services.academicyear_service import AcademicYearService
from entities.year import AcademicYear


class MockAcademicYearRepository:
    def __init__(self):
        self.academic_years = []
        self.studyplan_academicyear = []

    def create(self, start_year, end_year):
        academic_year = AcademicYear(len(self.academic_years) + 1, start_year, end_year)
        self.academic_years.append(academic_year)
        return academic_year

    def find_all_from_studyplan(self, studyplan_id):
        return [ay for ay in self.academic_years if studyplan_id == 1]

    def exists_in_studyplan(self, studyplan_id, start_year, end_year):
        for ay in self.academic_years:
            if (
                studyplan_id == 1
                and ay.start_year == start_year
                and ay.end_year == end_year
            ):
                return True
        return False

    def add_academic_year_to_studyplan(self, studyplan_id, academic_year):
        self.studyplan_academicyear.append(
            {"studyplan_id": studyplan_id, "academicyear_id": academic_year.year_id}
        )


class MockCourseService:
    def __init__(self):
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

    def get_courses_by_academic_year(self, academicyear):
        return [
            course
            for course in self.courses
            if course.academic_year_id == academicyear.year_id
        ]

    def get_courses_by_academicyear(self, academicyear):
        return self.get_courses_by_academic_year(academicyear)


class MockPeriodService:
    def __init__(self):
        self.created_periods = []

    def create(self, academic_year):
        for i in range(1, 6):
            self.created_periods.append(
                {"year_id": academic_year.year_id, "period_number": i}
            )


class TestAcademicYearService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MockAcademicYearRepository()
        self.course_service = MockCourseService()
        self.period_service = MockPeriodService()
        self.service = AcademicYearService(
            self.mock_repository, self.course_service, self.period_service
        )

    def test_years_are_valid_correct(self):
        result = self.service.years_are_valid(2023, 2024)
        self.assertTrue(result)

    def test_years_are_valid_invalid_format(self):
        result = self.service.years_are_valid(23, 2024)
        self.assertEqual(
            result, (False, "Years must be in the format YYYY (e.g., 2023, 2024).")
        )

    def test_years_are_valid_non_consecutive(self):
        result = self.service.years_are_valid(2023, 2025)
        self.assertEqual(
            result, (False, "End year must be exactly one year after start year.")
        )

    def test_create_valid_academic_year(self):
        success, academic_year = self.service.create(2023, 2024)
        self.assertTrue(success)
        self.assertEqual(academic_year.start_year, 2023)
        self.assertEqual(academic_year.end_year, 2024)
        self.assertEqual(academic_year.year_id, 1)
