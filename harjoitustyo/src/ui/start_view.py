from ttkbootstrap import Frame, Label, Button


class StartView(Frame):
    def __init__(
        self,
        root,
        auth_service,
        handle_register,
        handle_login,
        handle_logout,
        handle_add_course,
        handle_list_courses,
        handle_plan_courses,
        handle_view_stats,
        handle_view_studyplans,
    ):
        super().__init__(root)

        self.auth_service = auth_service
        self.handle_register = handle_register
        self.handle_login = handle_login
        self.handle_logout = handle_logout
        self.handle_add_course = handle_add_course
        self.handle_list_courses = handle_list_courses
        self.handle_plan_courses = handle_plan_courses
        self.handle_view_stats = handle_view_stats
        self.handle_view_studyplans = handle_view_studyplans

        self.create_widgets()

    def create_widgets(self):
        logged_in_user = self.auth_service.get_logged_in_user()
        if logged_in_user:
            label = Label(
                self,
                text=f"Olet kirjautunut sisään nimellä {logged_in_user.username}",
                bootstyle="secondary",
            )
            label.pack(pady=20)
            Button(
                self,
                text="Lisää yksittäinen kurssi",
                command=self.handle_add_course,
                bootstyle="success",
                width=30,
            ).pack(pady=10)
            Button(
                self,
                text="Lisää opintosuunnitelma",
                command=self.handle_plan_courses,
                bootstyle="success",
                width=30,
            ).pack(pady=10)
            Button(
                self,
                text="Listaa kurssit",
                command=self.handle_list_courses,
                bootstyle="info",
                width=30,
            ).pack(pady=10)
            Button(
                self,
                text="Tarkastele opintosuunnitelmia",
                command=self.handle_view_studyplans,
                bootstyle="info",
                width=30,
            ).pack(pady=10)
            Button(
                self,
                text="Tilastot",
                command=self.handle_view_stats,
                bootstyle="info",
                width=30,
            ).pack(pady=10)
            Button(
                self,
                text="Kirjaudu ulos",
                command=self.handle_logout,
                bootstyle="danger",
                width=30,
            ).pack(pady=10)
        else:
            label = Label(self, text="Tervetuloa!", bootstyle="secondary")
            label.pack(pady=20)
            Button(
                self,
                text="Rekisteröidy",
                command=self.handle_register,
                bootstyle="success",
                width=30,
            ).pack(pady=10)
            Button(
                self,
                text="Kirjaudu sisään",
                command=self.handle_login,
                bootstyle="info",
                width=30,
            ).pack(pady=10)
