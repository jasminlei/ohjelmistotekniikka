import unittest
from initialize_database import initialize_database
from database_connection import get_database_connection
from repositories.studyplan_repository import StudyPlanRepository
from repositories.academicyear_repository import AcademicYearRepository
from entities.studyplan import StudyPlan


class TestStudyPlanRepository(unittest.TestCase):
    def setUp(self):
        initialize_database(test=True)
        self.connection = get_database_connection(test=True)
        self.studyplan_repository = StudyPlanRepository(self.connection)
        self.academicyear_repository = AcademicYearRepository(self.connection)

        self.test_studyplan = StudyPlan(1, "Testi", 5)
        self.studyplan_repository.create(self.test_studyplan)

    def test_create_studyplan_returns_created_studyplan(self):
        studyplan = self.studyplan_repository.create(StudyPlan(2, "Suunnitelma", 1))

        self.assertEqual(studyplan.plan_name, "Suunnitelma")

    def test_add_academic_year(self):
        academicyear = self.academicyear_repository.create(2023, 2024)
        added = self.studyplan_repository.add_academic_year(
            self.test_studyplan, academicyear
        )

        academicyear_in_plan = self.academicyear_repository.find_all_from_studyplan(
            self.test_studyplan.plan_id
        )

        self.assertEqual(added, True)
        self.assertEqual(academicyear_in_plan[0].year_id, 1)

    def test_get_by_user_id(self):
        other_plan = StudyPlan(2, "Toinen suunnitelma", 5)
        self.studyplan_repository.create(other_plan)
        plans = self.studyplan_repository.get_by_user_id(5)

        self.assertEqual(len(plans), 2)
        self.assertEqual(plans[0].plan_name, "Testi")
        self.assertEqual(plans[1].plan_name, "Toinen suunnitelma")
