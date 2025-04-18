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

        Button(
            self, text="Tallenna", command=self._save_studyplan, bootstyle="success"
        ).pack(pady=10)
        Button(
            self, text="Takaisin", command=self._handle_back, bootstyle="secondary"
        ).pack(pady=10)

    def _save_studyplan(self):
        plan_name = self._plan_name_entry.get().strip()
        if plan_name:
            self._studyplan_service.create_studyplan(self._logged_user, plan_name)
            self._handle_back()
