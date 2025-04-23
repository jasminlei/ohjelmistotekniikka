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
        self.window.geometry("400x500")
        self.window.title(f"{course.code} - {course.name}")

        Label(
            self.window,
            text=f"{course.code} {course.name}",
            font=("Arial", 12, "bold"),
        ).pack(pady=5)

        description_label = Label(
            self.window,
            text=f"Kurssin kuvaus: {course.description}",
            font=("Arial", 12),
            wraplength=350,
        )
        description_label.pack(pady=5)

        Label(
            self.window,
            text=f"Arvosana: {course.grade if course.grade else 'Ei arvosanaa'}",
            font=("Arial", 12),
        ).pack(pady=5)

        Label(
            self.window,
            text=f"Suorituspäivämäärä: {course.completion_date if course.completion_date else '-'}",
            font=("Arial", 12),
        ).pack(pady=5)

        button_text = (
            "Muokkaa suoritusta"
            if self.course.is_completed
            else "Merkitse suoritetuksi"
        )
        Button(
            self.window,
            text=button_text,
            bootstyle="info",
            width=25,
            command=self.show_mark_completed_form,
        ).pack(pady=10)

        Button(
            self.window,
            text="Poista kurssi suunnitelmasta",
            bootstyle="danger",
            width=25,
            command=self.delete_course_from_plan,
        ).pack(pady=10)

        Button(
            self.window,
            text="Sulje",
            bootstyle="secondary",
            width=25,
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
        default_date = (
            self.course.completion_date
            if self.course.completion_date
            else datetime.today().strftime("%Y-%m-%d")
        )
        self.date_entry = Entry(form_frame)
        self.date_entry.insert(0, default_date)
        self.date_entry.pack(pady=5)

        Label(form_frame, text="Arvosana:").pack(pady=5)

        self.grade_var = tk.StringVar(value="Hyväksytty")
        grades = ["1", "2", "3", "4", "5", "Hyväksytty"]

        grades_frame = Frame(form_frame)
        grades_frame.pack(pady=5)

        for grade in grades:
            tk.Radiobutton(
                grades_frame, text=grade, variable=self.grade_var, value=grade
            ).pack(side="left", padx=5)

        Button(
            form_frame,
            text="Tallenna",
            bootstyle="success",
            command=self.mark_course_as_completed,
        ).pack(pady=10)

    def mark_course_as_completed(self):
        success, result = self.course_service.mark_as_completed(
            self.course, self.grade_var.get(), self.date_entry.get()
        )

        if success:
            self.window.destroy()
            if self.on_update:
                self.on_update()
        else:
            self.show_error_message(result)

    def delete_course_from_plan(self):
        success = self.course_service.remove_course_from_period(
            self.period, self.course
        )
        if success:
            self.window.destroy()
            if self.on_update:
                self.on_update()

    def show_error_message(self, message):
        error_label = Label(
            self.window, text=message, foreground="red", font=("Arial", 10, "bold")
        )
        error_label.pack(pady=5)
