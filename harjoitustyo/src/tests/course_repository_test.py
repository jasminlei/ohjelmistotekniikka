import unittest
from entities.course import Course
from entities.period import Period
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

    def test_create_course(self):
        course = Course(
            None, 123, "TKT0", "Testikurssi", 5, "Kiva kurssi", False, False
        )

        self.course_repository.create(course)

        self.assertIsNotNone(course.course_id)
        self.assertEqual(course.code, "TKT0")
        self.assertEqual(course.name, "Testikurssi")

    def test_find_all(self):
        course1 = Course(None, 111, "TKT300", "Kurssi 1", 5, "", False, False)
        course2 = Course(None, 333, "TKT400", "Kurssi 2", 3, "", True, False)

        self.course_repository.create(course1)
        self.course_repository.create(course2)

        courses = self.course_repository.find_all()
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0].code, "TKT300")
        self.assertEqual(courses[1].code, "TKT400")

    def test_find_all_by_user(self):
        course1 = Course(None, 123, "TKT100", "User Course 1", 5, "", False, False)
        course2 = Course(None, 123, "TKT200", "User Course 2", 3, "", True, False)
        course3 = Course(None, 456, "TKT300", "Other User Course", 3, "", True, True)

        self.course_repository.create(course1)
        self.course_repository.create(course2)
        self.course_repository.create(course3)

        user_courses = self.course_repository.find_all_by_user(123)

        self.assertEqual(len(user_courses), 2)
        self.assertEqual(user_courses[0].code, "TKT100")
        self.assertEqual(user_courses[1].code, "TKT200")

    def test_add_course_to_period_works(self):
        course = Course(None, 111, "TKT321", "Kurssin nimi", 5)
        period = Period(4, 1, 1)
        added = self.course_repository.add_to_period(period, course)

        self.assertTrue(added)

    def test_get_courses_by_period(self):
        period = Period(1, 1, 1)
        course1 = Course(None, 123, "TKT100", "Kurssi1", 5, "", False, False)
        course2 = Course(None, 123, "TKT200", "Kurssi 2", 3, "", True, False)

        self.course_repository.create(course1)
        self.course_repository.create(course2)

        self.course_repository.add_to_period(period, course1)
        self.course_repository.add_to_period(period, course2)

        period_courses = self.course_repository.get_courses_by_period(period)

        self.assertEqual(len(period_courses), 2)
        self.assertEqual(period_courses[0].code, "TKT100")
        self.assertEqual(period_courses[1].code, "TKT200")
