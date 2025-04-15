from repositories.course_repository import course_repository as course_repo
from services.authentication_service import auth_service as auth_serv
from entities.course import Course


class CourseService:
    def __init__(self, course_repository, auth_service):
        self._course_repository = course_repository
        self._auth_service = auth_service

    def add_course(self, code, name, ects, description=""):
        is_valid, result = self.course_is_valid(code, name, ects, description)

        if is_valid:
            user_id = self._auth_service.get_logged_in_user_id()
            course = Course(None, user_id, code, name, ects, description, False, False)
            return True, self._course_repository.create(course)

        return False, result

    def course_is_valid(self, code, name, ects, description=""):
        if not code or not name or not ects:
            return False, "Kurssikoodi, nimi ja opintopisteet ovat pakollisia."

        if int(ects) < 0:
            return False, "Opintopisteiden on oltava positiivinen kokonaisluku."

        if len(description) > 250:
            return False, "Kurssikuvauksen merkkirajoitus on 250 merkkiä."

        if len(name) > 150:
            return False, "Kurssin nimen merkkirajoitus on 150 merkkiä."

        if len(code) > 10:
            return False, "Kurssikoodin merkkirajoitus on 10 merkkiä."

        return True, None

    def find_by_id(self, course_id):
        return self._course_repository.find_by_id(course_id)

    def get_all_courses(self):
        return self._course_repository.find_all()

    def get_all_courses_not_in_plan(self):
        pass

    def get_all_courses_by_user(self, user_id):
        return self._course_repository.find_all_by_user(user_id)

    def add_course_to_period(self, period, course):
        self._course_repository.add_to_period(period, course)
        return True

    def get_courses_by_period(self, period):
        return self._course_repository.get_courses_by_period(period)

    def get_courses_not_in_period(self, period, user_id):
        return self._course_repository.get_courses_not_in_period(period, user_id)

    def remove_course_from_period(self, period, course):
        return self._course_repository.remove_from_period(period, course)

    def get_courses_by_academicyear(self, academicyear):
        return self._course_repository.get_courses_by_academicyear(academicyear)

    def mark_as_completed(self, course, grade, date):
        return self._course_repository.mark_completed(course, grade, date)


course_service = CourseService(course_repo, auth_serv)
