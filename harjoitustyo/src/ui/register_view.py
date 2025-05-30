from ttkbootstrap import Frame, Label, Entry, Button


class RegisterView(Frame):
    def __init__(self, root, user_service, handle_back):
        super().__init__(root)
        self.user_service = user_service
        self.handle_back = handle_back

        self._create_widgets()

    def _create_widgets(self):
        Label(self, text="Rekisteröidy", bootstyle="secondary").pack(pady=10)

        self.username_label = Label(self, text="Käyttäjänimi:")
        self.username_label.pack()
        self.username_entry = Entry(self)
        self.username_entry.pack(pady=5)

        self.password_label = Label(self, text="Salasana:")
        self.password_label.pack()
        self.password_entry = Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.error_label = Label(self, text="", foreground="red", bootstyle="danger")
        self.error_label.pack(pady=5)

        self.register_button = Button(
            self,
            text="Luo tili",
            bootstyle="success",
            width=20,
            command=self.create_user,
        )
        self.register_button.pack(pady=10)

        self.back_button = Button(
            self,
            text="Takaisin",
            bootstyle="secondary",
            width=20,
            command=self.handle_back,
        )
        self.back_button.pack(pady=5)

    def create_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_label.config(
                text="Käyttäjätunnus ja salasana eivät voi olla tyhjiä!"
            )
            return

        success, result = self.user_service.create_user(username, password)

        if success:
            self.error_label.config(
                text=f"Käyttäjä {result.username} luotu onnistuneesti!",
                foreground="green",
            )
            self.after(2000, self.handle_back)
        else:
            self.error_label.config(text=result)
