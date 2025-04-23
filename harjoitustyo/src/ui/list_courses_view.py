from ttkbootstrap import Frame, Label, Button, Toplevel, Entry
from datetime import datetime
import textwrap
from tkinter import ttk
import tkinter as tk

import tkinter.messagebox as messagebox


class ListCoursesView(Frame):
    def __init__(self, root, course_service, logged_user, handle_back):
        super().__init__(root)
        self._course_service = course_service
        self._logged_user = logged_user
        self._handle_back = handle_back
        self.selected_course = None
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

        list_container = Frame(self)
        list_container.pack(pady=20, fill="both", expand=True)

        self.treeview = ttk.Treeview(
            list_container,
            columns=("Code", "Name", "Credits", "Status"),
            show="headings",
        )
        self.treeview.heading("Code", text="Koodi", anchor="w")
        self.treeview.heading("Name", text="Kurssi", anchor="w")
        self.treeview.heading("Credits", text="Opintopisteet", anchor="w")
        self.treeview.heading("Status", text="Tila", anchor="w")

        self.treeview.column("Code", width=100)
        self.treeview.column("Name", width=150)
        self.treeview.column("Credits", width=100)
        self.treeview.column("Status", width=120)

        scrollbar = ttk.Scrollbar(
            list_container, orient="vertical", command=self.treeview.yview
        )
        self.treeview.configure(yscrollcommand=scrollbar.set)

        self.treeview.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.course_details_text = tk.Text(
            self,
            height=14,
            wrap="word",
            font=("Arial", 11),
            padx=10,
            pady=10,
            borderwidth=1,
            relief="solid",
        )
        self.course_details_text.insert(
            "1.0", "Valitse kurssi ylläolevasta listasta tarkastellaksesi sen tietoja."
        )
        self.course_details_text.configure(state="disabled")
        self.course_details_text.pack(pady=10, fill="x", padx=20)

        self.actions_frame = Frame(self)
        self.actions_frame.pack(pady=10)

        self._populate_courses()

        back_button = Button(
            self, text="Takaisin", bootstyle="secondary", command=self._handle_back
        )
        back_button.pack(pady=10)

    def _populate_courses(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        courses = self._course_service.get_all_courses_by_user(self._logged_user)
        for course in courses:
            completed = "Suoritettu" if course.is_completed else "Ei suoritettu"
            self.treeview.insert(
                "", "end", values=(course.code, course.name, course.credits, completed)
            )

        self.treeview.bind("<ButtonRelease-1>", self._on_course_click)

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
        self.selected_course = next(
            (c for c in user_courses if c.code == course_code), None
        )

        if self.selected_course:
            self._show_course_details(self.selected_course)

    def _show_course_details(self, course):
        grade_text = course.grade if course.grade else "Ei suoritettu"
        description = course.description or "Ei kuvausta"
        plans = self._course_service.get_course_timing(course)

        if plans:
            bullet_lines = [f"  • {self._get_plan_details(plan)}" for plan in plans]
            plans_text = "\n".join(bullet_lines)
        else:
            plans_text = "  Ei sijoitettu opintosuunnitelmaan"

        details_message = (
            f"Koodi: {course.code}\n\n"
            f"Nimi: {course.name}\n\n"
            f"Opintopisteet: {course.credits} op\n\n"
            f"Kuvaus:\n{textwrap.fill(description, width=70, initial_indent='  ', subsequent_indent='  ')}\n\n"
            f"Arvosana: {grade_text}\n\n"
            f"Opintosuunnitelma:\n{plans_text}"
        )

        self.course_details_text.configure(state="normal")
        self.course_details_text.delete("1.0", "end")
        self.course_details_text.insert("1.0", details_message)
        self.course_details_text.configure(state="disabled")

        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        button_text = (
            "Muokkaa suoritusta" if course.is_completed else "Merkitse suoritetuksi"
        )

        self.mark_completed_button = Button(
            self.actions_frame,
            text=button_text,
            bootstyle="success",
            width=25,
            command=self._mark_completed,
        )
        self.mark_completed_button.pack(pady=5)

        self.delete_button = Button(
            self.actions_frame,
            text="Poista kurssi",
            bootstyle="danger",
            width=25,
            command=self._delete_course,
        )
        self.delete_button.pack(pady=5)

    def _get_plan_details(self, plan):
        return (
            f"Suunnitelma: {plan['studyplan']['plan_name']}, "
            f"vuosi: {plan['academicyear']['year']}, "
            f"periodi: {plan['period']['period_name']}"
        )

    def _mark_completed(self):
        if not self.selected_course:
            return

        mark_completed_window = Toplevel(self)
        mark_completed_window.title("Merkitse suoritetuksi")

        Label(mark_completed_window, text="Suorituspäivämäärä (yyyy-mm-dd):").pack(
            pady=5
        )
        default_date = (
            self.selected_course.completion_date
            if self.selected_course.completion_date
            else datetime.today().strftime("%Y-%m-%d")
        )

        date_entry = Entry(mark_completed_window)
        date_entry.insert(0, default_date)
        date_entry.pack(pady=5)

        Label(mark_completed_window, text="Arvosana:").pack(pady=5)
        grade_var = tk.StringVar(value="Hyväksytty")

        grades = ["1", "2", "3", "4", "5", "Hyväksytty"]
        for grade in grades:
            ttk.Radiobutton(
                mark_completed_window, text=grade, variable=grade_var, value=grade
            ).pack(side="top", padx=5, pady=2)

        feedback_label = Label(mark_completed_window, text="", foreground="green")
        feedback_label.pack(pady=5)

        Button(
            mark_completed_window,
            text="Merkitse suoritetuksi",
            bootstyle="success",
            width=25,
            command=lambda: self.submit_mark(
                grade_var.get(), date_entry.get(), feedback_label
            ),
        ).pack(pady=10)

    def submit_mark(self, grade, completion_date, feedback_label):
        if self.selected_course:
            success, message = self._course_service.mark_as_completed(
                self.selected_course, grade, completion_date
            )

            if success:
                feedback_label.config(
                    text="Kurssi merkitty suoritetuksi!", foreground="green"
                )
                self._populate_courses()
                self._clear_course_details()
            else:
                feedback_label.config(text=message, foreground="red")

    def _delete_course(self):
        selected_items = self.treeview.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        course_data = self.treeview.item(selected_item, "values")

        if not course_data:
            return

        course_code = course_data[0]
        user_courses = self._course_service.get_all_courses_by_user(self._logged_user)
        course_to_delete = next(
            (c for c in user_courses if c.code == course_code), None
        )

        if not course_to_delete:
            return

        confirmation = messagebox.askyesno(
            "Vahvista poisto",
            f"Oletko varma, että haluat poistaa kurssin {course_to_delete.name}? Kurssi poistuu myös kaikista suunnitelmista, joihin se on lisätty.",
        )

        if confirmation:
            success = self._course_service.delete_course(course_to_delete)

            if success:
                messagebox.showinfo(
                    "Poisto onnistui", f"Kurssi {course_to_delete.name} poistettu."
                )
                self._clear_course_details()
                self._populate_courses()
            else:
                messagebox.showerror("Virhe", "Kurssin poistaminen epäonnistui.")

    def _clear_course_details(self):
        self.course_details_text.configure(state="normal")
        self.course_details_text.delete("1.0", "end")
        self.course_details_text.insert(
            "1.0", "Valitse kurssi ylläolevasta listasta tarkastellaksesi sen tietoja."
        )
        self.course_details_text.configure(state="disabled")

        self.selected_course = None

        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        self.treeview.selection_remove(self.treeview.selection())
