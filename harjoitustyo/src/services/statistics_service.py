from services.period_service import period_service as period_serv
from services.studyplan_service import studyplan_service as studyplan_serv
from services.course_service import course_service as course_serv


class StatisticsService:
    """
    Provides various statistics based on study plans and courses.
    Calculates totals, percentages, and averages for credits and grades.
    """

    def __init__(self, course_service, period_service, studyplan_service):
        """
        Initializes the service with course, period and studyplan services.

        Args:
            course_service: Service for handling course data.
            period_service: Service for handling period data.
            studyplan_service: Service for handling study plan data.
        """
        self._course_service = course_service
        self._period_service = period_service
        self._studyplan_service = studyplan_service

    def get_total_credits(self, studyplan):
        """
        Returns the total number of credits in a given study plan.

        Args:
            studyplan (StudyPlan): The study plan to calculate credits for.

        Returns:
            int: Total number of credits.
        """
        courses = self._course_service.get_courses_by_studyplan(studyplan)
        return sum(course.credits for course in courses)

    def get_completed_credits(self, studyplan):
        """
        Returns the number of completed credits in a study plan.

        Args:
            studyplan (StudyPlan): The study plan to calculate completed credits for.

        Returns:
            int: Number of completed credits.
        """
        courses = self._course_service.get_courses_by_studyplan(studyplan)
        return sum(course.credits for course in courses if course.is_completed)

    def get_percentage_completed(self, studyplan):
        """
        Returns how many percentages of the courses in studyplan are complete compared to the goal.

        Args:
            studyplan (StudyPlan): The study plan to check.

        Returns:
            float: Completion percentage (0–100).
        """
        completed = self.get_completed_credits(studyplan)
        goal = studyplan.goal_credits or 0
        return round((completed / goal) * 100, 2) if goal else 0

    def get_mean_grade(self, studyplan):
        """
        Calculates the average grade of completed courses in a study plan.

        Args:
            studyplan (StudyPlan): The study plan to check.

        Returns:
            float | None: Average grade, or None if no graded courses.
        """
        courses = self._course_service.get_courses_by_studyplan(studyplan)

        graded_courses = [
            course.grade
            for course in courses
            if course.is_completed and isinstance(course.grade, (int, float))
        ]

        if not graded_courses:
            return None

        return sum(graded_courses) / len(graded_courses)

    def get_courses_by_academic_year(self, academic_year):
        """
        Returns all courses assigned to the periods of a given academic year.

        Args:
            academic_year (AcademicYear): The academic year to check.

        Returns:
            list[Course]: List of courses.
        """
        periods = self._period_service.get_periods_by_academic_year(academic_year)
        courses = []
        for period in periods:
            courses.extend(self._course_service.get_courses_by_period(period))
        return courses

    def get_scheduled_credits_by_year(self, academic_year):
        """
        Returns the total number of credits planned in a given academic year.

        Args:
            academic_year (AcademicYear): The academic year to check.

        Returns:
            int: Total planned credits.
        """
        courses = self.get_courses_by_academic_year(academic_year)
        return sum(course.credits for course in courses)

    def get_completed_credits_by_year(self, academic_year):
        """
        Returns the number of credits completed in a given academic year.

        Args:
            academic_year (AcademicYear): The academic year to check.

        Returns:
            int: Number of completed credits.
        """
        courses = self.get_courses_by_academic_year(academic_year)
        return sum(course.credits for course in courses if course.is_completed)

    def get_credits_by_period(self, academic_year):
        """
        Returns the number of credits per period in a given academic year.

        Args:
            academic_year (AcademicYear): The academic year to check.

        Returns:
            list[tuple[int, int]]: List of tuples (period_number, credits).
        """
        periods = self._period_service.get_periods_by_academic_year(academic_year)
        data = []

        for period in periods:
            courses = self._course_service.get_courses_by_period(period)
            credits = sum(course.credits for course in courses)
            data.append((period.period_number, credits))

        return data


statistics_service = StatisticsService(course_serv, period_serv, studyplan_serv)
