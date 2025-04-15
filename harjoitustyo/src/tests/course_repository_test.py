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
        self.test_course = Course(None, 321, "TKT999", "Ohjelmistotekniikka", 5)
        self.course_repository.create(self.test_course)

    def test_create_course(self):
        course = Course(None, 123, "TKT0", "Testikurssi", 5, "Kiva kurssi")

        self.course_repository.create(course)

        self.assertIsNotNone(course.course_id)
        self.assertEqual(course.code, "TKT0")
        self.assertEqual(course.name, "Testikurssi")

    def test_find_all_returns_all_courses(self):
        course1 = Course(None, 111, "TKT300", "Kurssi 1", 5, "")
        course2 = Course(None, 333, "TKT400", "Kurssi 2", 3, "")

        self.course_repository.create(course1)
        self.course_repository.create(course2)

        courses = self.course_repository.find_all()
        self.assertEqual(len(courses), 3)
        self.assertEqual(courses[0].code, "TKT999")
        self.assertEqual(courses[1].code, "TKT300")
        self.assertEqual(courses[2].code, "TKT400")

    def test_find_all_by_user_returns_all_courses_by_user(self):
        course1 = Course(None, 123, "TKT100", "Kurssi 1", 5, "")
        course2 = Course(None, 123, "TKT200", "Kurssi 2", 3, "")
        course3 = Course(None, 456, "TKT300", "Vielä yksi kurssi", 3, "")

        self.course_repository.create(course1)
        self.course_repository.create(course2)
        self.course_repository.create(course3)

        user_courses = self.course_repository.find_all_by_user(123)

        self.assertEqual(len(user_courses), 2)
        self.assertEqual(user_courses[0].code, "TKT100")
        self.assertEqual(user_courses[1].code, "TKT200")

    def test_add_course_to_period_works(self):
        course = Course(None, 111, "TKT321", "Kurssin nimi", 5)
        added = self.course_repository.add_to_period(self.test_period, course)

        self.assertTrue(added)

    def test_get_courses_by_period_returns_all_courses_in_period(self):
        course1 = Course(None, 123, "TKT100", "Kurssi1", 5, "")
        course2 = Course(None, 123, "TKT200", "Kurssi 2", 3, "")

        self.course_repository.create(course1)
        self.course_repository.create(course2)

        self.course_repository.add_to_period(self.test_period, course1)
        self.course_repository.add_to_period(self.test_period, course2)

        period_courses = self.course_repository.get_courses_by_period(self.test_period)

        self.assertEqual(len(period_courses), 2)
        self.assertEqual(period_courses[0].code, "TKT100")
        self.assertEqual(period_courses[1].code, "TKT200")

    def test_get_courses_not_in_period(self):
        courses = self.course_repository.get_courses_not_in_period(
            self.test_period, 321
        )
        self.assertEqual(courses[0].name, "Ohjelmistotekniikka")

    def test_find_by_id_returns_correct_course(self):
        course = self.course_repository.find_by_id(1)
        self.assertEqual(course.name, "Ohjelmistotekniikka")

    def test_find_by_id_returns_none_if_not_found(self):
        self.assertIsNone(self.course_repository.find_by_id(88))

    def test_remove_from_period_removes_course_from_period(self):
        self.course_repository.add_to_period(self.test_period, self.test_course)
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
            self.test_course, 4, "2025-04-04"
        )
        updated_course = self.course_repository.find_by_id(self.test_course.course_id)
        print(updated_course)

        self.assertEqual(is_updated, True)
        self.assertEqual(updated_course.grade, 4)
        self.assertEqual(updated_course.completion_date, "2025-04-04")
        self.assertEqual(updated_course.is_completed, True)

    def test_mark_completed_with_accepted(self):
        is_updated = self.course_repository.mark_completed(
            self.test_course, "Hyväksytty", "2025-04-04"
        )
        updated_course = self.course_repository.find_by_id(self.test_course.course_id)
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
        course2 = Course(None, 123, "TKT100", "Testi toinen kurssi", 5, "")
        self.course_repository.create(course2)

        self.academicyear_repository.create(2023, 2024)
        self.period_repository.create(period1)
        self.period_repository.create(period2)
        self.course_repository.add_to_period(period1, self.test_course)
        self.course_repository.add_to_period(period2, course2)

        courses = self.course_repository.get_courses_by_academicyear(academicyear)
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0].name, "Ohjelmistotekniikka")
        self.assertEqual(courses[1].name, "Testi toinen kurssi")
