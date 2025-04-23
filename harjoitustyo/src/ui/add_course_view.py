from ttkbootstrap import Frame, Label, Entry, Button
import tkinter as tk


class AddCourseView(Frame):
    def __init__(self, root, course_service, handle_back):
        super().__init__(root)
        self._course_service = course_service
        self._handle_back = handle_back
        self._create_widgets()

    def _create_widgets(self):
        label = Label(
            self, text="Lisää kurssi", font=("Arial", 16), bootstyle="primary"
        )
        label.pack(pady=20)

        self.code_label = Label(self, text="Kurssin koodi:")
        self.code_label.pack()
        self.code_entry = Entry(self)
        self.code_entry.pack(pady=5)

        self.name_label = Label(self, text="Kurssin nimi:")
        self.name_label.pack()
        self.name_entry = Entry(self)
        self.name_entry.pack(pady=5)

        self.credits_label = Label(self, text="Opintopisteet:")
        self.credits_label.pack()
        self.credits_entry = Entry(self)
        self.credits_entry.pack(pady=5)

        self.description_label = Label(self, text="Kurssin kuvaus (valinnainen):")
        self.description_label.pack()
        self.description_text = tk.Text(self, height=5, width=40, wrap="word")
        self.description_text.pack(pady=5)

        self.error_label = Label(self, text="", foreground="red", bootstyle="danger")
        self.error_label.pack(pady=5)

        self.success_label = Label(
            self, text="", foreground="green", bootstyle="success"
        )
        self.success_label.pack(pady=5)

        self.add_course_button = Button(
            self, text="Lisää kurssi", bootstyle="success", command=self.add_course
        )
        self.add_course_button.pack(pady=10)

        self.back_button = Button(
            self, text="Takaisin", bootstyle="danger", command=self._handle_back
        )
        self.back_button.pack(pady=5)

    def add_course(self):
        self.error_label.config(text="")
        self.success_label.config(text="")

        code = self.code_entry.get().strip()
        name = self.name_entry.get().strip()
        credits = self.credits_entry.get().strip()
        description = self.description_text.get("1.0", "end").strip()

        if not code or not name or not credits:
            self.error_label.config(
                text="Kurssin koodi, nimi ja opintopisteet ovat pakollisia!"
            )
            return

        if not credits.isdigit():
            self.error_label.config(text="Opintopisteiden tulee olla numero!")
            return

        success, course = self._course_service.add_course(
            code, name, credits, description
        )
        if success:
            self.success_label.config(text=f"Kurssi {course.name} lisätty.")
            self.description_text.delete("1.0", "end")
        else:
            self.error_label.config(text=f"Virhe kurssin lisäämisessä: {course}")
