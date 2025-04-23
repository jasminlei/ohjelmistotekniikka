import unittest
from entities.course import Course
from entities.period import Period
from entities.year import AcademicYear
from initialize_database import initialize_database
from database_connection import get_database_connection
from repositories.course_repository import CourseRepository
from repositories.period_repository import PeriodRepository
from repositories.academicyear_repository import AcademicYearRepository


class TestCourseRepository(unittest.TestCase):
    def setUp(self):
        initialize_database(test=True)
        self.connection = get_database_connection(test=True)
        self.course_repository = CourseRepository(self.connection)
        self.period_repository = PeriodRepository(self.connection)
        self.academicyear_repository = AcademicYearRepository(self.connection)

        self.test_period = Period(1, 1, 1)
        self.course1 = Course(None, 111, "TKT300", "Kurssi 1", 5, "")
        self.course2 = Course(None, 333, "TKT400", "Kurssi 2", 3, "")
        self.course3 = Course(None, 111, "TKT500", "Kurssi 3", 5, "")

        self.course_repository.create(self.course1)
        self.course_repository.create(self.course2)
        self.course_repository.create(self.course3)

    def test_create_course(self):
        course = Course(None, 123, "TKT0", "Testikurssi", 5, "Kiva kurssi")

        self.course_repository.create(course)

        self.assertIsNotNone(course.course_id)
        self.assertEqual(course.code, "TKT0")
        self.assertEqual(course.name, "Testikurssi")

    def test_find_all_by_user_returns_all_courses_by_user(self):
        user_courses = self.course_repository.find_all_by_user(111)

        self.assertEqual(len(user_courses), 2)
        self.assertEqual(user_courses[0].code, "TKT300")
        self.assertEqual(user_courses[1].code, "TKT500")

    def test_add_course_to_period_works(self):
        added = self.course_repository.add_to_period(self.test_period, self.course1)

        self.assertTrue(added)

    def test_get_courses_by_period_returns_all_courses_in_period(self):
        self.course_repository.add_to_period(self.test_period, self.course1)
        self.course_repository.add_to_period(self.test_period, self.course2)

        period_courses = self.course_repository.get_courses_by_period(self.test_period)

        self.assertEqual(len(period_courses), 2)
        self.assertEqual(period_courses[0].code, "TKT300")
        self.assertEqual(period_courses[1].code, "TKT400")

    def test_find_by_id_returns_correct_course(self):
        course = self.course_repository.find_by_id(1)
        self.assertEqual(course.name, "Kurssi 1")

    def test_find_by_id_returns_none_if_not_found(self):
        self.assertIsNone(self.course_repository.find_by_id(88))

    def test_remove_from_period_removes_course_from_period(self):
        self.course_repository.add_to_period(self.test_period, self.course1)
        courses_in_period = self.course_repository.get_courses_by_period(
            self.test_period
        )
        self.course_repository.remove_from_period(
            self.test_period, courses_in_period[0]
        )
        courses_in_period = self.course_repository.get_courses_by_period(
            self.test_period
        )

        self.assertEqual(len(courses_in_period), 0)

    def test_mark_completed_with_grade(self):
        is_updated = self.course_repository.mark_completed(
            self.course1, 4, "2025-04-04"
        )
        updated_course = self.course_repository.find_by_id(self.course1.course_id)

        self.assertEqual(is_updated, True)
        self.assertEqual(updated_course.grade, 4)
        self.assertEqual(updated_course.completion_date, "2025-04-04")
        self.assertEqual(updated_course.is_completed, True)

    def test_mark_completed_with_accepted(self):
        is_updated = self.course_repository.mark_completed(
            self.course1, "Hyväksytty", "2025-04-04"
        )
        updated_course = self.course_repository.find_by_id(self.course1.course_id)
        print(updated_course)

        self.assertEqual(is_updated, True)
        self.assertEqual(updated_course.grade, "Hyväksytty")
        self.assertEqual(updated_course.completion_date, "2025-04-04")
        self.assertEqual(updated_course.is_completed, True)

    def test_get_courses_by_acaedemic_year_returns_empty_list(self):
        academicyear = AcademicYear(1, 2023, 2024)
        courses = self.course_repository.get_courses_by_academicyear(academicyear)
        self.assertEqual(len(courses), 0)

    def test_get_courses_by_acaedemic_year_returns_correct_courses(self):
        academicyear = AcademicYear(1, 2023, 2024)
        period1 = Period(2, 1, 1)
        period2 = Period(2, 1, 2)

        self.academicyear_repository.create(2023, 2024)
        self.period_repository.create(period1)
        self.period_repository.create(period2)
        self.course_repository.add_to_period(period1, self.course1)
        self.course_repository.add_to_period(period2, self.course2)

        courses = self.course_repository.get_courses_by_academicyear(academicyear)
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0].name, "Kurssi 1")
        self.assertEqual(courses[1].name, "Kurssi 2")
