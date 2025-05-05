import tkinter as tk
from tkinter import Toplevel
import ttkbootstrap as ttk
from ttkbootstrap import Frame, Label, Button, Entry
from ui.add_course_to_plan_view import AddCourseToPlanView
from ui.periods_view import PeriodsView
from ui.coursedetails_view import CourseDetailsView


class StudyPlansView(Frame):
    def __init__(
        self,
        master,
        studyplan_service,
        academicyear_service,
        course_service,
        period_service,
        statistics_service,
        logged_user,
        handle_back,
    ):
        super().__init__(master)
        self.studyplan_service = studyplan_service
        self.academicyear_service = academicyear_service
        self.course_service = course_service
        self.period_service = period_service
        self.statistics_service = statistics_service
        self.logged_user = logged_user
        self.handle_back = handle_back
        self.currently_shown_studyplan = None
        self.currently_shown_year = None
        self.academic_year_entry_visible = False

        Label(self, text="Lisätyt opintosuunnitelmat", font=("Arial", 16, "bold")).pack(
            pady=10
        )

        self.studyplans_frame = Frame(self)
        self.studyplans_frame.pack(pady=10)

        self.details_frame = Frame(self)
        self.years_frame = None

        self.studyplan_menu = ttk.Menubutton(
            self.studyplans_frame,
            text="Valitse opintosuunnitelma",
            bootstyle="primary",
            width=30,
        )
        self.studyplan_menu.pack(pady=5)

        self.studyplan_menu.menu = tk.Menu(self.studyplan_menu, tearoff=0)
        self.studyplan_menu["menu"] = self.studyplan_menu.menu

        self.load_studyplans()

        self.back_button = Button(
            self,
            text="Takaisin",
            bootstyle="secondary",
            command=self.on_back_button_clicked,
        )
        self.back_button.pack(pady=10, side=tk.BOTTOM)

    def load_studyplans(self):
        self.studyplan_menu.menu.delete(0, "end")

        studyplans = self.studyplan_service.get_studyplans_by_user(self.logged_user)

        for studyplan in studyplans:
            self.studyplan_menu.menu.add_command(
                label=studyplan.plan_name,
                command=lambda sp=studyplan: self.on_studyplan_selected(sp),
            )

    def on_studyplan_selected(self, studyplan):
        self.toggle_studyplan_details(studyplan)

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
            font=("Arial", 14, "bold"),
        ).pack(pady=5)

        self.years_frame = Frame(self.details_frame)
        self.years_frame.pack(pady=10)

        self.load_academic_years(studyplan)

        Label(self.details_frame, text="Lisää vuosi", font=("Arial", 12, "bold")).pack(
            pady=5
        )

        self.toggle_year_button = Button(
            self.details_frame,
            text="Lisää akateeminen vuosi",
            bootstyle="primary",
            command=lambda: self.toggle_academic_year_form(studyplan),
        )

        self.toggle_year_button.pack(pady=10)

        self.details_frame.pack(pady=10)
        self.currently_shown_studyplan = studyplan

        self.year_error_label = Label(self.details_frame, text="", foreground="red")
        self.year_error_label.pack()

    def toggle_academic_year_form(self, studyplan):
        if self.academic_year_entry_visible:
            self.start_year_entry_frame.pack_forget()
            self.end_year_entry_frame.pack_forget()
            self.academic_year_entry_visible = False
            self.toggle_year_button.config(text="Lisää suunnitelmaan vuosi")
        else:
            self.show_academic_year_form(studyplan)
            self.academic_year_entry_visible = True
            self.toggle_year_button.config(text="Piilota vuoden lisäys")

    def show_academic_year_form(self, studyplan):
        entry_frame = Frame(self.details_frame)
        entry_frame.pack(pady=5)

        self.start_year_entry_frame = entry_frame
        self.start_year_entry = Entry(entry_frame, width=6)
        self.start_year_entry.insert(0, "2024")
        self.start_year_entry.pack(side=tk.LEFT, padx=5)

        Label(entry_frame, text="-").pack(side=tk.LEFT)

        self.end_year_entry_frame = entry_frame
        self.end_year_entry = Entry(entry_frame, width=6)
        self.end_year_entry.insert(0, "2025")
        self.end_year_entry.pack(side=tk.LEFT, padx=5)

        Button(
            entry_frame,
            text="Lisää",
            bootstyle="success",
            command=lambda: self.add_academic_year(studyplan),
        ).pack(side=tk.LEFT, padx=10)

    def add_academic_year(self, studyplan):
        start_year = self.start_year_entry.get()
        end_year = self.end_year_entry.get()

        self.year_error_label.config(text="")

        success, result = self.studyplan_service.add_academic_year_to_plan(
            studyplan, int(start_year), int(end_year)
        )

        if not success:
            self.year_error_label.config(text=result)
            self.after(5000, self.hide_error_label)
        else:
            self.load_academic_years(studyplan)

    def hide_error_label(self):
        self.year_error_label.config(text="")

    def hide_studyplan_details(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        self.currently_shown_studyplan = None

    def load_academic_years(self, studyplan):
        if hasattr(self, "academic_year_menu"):
            self.academic_year_menu.pack_forget()
            self.academic_year_menu.destroy()

        if self.years_frame:
            for widget in self.years_frame.winfo_children():
                widget.destroy()

        academic_years = self.academicyear_service.get_academic_years_by_studyplan(
            studyplan
        )

        if not academic_years:
            Label(
                self.years_frame,
                text="Ei lisättyjä vuosia.",
            ).pack(pady=5)
            return

        self.academic_year_menu = ttk.Menubutton(
            self.studyplans_frame,
            text="Valitse vuosi",
            bootstyle="warning",
            width=30,
        )
        self.academic_year_menu.menu = tk.Menu(self.academic_year_menu, tearoff=0)
        self.academic_year_menu["menu"] = self.academic_year_menu.menu

        for academic_year in academic_years:
            self.academic_year_menu.menu.add_command(
                label=f"{academic_year.start_year}-{academic_year.end_year}",
                command=lambda ay=academic_year: self.show_year_details(ay),
            )

        self.academic_year_menu.pack(pady=5)

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

        self.load_periods(academic_year, self.currently_shown_studyplan)

        self.currently_shown_year = academic_year
        Button(
            self.year_details_frame,
            text="Poista vuosi",
            bootstyle="danger",
            width=25,
            command=lambda: self.confirm_delete_year(academic_year),
        ).pack(pady=10)

    def confirm_delete_year(self, academic_year):
        confirm_window = Toplevel(self)
        confirm_window.title("Vahvista poisto")

        Label(
            confirm_window,
            text=f"Haluatko varmasti poistaa vuoden {academic_year.start_year}-{academic_year.end_year}?",
            font=("Arial", 12),
        ).pack(padx=20, pady=10)

        Button(
            confirm_window,
            text="Poista",
            bootstyle="danger",
            width=25,
            command=lambda: self.delete_year(academic_year, confirm_window),
        ).pack(side=tk.LEFT, padx=10, pady=10)

        Button(
            confirm_window,
            text="Peruuta",
            bootstyle="secondary",
            command=confirm_window.destroy,
        ).pack(side=tk.LEFT, padx=10, pady=10)

    def delete_year(self, academic_year, confirm_window):
        self.academicyear_service.delete_year(academic_year.year_id)
        confirm_window.destroy()
        self.hide_year_details()
        self.load_academic_years(self.currently_shown_studyplan)
        self.show_message("Vuosi poistettu onnistuneesti.")

    def load_periods(self, academic_year, studyplan):
        if hasattr(self, "periods_view") and self.periods_view.winfo_exists():
            self.periods_view.destroy()

        self.periods_view = PeriodsView(
            self.year_details_frame,
            academic_year,
            studyplan,
            self.period_service,
            self.course_service,
            self.statistics_service,
            self.show_course_details,
            self.show_add_course_view,
        )

    def hide_period_details(self):
        if hasattr(self, "periods_view") and self.periods_view.winfo_exists():
            self.periods_view.destroy()

    def show_course_details(self, course, period):
        CourseDetailsView(
            self,
            course,
            period,
            self.course_service,
            on_update=lambda: self.reload_periods(),
        )

    def reload_periods(self):
        self.hide_period_details()
        self.load_periods(self.currently_shown_year, self.currently_shown_studyplan)

    def show_message(self, message):
        message_label = Label(
            self, text=message, font=("Arial", 10, "italic"), foreground="green"
        )
        message_label.pack(pady=10)
        self.after(3000, message_label.destroy)

    def show_add_course_view(self, period):
        if (
            hasattr(self, "course_list_window")
            and self.course_list_window.winfo_exists()
        ):
            self.course_list_window.destroy()

        course_list_window = Toplevel(self)
        course_list_window.title("Valitse kurssi")

        Label(course_list_window, text="Kurssit", font=("Arial", 14, "bold")).pack(
            pady=10
        )

        self.add_course_view = AddCourseToPlanView(
            course_list_window,
            self.course_service,
            self.add_course_to_period,
            period,
            self.currently_shown_studyplan,
            self.logged_user,
        )
        self.add_course_view.pack(pady=10)

        Button(
            course_list_window,
            text="Sulje",
            bootstyle="secondary",
            command=course_list_window.destroy,
        ).pack(pady=10)

    def add_course_to_period(self, course, period):
        success, error_message = self.course_service.add_course_to_period(
            period, course
        )

        if success:
            self.hide_period_details()
            self.load_periods(self.currently_shown_year, self.currently_shown_studyplan)
            self.show_message("Kurssi lisätty!")
        else:
            self.show_message(error_message, is_error=True)

    def hide_year_details(self):
        if hasattr(self, "year_details_frame"):
            self.year_details_frame.pack_forget()
            self.year_details_frame.destroy()
        self.currently_shown_year = None

    def on_back_button_clicked(self):
        if hasattr(self, "add_course_view"):
            try:
                self.add_course_view.hide()
                return
            except tk.TclError:
                pass

        self.handle_back()
