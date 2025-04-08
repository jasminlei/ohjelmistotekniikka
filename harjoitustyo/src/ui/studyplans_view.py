import tkinter as tk
import ttkbootstrap as ttk
from ui.add_course_view import AddCourseView
from ttkbootstrap import Frame, Label, Button, Entry


class StudyPlansView(Frame):
    def __init__(
        self,
        master,
        studyplan_service,
        academicyear_service,
        course_service,
        period_service,
        logged_user,
        handle_back,
    ):
        super().__init__(master)
        self.studyplan_service = studyplan_service
        self.academicyear_service = academicyear_service
        self.course_service = course_service
        self.period_service = period_service
        self.logged_user = logged_user
        self.handle_back = handle_back
        self.currently_shown_studyplan = None
        self.currently_shown_year = None

        Label(
            self, text="Lisätyt opintosuunnitelmat", font=("Helvetica Neue", 16, "bold")
        ).pack(pady=10)

        self.studyplans_frame = Frame(self)
        self.studyplans_frame.pack(pady=10)

        self.details_frame = Frame(self)
        self.years_frame = None

        self.load_studyplans()

        self.back_button = Button(
            self, text="Takaisin", bootstyle="secondary", command=self.handle_back
        )
        self.back_button.pack(pady=10, side=tk.BOTTOM)

    def load_studyplans(self):
        for widget in self.studyplans_frame.winfo_children():
            widget.destroy()

        studyplans = self.studyplan_service.get_studyplans_by_user(self.logged_user)
        if not studyplans:
            Label(
                self.studyplans_frame,
                text="Ei lisättyjä opintosuunnitelmia.",
            ).pack(pady=5)
            return

        for studyplan in studyplans:
            Button(
                self.studyplans_frame,
                text=studyplan.plan_name,
                bootstyle="warning",
                width=30,
                command=lambda sp=studyplan: self.toggle_studyplan_details(sp),
            ).pack(pady=5, padx=20, fill=tk.X)

    def toggle_studyplan_details(self, studyplan):
        if self.currently_shown_studyplan == studyplan:
            self.hide_studyplan_details()
        else:
            self.show_studyplan_details(studyplan)

    def show_studyplan_details(self, studyplan):
        self.hide_studyplan_details()

        Label(
            self.details_frame,
            text=f"Opintosuunnitelma: {studyplan.plan_name}",
            font=("Helvetica Neue", 14, "bold"),
        ).pack(pady=5)

        self.years_frame = Frame(self.details_frame)
        self.years_frame.pack(pady=10)

        self.load_academic_years(studyplan)

        Label(
            self.details_frame, text="Lisää vuosi", font=("Helvetica Neue", 12, "bold")
        ).pack(pady=5)

        entry_frame = Frame(self.details_frame)
        entry_frame.pack(pady=5)

        self.start_year_entry = Entry(entry_frame, width=4)
        self.start_year_entry.pack(side=tk.LEFT, padx=5)
        Label(entry_frame, text="-").pack(side=tk.LEFT)
        self.end_year_entry = Entry(entry_frame, width=4)
        self.end_year_entry.pack(side=tk.LEFT, padx=5)

        Button(
            entry_frame,
            text="Lisää",
            bootstyle="success",
            command=lambda: self.add_academic_year(studyplan),
        ).pack(side=tk.LEFT, padx=10)

        self.details_frame.pack(pady=10)
        self.currently_shown_studyplan = studyplan

    def hide_studyplan_details(self):
        self.details_frame.pack_forget()
        if self.years_frame:
            self.years_frame.pack_forget()
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        self.currently_shown_studyplan = None

    def add_academic_year(self, studyplan):
        start_year = self.start_year_entry.get()
        end_year = self.end_year_entry.get()

        if not (
            start_year.isdigit()
            and end_year.isdigit()
            and int(start_year) < int(end_year)
        ):
            Label(
                self.details_frame, text="Virheellinen vuosi!", foreground="red"
            ).pack()
            return

        self.studyplan_service.add_academic_year_to_plan(
            studyplan, int(start_year), int(end_year)
        )

        self.load_academic_years(studyplan)

    def load_academic_years(self, studyplan):
        for widget in self.years_frame.winfo_children():
            widget.destroy()

        academic_years = self.academicyear_service.get_academic_years_by_studyplan(
            studyplan
        )

        for year in academic_years:
            Button(
                self.years_frame,
                text=f"{year.start_year}-{year.end_year}",
                bootstyle="info",
                width=30,
                command=lambda y=year: self.toggle_year_details(y),
            ).pack(pady=5, padx=10)

    def toggle_year_details(self, academic_year):
        if self.currently_shown_year == academic_year:
            self.hide_year_details()
        else:
            self.show_year_details(academic_year)

    def show_year_details(self, academic_year):
        self.hide_year_details()

        self.year_details_frame = Frame(self.years_frame)
        self.year_details_frame.pack(pady=5, fill=tk.X)

        Label(
            self.year_details_frame,
            text=f"Akateeminen vuosi: {academic_year.start_year}-{academic_year.end_year}",
            font=("Arial", 12, "bold"),
        ).pack()

        self.load_periods(academic_year)

        self.currently_shown_year = academic_year

    def load_periods(self, academic_year):
        periods = self.period_service.get_periods_by_academic_year(academic_year)

        if not periods:
            Label(
                self.year_details_frame,
                text="Ei lisättyjä periodeja.",
            ).pack()
            return

        periods_notebook = ttk.Notebook(self.year_details_frame, width=450)
        periods_notebook.pack(pady=5, fill=tk.BOTH, expand=True)

        for period in periods:
            period_frame = Frame(periods_notebook)
            periods_notebook.add(
                period_frame,
                text=f"Periodi {period.period_number}"
                if period.period_number != 5
                else "Kesä",
            )

            courses = self.course_service.get_courses_by_period(period)

            if courses:
                for course in courses:
                    Label(
                        period_frame, text=f"• {course.name}", font=("Arial", 9)
                    ).pack(padx=5, pady=2)
            else:
                Label(
                    period_frame, text="(Ei kursseja)", font=("Arial", 9, "italic")
                ).pack(padx=5, pady=2)

            Button(
                period_frame,
                text="Lisää kurssi",
                bootstyle="success",
                command=lambda p=period: self.show_add_course_view(p),
            ).pack(pady=5)

    def show_add_course_view(self, period):
        self.year_details_frame.pack_forget()

        self.add_course_view = AddCourseView(
            self.master,
            self.course_service,
            self.add_course_to_period,
            period,
        )
        self.add_course_view.pack(pady=10)

    def add_course_to_period(self, course, period):
        self.course_service.add_course_to_period(course, period)
        self.load_periods(self.currently_shown_year)

    def hide_year_details(self):
        if hasattr(self, "year_details_frame"):
            self.year_details_frame.pack_forget()
            self.year_details_frame.destroy()
        self.currently_shown_year = None
