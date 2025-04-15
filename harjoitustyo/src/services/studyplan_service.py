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
            return False, "Tämä vuosi on jo lisätty opintosuunnitelmaan!"

        success, result = self._academic_year_service.create(year_start, year_end)

        if not success:
            return False, result

        academicyear = result
        self._studyplan_repository.add_academic_year(studyplan, academicyear)
        return True, academicyear

    def _academic_year_already_in_plan(self, studyplan, year_start, year_end):
        return self._academic_year_service.year_exists_in_studyplan(
            studyplan, year_start, year_end
        )

    def get_total_credits(self, studyplan):
        academicyears = self._academic_year_service.get_academic_years_by_studyplan(
            studyplan
        )
        credits = 0
        for year in academicyears:
            credits += self._academic_year_service.get_total_credits(year)
        return credits

    def get_completed_credits(self, studyplan):
        pass

    def get_mean_grade(self, studyplan):
        pass


studyplan_service = StudyPlanService(studyplan_repo, academicyear_serv, period_serv)
