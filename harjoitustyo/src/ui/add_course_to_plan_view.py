import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Frame


class AddCourseToPlanView(Frame):
    def __init__(
        self, master, course_service, add_course_callback, period, logged_user
    ):
        super().__init__(master)
        self.course_service = course_service
        self.add_course_callback = add_course_callback
        self.period = period
        self.logged_in_user = logged_user

        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )

        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.course_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.course_frame, anchor="nw")

        self.load_existing_courses()

    def load_existing_courses(self):
        for widget in self.course_frame.winfo_children():
            widget.destroy()

        courses = self.course_service.get_courses_not_in_period(
            self.period, self.logged_in_user
        )

        row = 0
        for course in courses:
            course_label = ttk.Label(
                self.course_frame,
                text=f"{course.code} - {course.name} - {course.credits}",
            )
            course_label.grid(row=row, column=0, sticky="w", pady=5)

            add_link = ttk.Label(
                self.course_frame,
                text="Lisää",
                bootstyle="primary",
                foreground="blue",
                cursor="hand2",
            )
            add_link.grid(row=row, column=1, padx=5, pady=5)

            add_link.bind(
                "<Button-1>",
                lambda event, course=course: self.add_selected_course(course),
            )

            row += 1

        self.course_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def add_selected_course(self, course):
        if course:
            self.add_course_callback(course, self.period)
        else:
            print("Kurssia ei löydetty.")

    def hide(self):
        self.pack_forget()
        for widget in self.winfo_children():
            widget.destroy()
