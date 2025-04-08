from entities.studyplan import StudyPlan
from repositories.studyplan_repository import studyplan_repository as studyplan_repo
from services.academicyear_service import academicyear_service as academicyear_serv
from services.period_service import period_service as period_serv


class StudyPlanService:
    def __init__(
        self,
        studyplan_repository,
        academicyear_service,
        period_service,
    ):
        self._studyplan_repository = studyplan_repository
        self._academic_year_service = academicyear_service
        self._period_service = period_service

    def create_studyplan(self, user_id, plan_name):
        studyplan = StudyPlan(None, plan_name, user_id)
        studyplan = self._studyplan_repository.create(studyplan)
        return studyplan

    def get_studyplans_by_user(self, user_id):
        return self._studyplan_repository.get_by_user_id(user_id)

    def add_academic_year_to_plan(self, studyplan, year_start, year_end):
        if self._academic_year_already_in_plan(studyplan, year_start, year_end):
            raise ValueError(
                "Tämä akateeminen vuosi on jo lisätty opintosuunnitelmaan!"
            )

        success, academic_year_or_error = self._academic_year_service.create(
            year_start, year_end
        )

        if not success:
            return False, academic_year_or_error

        academic_year = academic_year_or_error
        self._studyplan_repository.add_academic_year(studyplan, academic_year)
        return True, academic_year

    def _academic_year_already_in_plan(self, studyplan, year_start, year_end):
        return self._academic_year_service.year_exists_in_studyplan(
            studyplan, year_start, year_end
        )


studyplan_service = StudyPlanService(studyplan_repo, academicyear_serv, period_serv)
