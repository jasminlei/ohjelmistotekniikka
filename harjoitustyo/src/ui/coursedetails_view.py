import tkinter as tk
from tkinter import Toplevel
from ttkbootstrap import Frame, Label, Button, Entry
from datetime import datetime


class CourseDetailsView:
    def __init__(self, master, course, period, course_service, on_update=None):
        self.course = course
        self.period = period
        self.course_service = course_service
        self.on_update = on_update

        self.window = Toplevel(master)
        self.window.title(f"{course.code} - {course.name}")

        Label(
            self.window,
            text=f"{course.code} {course.name}",
            font=("Arial", 12, "bold"),
        ).pack(pady=5)
        Label(
            self.window,
            text=f"Kurssin kuvaus: {course.description}",
            font=("Arial", 10),
        ).pack(pady=5)
        Label(
            self.window,
            text=f"Arvosana: {course.grade if course.grade else 'Ei arvosanaa'}",
            font=("Arial", 10),
        ).pack(pady=5)

        Label(
            self.window,
            text=f"Suorituspäivämäärä: {course.completion_date if course.completion_date else '-'}",
            font=("Arial", 10),
        ).pack(pady=5)

        Button(
            self.window,
            text="Merkitse suoritetuksi",
            bootstyle="info",
            command=self.show_mark_completed_form,
        ).pack(pady=10)

        Button(
            self.window,
            text="Poista kurssi",
            bootstyle="danger",
            command=self.delete_course_from_plan,
        ).pack(pady=10)

        Button(
            self.window,
            text="Sulje",
            bootstyle="secondary",
            command=self.window.destroy,
        ).pack(pady=10)

    def show_mark_completed_form(self):
        for widget in self.window.winfo_children():
            if (
                isinstance(widget, Button)
                and widget.cget("text") == "Merkitse suoritetuksi"
            ):
                widget.pack_forget()

        form_frame = Frame(self.window)
        form_frame.pack(pady=10)

        Label(form_frame, text="Suorituspäivämäärä (yyyy-mm-dd):").pack(pady=5)
        today = datetime.today().strftime("%Y-%m-%d")
        self.date_entry = Entry(form_frame)
        self.date_entry.insert(0, today)
        self.date_entry.pack(pady=5)

        Label(form_frame, text="Arvosana:").pack(pady=5)
        self.grade_var = tk.StringVar(value="Hyväksytty")
        grades = ["1", "2", "3", "4", "5", "Hyväksytty"]

        for grade in grades:
            tk.Radiobutton(
                form_frame, text=grade, variable=self.grade_var, value=grade
            ).pack(side=tk.LEFT, padx=5)

        Button(
            form_frame,
            text="Merkitse suoritetuksi",
            bootstyle="success",
            command=self.mark_course_as_completed,
        ).pack(pady=10)

    def mark_course_as_completed(self):
        success = self.course_service.mark_as_completed(
            self.course, self.grade_var.get(), self.date_entry.get()
        )

        if success:
            self.window.destroy()
            if self.on_update:
                self.on_update()

    def delete_course_from_plan(self):
        success = self.course_service.remove_course_from_period(
            self.period, self.course
        )
        if success:
            self.window.destroy()
            if self.on_update:
                self.on_update()
