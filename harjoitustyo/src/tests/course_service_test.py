import unittest
from services.course_service import CourseService


class MockCourseRepository:
    def __init__(self):
        self.courses = []

    def find_all(self):
        return self.courses

    def create(self, course):
        self.courses.append(course)
        return course


class TestCourseService(unittest.TestCase):
    def setUp(self):
        self.course_repository = MockCourseRepository()
        self.course_service = CourseService(self.course_repository)
        self.course_service.add_course("TKT111", "Kurssi 1", 5, "hyvä kurssi")
        self.course_service.add_course("TKT222", "Kurssi 2", 3, "vaikea kurssi")

    def test_add_course(self):
        course = self.course_service.add_course(
            "TKT000", "Testikurssi", 5, "Kiva kurssi"
        )
        self.assertEqual(course.code, "TKT000")
        self.assertEqual(len(self.course_repository.courses), 3)

    def test_get_all_courses(self):
        courses = self.course_service.get_all_courses()
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0].code, "TKT111")
        self.assertEqual(courses[1].code, "TKT222")
