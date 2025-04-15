import unittest
from services.course_service import CourseService
from entities.year import AcademicYear


class MockAuthenticationService:
    def __init__(self):
        self.logged_in_user_id = 1

    def get_logged_in_user_id(self):
        return self.logged_in_user_id


class MockCourseRepository:
    def __init__(self):
        self.courses = []
        self.course_periods = [
            (1, 1),
            (2, 1),
            (3, 2),
        ]
        self.next_course_id = 1

    def find_all(self):
        return self.courses

    def create(self, course):
        course.course_id = self.next_course_id
        self.next_course_id += 1
        self.courses.append(course)
        return course

    def get_courses_by_academicyear(self, academicyear):
        courses_for_year = []
        for i in range(len(self.courses)):
            if self.course_periods[i][1] == academicyear.year_id:
                courses_for_year.append(self.courses[i])
        return courses_for_year

    def mark_as_completed(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                course.is_completed = True
                return True
        return False


class TestCourseService(unittest.TestCase):
    def setUp(self):
        self.auth_service = MockAuthenticationService()
        self.course_repository = MockCourseRepository()
        self.course_service = CourseService(self.course_repository, self.auth_service)
        self.course_service.add_course("TKT111", "Kurssi 1", 5, "hyvä kurssi")
        self.course_service.add_course("TKT222", "Kurssi 2", 3, "vaikea kurssi")

    def test_add_course_valid(self):
        success, course_or_error = self.course_service.add_course(
            "TKT000", "Testikurssi", 5, "Kiva kurssi"
        )
        self.assertTrue(success)
        self.assertEqual(course_or_error.code, "TKT000")
        self.assertEqual(len(self.course_repository.courses), 3)

    def test_add_course_invalid_code(self):
        success, error_message = self.course_service.add_course(
            "", "Testikurssi", 5, "Kiva kurssi"
        )
        self.assertFalse(success)
        self.assertEqual(
            error_message, "Kurssikoodi, nimi ja opintopisteet ovat pakollisia."
        )

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

    def test_get_all_courses(self):
        courses = self.course_service.get_all_courses()
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0].code, "TKT111")
        self.assertEqual(courses[1].code, "TKT222")

    def test_get_courses_by_academicyear(self):
        academicyear = AcademicYear(1, 2021, 2022)
        courses = self.course_service.get_courses_by_academicyear(academicyear)
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0].code, "TKT111")
        self.assertEqual(courses[1].code, "TKT222")
