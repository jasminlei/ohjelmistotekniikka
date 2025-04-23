import tkinter as tk
from ttkbootstrap import Frame, Label, OptionMenu, Button


class StatisticView(Frame):
    def __init__(
        self,
        master,
        user_service,
        studyplan_service,
        academicyear_service,
        course_service,
        period_service,
        statistics_service,
        user,
        handle_back,
    ):
        super().__init__(master)
        self.user_service = user_service
        self.studyplan_service = studyplan_service
        self.academicyear_service = academicyear_service
        self.course_service = course_service
        self.period_service = period_service
        self.statistics_service = statistics_service
        self.user = user
        self.handle_back = handle_back

        self.plan_var = tk.StringVar()
        self.stats_frame = None

        self.year_var = tk.StringVar()
        self.years = []
        self.year_stats_frame = None

        self.render()

    def render(self):
        Label(self, text="Valitse opintosuunnitelma:").pack(
            anchor="w", padx=10, pady=(10, 0)
        )

        self.plans = self.studyplan_service.get_studyplans_by_user(self.user)

        if not self.plans:
            Label(self, text="Ei opintosuunnitelmia.").pack(padx=10, pady=10)
            return

        plan_names = ["Valitse opintosuunnitelma"] + [
            plan.plan_name for plan in self.plans
        ]
        self.plan_var.set(plan_names[0])

        OptionMenu(
            self,
            self.plan_var,
            *plan_names,
            command=self.update_statistics,
        ).pack(padx=10, pady=5, anchor="w")

        self.stats_frame = Frame(self)
        self.stats_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        Button(
            self, text="Takaisin", command=self.handle_back, bootstyle="secondary"
        ).pack(pady=(10, 5))

    def update_statistics(self, selected_plan_name):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        if selected_plan_name == "Valitse opintosuunnitelma":
            return

        plan = next((p for p in self.plans if p.plan_name == selected_plan_name), None)
        if not plan:
            Label(self.stats_frame, text="Suunnitelmaa ei löytynyt.").pack()
            return

        total_credits = self.statistics_service.get_total_credits(plan)
        completed_credits = self.statistics_service.get_completed_credits(plan)
        percent_completed = self.statistics_service.get_percentage_completed(plan)
        mean_grade = self.statistics_service.get_mean_grade(plan)

        Label(
            self.stats_frame, text=f"Yhteensä opintopisteitä: {total_credits} op"
        ).pack(anchor="w")
        Label(
            self.stats_frame, text=f"Suoritetut opintopisteet: {completed_credits} op"
        ).pack(anchor="w")
        Label(self.stats_frame, text=f"Tavoite: {plan.goal_credits} op").pack(
            anchor="w"
        )
        Label(self.stats_frame, text=f"Suoritettu: {percent_completed:.1f}%").pack(
            anchor="w", pady=(0, 10)
        )

        if mean_grade is not None:
            Label(self.stats_frame, text=f"Keskiarvo: {mean_grade:.2f}").pack(
                anchor="w", pady=(0, 10)
            )
        else:
            Label(self.stats_frame, text="Keskiarvoa ei voida vielä laskea.").pack(
                anchor="w", pady=(0, 10)
            )

        Label(self.stats_frame, text="Valitse lukuvuosi:").pack(anchor="w")

        self.years = self.academicyear_service.get_academic_years_by_studyplan(plan)
        year_options = ["Valitse lukuvuosi"] + [
            f"{y.start_year}-{y.end_year}" for y in self.years
        ]
        if len(year_options) == 1:
            Label(self.stats_frame, text="Ei lukuvuosia.").pack()
            return

        self.year_var.set(year_options[0])

        OptionMenu(
            self.stats_frame,
            self.year_var,
            *year_options,
            command=lambda selected: self.update_year_statistics(selected, plan),
        ).pack(pady=(0, 10), anchor="w")

        self.year_stats_frame = Frame(self.stats_frame)
        self.year_stats_frame.pack(fill=tk.BOTH, expand=True)

    def update_year_statistics(self, selected_year, plan):
        for widget in self.year_stats_frame.winfo_children():
            widget.destroy()

        if selected_year == "Valitse lukuvuosi":
            return

        start_year = int(selected_year.split("-")[0])
        year = next((y for y in self.years if y.start_year == start_year), None)
        if not year:
            Label(self.year_stats_frame, text="Lukuvuotta ei löytynyt.").pack()
            return

        scheduled_credits = self.statistics_service.get_scheduled_credits_by_year(year)
        completed_credits = self.statistics_service.get_completed_credits_by_year(year)

        Label(
            self.year_stats_frame,
            text=f"Vuoden {selected_year} aikana suoritetut: {completed_credits} op",
        ).pack(anchor="w")
        Label(
            self.year_stats_frame,
            text=f"Aikataulutetut opintopisteet: {scheduled_credits} op",
        ).pack(anchor="w", pady=(0, 10))

        Label(self.year_stats_frame, text="Jakautuminen periodeittain:").pack(
            anchor="w"
        )

        period_data = self.statistics_service.get_credits_by_period(year)
        for period_number, credits in period_data:
            name = f"Periodi {period_number}" if period_number != 5 else "Kesä"
            Label(self.year_stats_frame, text=f"{name}: {credits} op").pack(anchor="w")
