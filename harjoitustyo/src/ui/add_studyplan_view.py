from ttkbootstrap import Frame, Label, Entry, Button


class AddStudyPlanView(Frame):
    def __init__(self, root, studyplan_service, logged_user, handle_back):
        super().__init__(root)
        self._studyplan_service = studyplan_service
        self._handle_back = handle_back
        self._logged_user = logged_user

        self._plan_name_entry = None
        self._create_widgets()

    def _create_widgets(self):
        Label(self, text="Lisää uusi opintosuunnitelma", font=("Arial", 16)).pack(
            pady=10
        )

        Label(self, text="Opintosuunnitelman nimi:").pack()
        self._plan_name_entry = Entry(self)
        self._plan_name_entry.pack(pady=5)

        Label(self, text="Tavoite opintopistemäärä:").pack()
        self._goal_credits_entry = Entry(self)
        self._goal_credits_entry.insert(0, "180")
        self._goal_credits_entry.pack(pady=5)

        self._message_label = Label(self, text="", foreground="red")
        self._message_label.pack(pady=5)

        Button(
            self, text="Tallenna", command=self._save_studyplan, bootstyle="success"
        ).pack(pady=10)
        Button(
            self, text="Takaisin", command=self._handle_back, bootstyle="secondary"
        ).pack(pady=10)

    def _save_studyplan(self):
        plan_name = self._plan_name_entry.get().strip()
        goal_credits = self._goal_credits_entry.get().strip()

        success, result = self._studyplan_service.create_studyplan(
            self._logged_user, plan_name, goal_credits
        )

        if success:
            self._handle_back()
        else:
            self.show_message(result)

    def show_message(self, message):
        self._message_label.config(text=message, foreground="red")
        self.after(3000, lambda: self._message_label.config(text=""))
