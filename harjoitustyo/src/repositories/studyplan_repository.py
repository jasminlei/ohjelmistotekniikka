from database_connection import get_database_connection
from entities.studyplan import StudyPlan


class StudyPlanRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, studyplan):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO studyplans (plan_name, user_id) VALUES (?, ?)",
            (studyplan.plan_name, studyplan.user_id),
        )
        self._connection.commit()
        studyplan.plan_id = cursor.lastrowid
        self._connection.commit()
        return studyplan

    def add_academic_year(self, studyplan, academicyear):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO studyplan_academicyear (studyplan_id, academicyear_id) VALUES (?, ?)",
            (studyplan.plan_id, academicyear.year_id),
        )
        self._connection.commit()
        return True

    def get_by_user_id(self, user_id):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, plan_name FROM studyplans WHERE user_id = ?",
            (user_id,),
        )
        rows = cursor.fetchall()

        studyplans = []
        for row in rows:
            studyplans.append(StudyPlan(row["id"], row["plan_name"], user_id))

        return studyplans


studyplan_repository = StudyPlanRepository(get_database_connection())
