import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Frame
import textwrap


class AddCourseToPlanView(Frame):
    def __init__(
        self, master, course_service, add_course_callback, period, plan, logged_user
    ):
        super().__init__(master)
        self.course_service = course_service
        self.add_course_callback = add_course_callback
        self.period = period
        self.plan = plan
        self.logged_in_user = logged_user

        self.canvas = tk.Canvas(self, width=500)
        self.scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self.canvas.yview
        )

        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.course_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.course_frame, anchor="nw")

        self.load_existing_courses()

    def shorten_course_name(self, course_name, max_length=25):
        if len(course_name) > max_length:
            return textwrap.shorten(course_name, width=max_length, placeholder="...")
        return course_name

    def load_existing_courses(self):
        for widget in self.course_frame.winfo_children():
            widget.destroy()

        courses = self.course_service.get_all_courses_by_user(self.logged_in_user)

        row = 0
        for course in courses:
            all_courses_in_plan = self.course_service.get_courses_by_studyplan(
                self.plan
            )
            is_course_in_plan = any(c.code == course.code for c in all_courses_in_plan)

            shortened_name = self.shorten_course_name(course.name, max_length=25)
            course_label = ttk.Label(
                self.course_frame,
                text=f"{course.code} - {shortened_name} - {course.credits} op",
            )
            course_label.grid(row=row, column=0, sticky="w", pady=5)

            if is_course_in_plan:
                added_label = ttk.Label(
                    self.course_frame,
                    text="Lisätty jo suunnitelmaan",
                    foreground="gray",
                )
                added_label.grid(row=row, column=1, padx=5, pady=5)
            else:
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
