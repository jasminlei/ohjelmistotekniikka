import re
from repositories.academicyear_repository import (
    academicyear_repository as academicyear_repo,
)
from services.course_service import course_service as course_serv
from services.period_service import period_service as period_serv


class AcademicYearService:
    def __init__(self, academicyear_repository, course_service, period_service):
        self._academicyear_repository = academicyear_repository
        self._course_service = course_service
        self._period_service = period_service

    def years_are_valid(self, start_year, end_year):
        if not re.match(r"^\d{4}$", str(start_year)) or not re.match(
            r"^\d{4}$", str(end_year)
        ):
            return False, "Vuosien on oltava muotoa YYYY (esim. 2023)."

        if end_year != start_year + 1:
            return False, "Vuosien on oltava peräkkäisiä."

        if start_year >= end_year:
            return False, "Alkuvuoden täytyy olla pienempi kuin loppuvuosi."

        return True, None

    def create(self, start_year, end_year):
        valid, error_message = self.years_are_valid(start_year, end_year)

        if not valid:
            return False, error_message

        academic_year = self._academicyear_repository.create(start_year, end_year)
        self._period_service.create(academic_year)
        return True, academic_year

    def year_exists_in_studyplan(self, studyplan, start_year, end_year):
        return self._academicyear_repository.exists_in_studyplan(
            studyplan.plan_id, start_year, end_year
        )

    def get_academic_years_by_studyplan(self, studyplan):
        return self._academicyear_repository.find_all_from_studyplan(studyplan.plan_id)

    def get_total_credits(self, academicyear):
        return self._academicyear_repository.get_total_credits(academicyear.year_id)

    def get_completed_credits(self, academicyear):
        return self._academicyear_repository.get_completed_credits(academicyear.year_id)


academicyear_service = AcademicYearService(academicyear_repo, course_serv, period_serv)
