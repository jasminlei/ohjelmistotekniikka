from database_connection import get_database_connection
from entities.studyplan import StudyPlan


class StudyPlanRepository:
    """Repository class for managing studyplan-related database operations."""

    def __init__(self, connection):
        """
        Initializes the repository with a database connection.

        Args:
            connection: A SQLite database connection object.
        """
        self._connection = connection

    def create(self, studyplan):
        """
        Adds a new study plan into the database.

        Args:
            studyplan (StudyPlan): The StudyPlan object to insert.

        Returns:
            StudyPlan: The inserted StudyPlan object with the generated ID.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO studyplans (plan_name, user_id, goal_credits) VALUES (?, ?, ?)",
            (studyplan.plan_name, studyplan.user_id, studyplan.goal_credits),
        )
        self._connection.commit()
        studyplan.plan_id = cursor.lastrowid
        self._connection.commit()
        return studyplan

    def add_academic_year(self, studyplan, academicyear):
        """
        Associates an academic year with a studyplan.

        Args:
            studyplan (StudyPlan): The studyplan object.
            academicyear (AcademicYear): The academic year to associate.

        Returns:
            bool: True if the operation was successful.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO studyplan_academicyear (studyplan_id, academicyear_id) VALUES (?, ?)",
            (studyplan.plan_id, academicyear.year_id),
        )
        self._connection.commit()
        return True

    def get_by_user_id(self, user_id):
        """
        Retrieves all study plans associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list[StudyPlan]: A list of StudyPlan objects for the user.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM studyplans WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()

        return [
            StudyPlan(
                plan_id=row["id"],
                plan_name=row["plan_name"],
                user_id=row["user_id"],
                goal_credits=row["goal_credits"],
            )
            for row in rows
        ]


studyplan_repository = StudyPlanRepository(get_database_connection())
