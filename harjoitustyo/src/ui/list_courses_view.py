from ttkbootstrap import Frame, Label, Button
from tkinter import ttk


class ListCoursesView(Frame):
    def __init__(self, root, course_service, logged_user, handle_back):
        super().__init__(root)
        self._course_service = course_service
        self._logged_user = logged_user
        self._handle_back = handle_back
        self._create_widgets()

    def _create_widgets(self):
        label = Label(self, text="Kurssit", font=("Arial", 16), bootstyle="primary")
        label.pack(pady=20)

        self.treeview = ttk.Treeview(
            self, columns=("Code", "Name", "Credits", "Status"), show="headings"
        )

        self.treeview.heading("Code", text="Koodi", anchor="w")
        self.treeview.heading("Name", text="Kurssi", anchor="w")
        self.treeview.heading("Credits", text="Opintopisteet", anchor="w")
        self.treeview.heading("Status", text="Tila", anchor="w")

        self.treeview.column("Code", width=100)
        self.treeview.column("Name", width=150)
        self.treeview.column("Credits", width=100)
        self.treeview.column("Status", width=120)

        self._populate_courses()

        self.treeview.bind("<ButtonRelease-1>", self._on_course_click)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.treeview.pack(pady=20)

        self.course_details_label = Label(
            self, text="", font=("Arial", 12), justify="left"
        )
        self.course_details_label.pack(pady=10)

        self.actions_frame = Frame(self)
        self.actions_frame.pack(pady=10)

        back_button = Button(
            self, text="Takaisin", bootstyle="danger", command=self._handle_back
        )
        back_button.pack(pady=10)

    def _populate_courses(self):
        courses = self._course_service.get_all_courses_by_user(self._logged_user)
        for course in courses:
            completed = "Suoritettu" if course.is_completed else "Ei suoritettu"
            self.treeview.insert(
                "",
                "end",
                values=(
                    course.code,
                    course.name,
                    course.credits,
                    completed,
                ),
            )

    def _on_course_click(self, event):
        selected_items = self.treeview.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        course_data = self.treeview.item(selected_item, "values")

        if not course_data:
            return

        course_code = course_data[0]

        user_courses = self._course_service.get_all_courses_by_user(self._logged_user)
        course = next((c for c in user_courses if c.code == course_code), None)

        if course:
            self._show_course_details(course)

    def _show_course_details(self, course):
        self.selected_course = course

        details_message = f"""
        Koodi: {course.code}
        Nimi: {course.name}
        Opintopisteet: {course.credits} op
        Kuvaus: {course.description}
        """
        self.course_details_label.config(text=details_message)

        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        if not course.is_completed:
            self.mark_completed_button = Button(
                self.actions_frame,
                text="Merkitse suoritetuksi",
                bootstyle="success",
                command=self._mark_completed,
            )
            self.mark_completed_button.pack(pady=5)

    def _mark_completed(self):
        pass
