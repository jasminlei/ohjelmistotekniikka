from repositories.course_repository import course_repository as course_repo
from services.authentication_service import auth_service as auth_serv
from entities.course import Course


class CourseService:
    def __init__(self, course_repository, auth_service):
        self._course_repository = course_repository
        self._auth_service = auth_service

    def add_course(self, code, name, ects, description=""):
        user_id = self._auth_service.get_logged_in_user_id()
        course = Course(None, user_id, code, name, ects, description, False, False)
        return self._course_repository.create(course)

    def get_all_courses(self):
        return self._course_repository.find_all()

    def get_all_courses_by_user(self, user_id):
        return self._course_repository.find_all_by_user(user_id)

    def get_courses_by_period(self, period):
        return self._course_repository.get_courses_by_period(period)

    def add_course_to_period(self, period, course):
        self._course_repository.add_to_period(period, course)
        return True

    def get_courses_by_academicyear(self, academicyear):
        return self._course_repository.get_courses_by_academicyear(academicyear)

    def mark_as_completed(self, course_id):
        pass


course_service = CourseService(course_repo, auth_serv)
