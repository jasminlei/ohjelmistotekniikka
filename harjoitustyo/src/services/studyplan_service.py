from entities.studyplan import StudyPlan
from repositories.studyplan_repository import studyplan_repository as studyplan_repo
from services.academicyear_service import academicyear_service as academicyear_serv
from services.period_service import period_service as period_serv
from services.course_service import course_service as course_serv


class StudyPlanService:
    """
    Manages study plans: create, add years, and get user’s plans.
    """

    def __init__(
        self, studyplan_repository, academicyear_service, period_service, course_service
    ):
        """
        Initializes the service with necessary repositories and other services.

        Args:
            studyplan_repository: Repository for saving and fetching study plans.
            academicyear_service: Service to handle academic year logic.
            period_service: Service to handle periods.
            course_service: Service to handle courses.
        """
        self._studyplan_repository = studyplan_repository
        self._academic_year_service = academicyear_service
        self._period_service = period_service
        self._course_service = course_service

    def create_studyplan(self, user_id, plan_name, goal_credits):
        """
        Creates a new study plan for a user.

        Args:
            user_id (int): ID of the user.
            plan_name (str): Name of the study plan.
            goal_credits (int): Credit target for the plan.

        Returns:
            StudyPlan: The created study plan object.
        """
        studyplan = StudyPlan(None, plan_name, user_id, goal_credits)
        studyplan = self._studyplan_repository.create(studyplan)
        return studyplan

    def get_studyplans_by_user(self, user_id):
        """
        Gets all study plans belonging to a user.

        Args:
            user_id (int): ID of the user.

        Returns:
            list[StudyPlan]: List of study plans.
        """
        return self._studyplan_repository.get_by_user_id(user_id)

    def add_academic_year_to_plan(self, studyplan, year_start, year_end):
        """
        Adds a new academic year to a study plan if it's not already there.

        Args:
            studyplan (StudyPlan): The plan to add the year to.
            year_start (int): Start year of the academic year.
            year_end (int): End year of the academic year.

        Returns:
            tuple[bool, AcademicYear | str]: (True, year) if added,
                                             (False, reason) if failed.
        """
        if self._academic_year_already_in_plan(studyplan, year_start, year_end):
            return False, "Tämä vuosi on jo lisätty opintosuunnitelmaan!"

        success, result = self._academic_year_service.create(year_start, year_end)

        if not success:
            return False, result

        academicyear = result
        self._studyplan_repository.add_academic_year(studyplan, academicyear)
        return True, academicyear

    def _academic_year_already_in_plan(self, studyplan, year_start, year_end):
        """
        Checks if the given academic year already exists in the plan.

        Args:
            studyplan (StudyPlan): The plan to check.
            year_start (int): Start year of the academic year.
            year_end (int): End year of the academic year.

        Returns:
            bool: True if the year is already in the plan, otherwise False.
        """
        return self._academic_year_service.year_exists_in_studyplan(
            studyplan, year_start, year_end
        )


studyplan_service = StudyPlanService(
    studyplan_repo, academicyear_serv, period_serv, course_serv
)
