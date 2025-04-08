import unittest
from services.studyplan_service import StudyPlanService
from entities.year import AcademicYear
from entities.period import Period


class MockStudyPlanRepository:
    def __init__(self):
        self.studyplans = []
        self.next_id = 1
        self.academicyears_studyplans = []

    def create(self, study_plan):
        study_plan.plan_id = self.next_id
        self.next_id += 1
        self.studyplans.append(study_plan)
        return study_plan

    def add_academic_year(self, studyplan, academicyear):
        self.academicyears_studyplans.append((studyplan.plan_id, academicyear.year_id))
        return True

    def get_by_user_id(self, user_id):
        return [sp for sp in self.studyplans if sp.user_id == user_id]


class MockAcademicYearRepository:
    def __init__(self):
        self.academic_years = []
        self.next_id = 1

    def create(self, start_year, end_year):
        academic_year = AcademicYear(self.next_id, start_year, end_year)
        self.next_id += 1
        self.academic_years.append(academic_year)
        return academic_year

    def exists_in_studyplan(self, plan_id, start_year, end_year):
        for ay in self.academic_years:
            if ay.start_year == start_year and ay.end_year == end_year:
                return True
        return False

    def find_all_from_studyplan(self, studyplan_id):
        return [ay for ay in self.academic_years if ay.year_id == studyplan_id]


class MockPeriodRepository:
    def __init__(self):
        self.periods = []

    def create(self, period):
        self.periods.append(period)

    def get_periods_by_academic_year(self, academic_year):
        return [p for p in self.periods if p.academic_year_id == academic_year.year_id]


class MockPeriodService:
    def __init__(self):
        self.academicyears_periods = []

    def create(self, academic_year):
        for period_number in range(1, 6):
            period = Period(None, academic_year.year_id, period_number)
            self.academicyears_periods.append(period)

    def get_periods_by_academic_year(self, academic_year):
        return [
            period
            for period in self.academicyears_periods
            if period.academic_year_id == academic_year.year_id
        ]


class MockAcademicYearService:
    def __init__(self):
        self.created_years = []
        self.existing_years = set()

    def create(self, start_year, end_year):
        if end_year != start_year + 1:
            return False, "End year must be exactly one year after start year."
        if start_year >= end_year:
            return False, "Start year must be smaller than end year."

        year_id = len(self.created_years) + 1
        academic_year = AcademicYear(year_id, start_year, end_year)
        self.created_years.append(academic_year)
        return True, academic_year

    def year_exists_in_studyplan(self, studyplan, start_year, end_year):
        return (studyplan.plan_id, start_year, end_year) in self.existing_years

    def add_existing_year_to_plan(self, plan_id, start_year, end_year):
        self.existing_years.add((plan_id, start_year, end_year))


class TestStudyPlanService(unittest.TestCase):
    def setUp(self):
        self.mock_studyplan_repo = MockStudyPlanRepository()
        self.mock_academicyear_service = MockAcademicYearService()
        self.mock_period_service = MockPeriodService()

        self.studyplan_service = StudyPlanService(
            self.mock_studyplan_repo,
            self.mock_academicyear_service,
            self.mock_period_service,
        )

    def test_create_studyplan(self):
        studyplan = self.studyplan_service.create_studyplan(3, "Testi suunnitelma")

        self.assertEqual(studyplan.plan_name, "Testi suunnitelma")
        self.assertEqual(studyplan.user_id, 3)
        self.assertEqual(studyplan.plan_id, 1)

    def test_add_academic_year_to_plan(self):
        studyplan = self.studyplan_service.create_studyplan(
            2, "Toinen testi suunnitelma"
        )

        success, result = self.studyplan_service.add_academic_year_to_plan(
            studyplan, 2024, 2025
        )

        self.assertTrue(success)
        self.assertEqual(result.start_year, 2024)
        self.assertEqual(result.end_year, 2025)
