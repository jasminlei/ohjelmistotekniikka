import unittest
from entities.course import Course
from initialize_database import initialize_database
from database_connection import get_database_connection
from repositories.course_repository import CourseRepository


class TestCourseRepository(unittest.TestCase):
    def setUp(self):
        initialize_database(test=True)
        self.connection = get_database_connection(test=True)
        self.course_repository = CourseRepository(self.connection)

    def test_create_course(self):
        course = Course(None, "TKT0", "Testikurssi", 5, "Kiva kurssi", False, False)

        self.course_repository.create(course)

        self.assertIsNotNone(course.course_id)
        self.assertEqual(course.code, "TKT0")
        self.assertEqual(course.name, "Testikurssi")

    def test_find_all(self):
        course1 = Course(None, "TKT300", "Kurssi 1", 5, "", False, False)
        course2 = Course(None, "TKT400", "Kurssi 2", 3, "", True, False)

        self.course_repository.create(course1)
        self.course_repository.create(course2)

        courses = self.course_repository.find_all()
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0].code, "TKT300")
        self.assertEqual(courses[1].code, "TKT400")
