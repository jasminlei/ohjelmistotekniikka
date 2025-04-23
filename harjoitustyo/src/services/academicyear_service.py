import re
from repositories.academicyear_repository import (
    academicyear_repository as academicyear_repo,
)
from services.course_service import course_service as course_serv
from services.period_service import period_service as period_serv


class AcademicYearService:
    """Service class for managing academic years and their related logic."""

    def __init__(self, academicyear_repository, course_service, period_service):
        """
        Initializes the AcademicYearService.

        Args:
            academicyear_repository: Repository for academic year data access.
            course_service: Service for course-related operations.
            period_service: Service for period-related operations.
        """
        self._academicyear_repository = academicyear_repository
        self._course_service = course_service
        self._period_service = period_service

    def _years_are_valid(self, start_year, end_year):
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
        """
        Creates a new academic year if the years are valid,
        and creates the associated periods for the year.

        Args:
            start_year (int): The start year.
            end_year (int): The end year.

        Returns:
            tuple[bool, object/str]: (True, academic_year) if successful,
                                       (False, error_message) if not.
        """
        valid, error_message = self._years_are_valid(start_year, end_year)

        if not valid:
            return False, error_message

        academic_year = self._academicyear_repository.create(start_year, end_year)
        self._period_service.create(academic_year)
        return True, academic_year

    def year_exists_in_studyplan(self, studyplan, start_year, end_year):
        """
        Checks whether an academic year already exists in a given study plan.

        Args:
            studyplan (StudyPlan): The study plan to check.
            start_year (int): Start year.
            end_year (int): End year.

        Returns:
            bool: True if the year exists in the plan, False otherwise.
        """
        return self._academicyear_repository.exists_in_studyplan(
            studyplan.plan_id, start_year, end_year
        )

    def get_academic_years_by_studyplan(self, studyplan):
        """
        Get all academic years linked to a given study plan.

        Args:
            studyplan (StudyPlan): The plan to get years from.

        Returns:
            list[AcademicYear]: List of academic years in the plan.
        """
        return self._academicyear_repository.find_all_from_studyplan(studyplan.plan_id)

    def delete_year(self, year_id):
        """
        Delete academic year by ID.

        Args:
            year_id (int): ID of the academic year to remove.
        """
        self._academicyear_repository.delete_by_id(year_id)


academicyear_service = AcademicYearService(academicyear_repo, course_serv, period_serv)
