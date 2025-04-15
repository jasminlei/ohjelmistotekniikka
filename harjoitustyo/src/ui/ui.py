from ui.start_view import StartView
from ui.register_view import RegisterView
from ui.login_view import LoginView
from ui.add_course_view import AddCourseView
from ui.list_courses_view import ListCoursesView
from ui.add_studyplan_view import AddStudyPlanView
from ui.studyplans_view import StudyPlansView


class UI:
    def __init__(
        self,
        root,
        user_service,
        auth_service,
        course_service,
        studyplan_service,
        academicyear_service,
        period_service,
    ):
        self._root = root
        self._user_service = user_service
        self._auth_service = auth_service
        self._course_service = course_service
        self._studyplan_service = studyplan_service
        self._academicyear_service = academicyear_service
        self._period_service = period_service
        self._current_view = None
        self._logged_user = self._auth_service.get_logged_in_user_id()

    def start(self):
        self._show_start_view()

    def _hide_current_view(self):
        if self._current_view:
            for widget in self._current_view.winfo_children():
                widget.destroy()
            self._current_view.destroy()
        self._current_view = None

    def _show_start_view(self):
        self._hide_current_view()
        params = {
            "root": self._root,
            "auth_service": self._auth_service,
            "handle_register": self._handle_register,
            "handle_login": self._handle_login,
            "handle_logout": self._handle_logout,
            "handle_add_course": self._handle_add_course,
            "handle_list_courses": self._handle_list_courses,
            "handle_plan_courses": self._handle_plan_courses,
            "handle_view_stats": self._handle_view_stats,
            "handle_view_studyplans": self._handle_view_studyplans,
        }

        if self._auth_service.get_logged_in_user():
            self._logged_user = self._auth_service.get_logged_in_user_id()

        self._current_view = StartView(**params)
        self._current_view.pack()

    def _handle_register(self):
        self._show_register_view()

    def _handle_login(self):
        self._show_login_view()

    def _handle_logout(self):
        self._auth_service.log_out()
        self._show_start_view()

    def _handle_add_course(self):
        self._hide_current_view()
        self._current_view = AddCourseView(
            self._root, self._course_service, self._show_start_view
        )
        self._current_view.pack()

    def _handle_list_courses(self):
        self._hide_current_view()
        self._current_view = ListCoursesView(
            self._root, self._course_service, self._logged_user, self._show_start_view
        )
        self._current_view.pack()

    def _handle_plan_courses(self):
        self._hide_current_view()
        self._current_view = AddStudyPlanView(
            self._root,
            self._studyplan_service,
            self._logged_user,
            self._show_start_view,
        )
        self._current_view.pack()

    def _handle_view_studyplans(self):
        self._hide_current_view()
        self._current_view = StudyPlansView(
            self._root,
            self._studyplan_service,
            self._academicyear_service,
            self._course_service,
            self._period_service,
            self._logged_user,
            self._show_start_view,
        )
        self._current_view.pack()

    def _handle_view_stats(self):
        pass

    def _show_register_view(self):
        self._hide_current_view()
        self._current_view = RegisterView(
            self._root, self._user_service, self._handle_back_to_start
        )
        self._current_view.pack()

    def _show_login_view(self):
        self._hide_current_view()
        self._current_view = LoginView(
            self._root, self._auth_service, self._handle_back_to_start
        )
        self._current_view.pack()

    def _handle_back_to_start(self):
        self._show_start_view()
