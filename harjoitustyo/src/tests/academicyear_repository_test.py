import unittest
from initialize_database import initialize_database
from database_connection import get_database_connection
from repositories.academicyear_repository import AcademicYearRepository
from repositories.studyplan_repository import StudyPlanRepository
from entities.studyplan import StudyPlan


class TestAcademicYearRepository(unittest.TestCase):
    def setUp(self):
        initialize_database(test=True)
        self.connection = get_database_connection(test=True)

        self.academicyear_repository = AcademicYearRepository(self.connection)
        self.studyplan_repository = StudyPlanRepository(self.connection)

        self.studyplan = StudyPlan(None, "Testi opintosuunnitelma", 1)
        self.studyplan_repository.create(self.studyplan)

    def test_create_academicyear(self):
        created_academicyear = self.academicyear_repository.create(2023, 2024)
        self.assertIsNotNone(created_academicyear.year_id)
        self.assertEqual(created_academicyear.start_year, 2023)
        self.assertEqual(created_academicyear.end_year, 2024)

    def test_find_all_from_studyplan(self):
        studyplan_id = self.studyplan.plan_id
        academic_year1 = self.academicyear_repository.create(2023, 2024)
        academic_year2 = self.academicyear_repository.create(2024, 2025)

        self.studyplan_repository.add_academic_year(self.studyplan, academic_year1)
        self.studyplan_repository.add_academic_year(self.studyplan, academic_year2)

        academicyears = self.academicyear_repository.find_all_from_studyplan(
            studyplan_id
        )
        self.assertEqual(len(academicyears), 2)
        self.assertEqual(academicyears[0].start_year, 2023)
        self.assertEqual(academicyears[1].start_year, 2024)

    def test_if_exists_in_studyplan_returns_true(self):
        studyplan_id = self.studyplan.plan_id
        academic_year = self.academicyear_repository.create(2022, 2023)
        self.studyplan_repository.add_academic_year(self.studyplan, academic_year)
        exists = self.academicyear_repository.exists_in_studyplan(
            studyplan_id, 2022, 2023
        )
        self.assertTrue(exists)

    def test_if_does_not_exist_returns_false(self):
        studyplan_id = self.studyplan.plan_id
        non_existing_academic_year = self.academicyear_repository.exists_in_studyplan(
            studyplan_id, 2020, 2021
        )
        self.assertFalse(non_existing_academic_year)
