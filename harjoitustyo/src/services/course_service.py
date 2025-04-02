from repositories.course_repository import course_repository
from services.authentication_service import auth_service
from entities.course import Course


class CourseService:
    def __init__(self, course_repository, auth_service):
        self._course_repository = course_repository
        self._auth_service = auth_service

    def add_course(self, code, name, credits, description=""):
        user_id = self._auth_service.get_logged_in_user_id()
        course = Course(None, user_id, code, name, credits, description, False, False)
        return self._course_repository.create(course)

    def get_all_courses(self):
        return self._course_repository.find_all()


course_service = CourseService(course_repository, auth_service)
