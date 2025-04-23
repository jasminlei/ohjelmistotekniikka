import tkinter as tk
from ttkbootstrap import Frame, Label, Button, Notebook


class PeriodsView(Frame):
    def __init__(
        self,
        master,
        academic_year,
        studyplan,
        period_service,
        course_service,
        statistics_service,
        show_course_details,
        show_add_course_view,
    ):
        super().__init__(master)
        self.academic_year = academic_year
        self.studyplan = studyplan
        self.period_service = period_service
        self.course_service = course_service
        self.statistics_service = statistics_service
        self.show_course_details = show_course_details
        self.show_add_course_view = show_add_course_view

        self.pack(pady=5, fill=tk.BOTH, expand=True)
        self.render()

    def render(self):
        periods = self.period_service.get_periods_by_academic_year(self.academic_year)

        if not periods:
            Label(self, text="Ei lisättyjä periodeja.").pack()
            return

        total_credits = self.statistics_service.get_total_credits(self.studyplan)
        year_credits = self.statistics_service.get_scheduled_credits_by_year(
            self.academic_year
        )

        Label(
            self,
            text=f"Suunnitelmaan valittu {total_credits} opintopisteen edestä kursseja, joista vuodella {self.academic_year.start_year}-{self.academic_year.end_year} {year_credits} op.",
            font=("Arial", 12),
        ).pack(pady=5)

        Label(
            self,
            text="Klikkaa kurssia tarkastellaksesi sen tietoja, merkitäksesi sen suoritetuksi tai poistaaksesi sen suunnitelmasta.",
            font=("Arial", 12, "italic"),
            anchor="w",
            justify="left",
        ).pack(padx=5, pady=(0, 5), anchor="w")

        notebook = Notebook(self, width=550)
        notebook.pack(pady=5, fill=tk.BOTH, expand=True)

        for period in periods:
            period_frame = Frame(notebook)
            notebook.add(
                period_frame,
                text=f"Periodi {period.period_number}"
                if period.period_number != 5
                else "Kesä",
            )

            self.render_courses(period_frame, period)

    def render_courses(self, period_frame, period):
        courses = self.course_service.get_courses_by_period(period)

        if courses:
            for course in courses:
                course_frame = Frame(period_frame)
                course_frame.pack(fill=tk.X, padx=5, pady=2)

                Label(course_frame, text=course.code, width=12, anchor="w").pack(
                    side=tk.LEFT, padx=4
                )
                Label(course_frame, text=course.name, width=20, anchor="w").pack(
                    side=tk.LEFT, padx=4
                )
                Label(
                    course_frame, text=f"{course.credits} op", width=5, anchor="w"
                ).pack(side=tk.LEFT, padx=4)
                Label(
                    course_frame,
                    text="Suoritettu ✓" if course.is_completed else "Ei suoritettu",
                    width=10,
                    anchor="w",
                ).pack(side=tk.LEFT, padx=4)
                Label(
                    course_frame,
                    text=f"Arvosana: {'Hyv.' if course.grade == 'Hyväksytty' else course.grade if course.grade else '-'}",
                    width=20,
                    anchor="w",
                ).pack(side=tk.LEFT, padx=4)

                course_frame.bind(
                    "<Button-1>",
                    lambda e, c=course, p=period: self.show_course_details(c, p),
                )
                for widget in course_frame.winfo_children():
                    widget.bind(
                        "<Button-1>",
                        lambda e, c=course, p=period: self.show_course_details(c, p),
                    )
        else:
            Label(period_frame, text="(Ei kursseja)", font=("Arial", 9, "italic")).pack(
                padx=5, pady=2
            )

        Button(
            period_frame,
            text="Lisää kurssi",
            bootstyle="success",
            command=lambda p=period: self.show_add_course_view(p),
        ).pack(pady=10, anchor="w")
