from ttkbootstrap import Frame, Label, Entry, Button


class LoginView(Frame):
    def __init__(self, root, auth_service, handle_back):
        super().__init__(root)
        self.auth_service = auth_service
        self.handle_back = handle_back

        self.create_widgets()

    def create_widgets(self):
        Label(self, text="Kirjaudu sisään", bootstyle="secondary").pack(pady=10)

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

        self.login_button = Button(
            self,
            text="Kirjaudu sisään",
            bootstyle="success",
            width=20,
            command=self.login,
        )
        self.login_button.pack(pady=10)

        self.back_button = Button(
            self,
            text="Takaisin",
            bootstyle="secondary",
            width=20,
            command=self.handle_back,
        )
        self.back_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_label.config(
                text="Käyttäjätunnus ja salasana eivät voi olla tyhjiä!"
            )
            return

        user = self.auth_service.log_in(username, password)

        if user:
            self.handle_back()
        else:
            self.error_label.config(text="Väärä käyttäjätunnus tai salasana.")
