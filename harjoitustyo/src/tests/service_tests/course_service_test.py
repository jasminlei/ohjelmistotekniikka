import unittest
from initialize_database import initialize_database
from database_connection import get_database_connection
from repositories.course_repository import CourseRepository
from repositories.period_repository import PeriodRepository
from services.course_service import CourseService
from services.period_service import PeriodService
from entities.year import AcademicYear


class MockAuthenticationService:
    def __init__(self):
        self.logged_in_user_id = 1

    def get_logged_in_user_id(self):
        return self.logged_in_user_id


class TestCourseService(unittest.TestCase):
    def setUp(self):
        initialize_database(test=True)
        self.connection = get_database_connection(test=True)
        self.course_repository = CourseRepository(self.connection)
        self.auth_service = MockAuthenticationService()
        self.course_service = CourseService(self.course_repository, self.auth_service)
        self.period_repository = PeriodRepository(self.connection)
        self.period_service = PeriodService(self.period_repository)

        self.course1 = self.course_service.add_course(
            "TKT111", "Kurssi 1", 5, "hyvä kurssi"
        )[1]
        self.course2 = self.course_service.add_course(
            "TKT222", "Kurssi 2", 3, "vaikea kurssi"
        )[1]

    def test_add_course_valid(self):
        success, course = self.course_service.add_course(
            "TKT000", "Testikurssi", 5, "Kiva kurssi"
        )
        self.assertTrue(success)
        self.assertEqual(course.code, "TKT000")

    def test_add_course_invalid_code_too_long(self):
        success, error_message = self.course_service.add_course(
            "12345678910", "Testikurssi", 5, "Kiva kurssi"
        )
        self.assertFalse(success)
        self.assertEqual(error_message, "Kurssikoodin merkkirajoitus on 10 merkkiä.")

    def test_add_course_invalid_ects(self):
        success, error_message = self.course_service.add_course(
            "TKT003", "Testikurssi", -1, "Kiva kurssi"
        )
        self.assertFalse(success)
        self.assertEqual(
            error_message, "Opintopisteiden on oltava positiivinen kokonaisluku."
        )

    def test_add_course_description_too_long(self):
        long_description = "a" * 251
        success, error_message = self.course_service.add_course(
            "TKT004", "Testikurssi", 5, long_description
        )
        self.assertFalse(success)
        self.assertEqual(
            error_message, "Kurssikuvauksen merkkirajoitus on 250 merkkiä."
        )

    def test_add_course_name_too_long(self):
        long_name = "a" * 151
        success, error_message = self.course_service.add_course(
            "TKT005", long_name, 5, "Kiva kurssi"
        )
        self.assertFalse(success)
        self.assertEqual(error_message, "Kurssin nimen merkkirajoitus on 150 merkkiä.")

    def test_get_courses_by_academicyear(self):
        academicyear = AcademicYear(1, 2021, 2022)
        period = self.period_service.create(academicyear)[0]
        self.course_service.add_course_to_period(period, self.course1)
        self.course_service.add_course_to_period(period, self.course2)
        courses = self.course_service.get_courses_by_academicyear(academicyear)
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0].code, "TKT111")
        self.assertEqual(courses[1].code, "TKT222")
