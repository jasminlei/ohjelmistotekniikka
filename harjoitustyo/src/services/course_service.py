from repositories.course_repository import course_repository
from entities.course import Course


class CourseService:
    def __init__(self, course_repository):
        self._course_repository = course_repository

    def add_course(self, code, name, credits, description=""):
        course = Course(None, code, name, credits, description, False, False)
        return self._course_repository.create(course)

    def get_all_courses(self):
        return self._course_repository.find_all()


course_service = CourseService(course_repository)
