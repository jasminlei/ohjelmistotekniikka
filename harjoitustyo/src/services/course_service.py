from datetime import datetime
from repositories.course_repository import course_repository as course_repo
from services.authentication_service import auth_service as auth_serv
from entities.course import Course


class CourseService:
    """Handles all course-related logic and operations,
    such as creating, validating, assigning, and managing courses."""

    def __init__(self, course_repository, auth_service):
        """
        Initialize the service with required dependencies.

        Args:
            course_repository: Repository for course data.
            auth_service: Authentication service to get the logged-in user.
        """

        self._course_repository = course_repository
        self._auth_service = auth_service

    def add_course(self, code, name, ects, description=""):
        """
        Create a new course for the logged-in user if inputs are valid.

        Args:
            code (str): Course code.
            name (str): Course name.
            ects (int): Credit points.
            description (str): Optional description.

        Returns:
            tuple[bool, Course|str]: (True, Course) if successful, (False, error_message) if not.
        """
        is_valid, result = self.course_is_valid(code, name, ects, description)

        if is_valid:
            user_id = self._auth_service.get_logged_in_user_id()
            course = Course(None, user_id, code, name, ects, description, False, False)
            return True, self._course_repository.create(course)

        return False, result

    def course_is_valid(self, code, name, ects, description=""):
        """
        Validate the input fields for a course.

        Returns:
            tuple[bool, str | None]: True if valid, False and message if not.
        """
        if not code or not name or not ects:
            return False, "Kurssikoodi, nimi ja opintopisteet ovat pakollisia."

        if int(ects) < 0:
            return False, "Opintopisteiden on oltava positiivinen kokonaisluku."

        if len(description) > 250:
            return False, "Kurssikuvauksen merkkirajoitus on 250 merkkiä."

        if len(name) > 150:
            return False, "Kurssin nimen merkkirajoitus on 150 merkkiä."

        if len(code) > 10:
            return False, "Kurssikoodin merkkirajoitus on 10 merkkiä."

        return True, None

    def find_by_id(self, course_id):
        """
        Find a course by its ID.

        Returns:
            Course or None: The found course, or None if not found.
        """
        return self._course_repository.find_by_id(course_id)

    def get_all_courses_by_user(self, user_id):
        """
        Get all courses for a specific user.

        Returns:
            list[Course]: List of the user's courses.
        """
        return self._course_repository.find_all_by_user(user_id)

    def add_course_to_period(self, period, course):
        """
        Link a course to a specific period.

        Returns:
            bool: True.
        """
        self._course_repository.add_to_period(period, course)
        return True

    def get_courses_by_period(self, period):
        """
        Get all courses assigned to a given period.

        Returns:
            list[Course]: List of courses in the period.
        """
        return self._course_repository.get_courses_by_period(period)

    def get_courses_by_academicyear(self, academicyear):
        """
        Get all courses in a given academic year.

        Returns:
            list[Course]: Courses assigned to the academic year.
        """
        return self._course_repository.get_courses_by_academicyear(academicyear)

    def get_courses_by_studyplan(self, studyplan):
        """
        Get all courses assigned to a specific study plan.

        Returns:
            list[Course]: Courses in the study plan.
        """
        return self._course_repository.get_courses_by_studyplan(studyplan)

    def remove_course_from_period(self, period, course):
        """
        Remove a course from a specific period.

        Returns:
            bool: True if the removal succeeded.
        """
        return self._course_repository.remove_from_period(period, course)

    def mark_as_completed(self, course, grade, date):
        """
        Mark a course as completed with a grade and completion date.

        Args:
            course (Course): The course to update.
            grade (int): The grade achieved.
            date (str): Completion date (format YYYY-MM-DD).

        Returns:
            tuple[bool, str | None]: True if valid, False and error message otherwise.
        """
        if not self._date_is_valid(date):
            return False, "Päivämäärän on oltava muodossa YYYY-MM-DD."
        return True, self._course_repository.mark_completed(course, grade, date)

    def _date_is_valid(self, date_str):
        """
        Check if date string matches YYYY-MM-DD format.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def delete_course(self, course):
        """
        Delete a course from the system.

        Args:
            course (Course): The course to delete.

        Returns:
            bool: True if successfully deleted, False otherwise.
        """
        if not course or not hasattr(course, "course_id"):
            return False
        self._course_repository.delete(course.course_id)
        return True

    def get_course_timing(self, course):
        """
        Return the timing details of a course including studyplan, academic year and period.

        Args:
            course (Course): The course to look up.

        Returns:
            list[dict]: List of timing details or empty list if not found.
        """
        data = self._course_repository.get_course_timing(course)

        if not data:
            return []

        course_details = []
        for info in data:
            course_details.append(
                {
                    "studyplan": info["studyplan"],
                    "period": info["period"],
                    "academicyear": info["academicyear"],
                }
            )

        return course_details


course_service = CourseService(course_repo, auth_serv)
