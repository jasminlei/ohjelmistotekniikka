import tkinter as tk
from ttkbootstrap import Frame, Label, Entry, Button


class AcademicYearForm(Frame):
    def __init__(self, master, studyplan_service, studyplan, on_success_callback):
        super().__init__(master)
        self.studyplan_service = studyplan_service
        self.studyplan = studyplan
        self.on_success_callback = on_success_callback

        self.start_year_entry = Entry(self, width=6)
        self.start_year_entry.insert(0, "2024")
        self.start_year_entry.pack(side=tk.LEFT, padx=5)

        Label(self, text="-").pack(side=tk.LEFT)

        self.end_year_entry = Entry(self, width=6)
        self.end_year_entry.insert(0, "2025")
        self.end_year_entry.pack(side=tk.LEFT, padx=5)

        Button(
            self,
            text="Lisää",
            bootstyle="success",
            command=self.submit_years,
        ).pack(side=tk.LEFT, padx=10)

        self.error_label = Label(self, text="", foreground="red")
        self.error_label.pack(pady=5, side=tk.BOTTOM)

    def submit_years(self):
        start_year = self.start_year_entry.get()
        end_year = self.end_year_entry.get()

        self.error_label.config(text="")

        result = self.studyplan_service.add_academic_year_to_plan(
            self.studyplan, int(start_year), int(end_year)
        )

        if result == "success":
            self.on_success_callback()
        else:
            self.error_label.config(text=result)
            self.after(5000, lambda: self.error_label.config(text=""))
