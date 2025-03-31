from services.user_service import user_service
from services.authentication_service import auth_service


class UI:
    def __init__(self, user_service, auth_service):
        self.user_service = user_service
        self.auth_service = auth_service

    def run(self):
        while True:
            print("\n1) Luo käyttäjä")
            print("2) Listaa käyttäjät")

            if self.auth_service.get_logged_in_user():
                print("3) Kirjaudu ulos")
            else:
                print("3) Kirjaudu sisään")

            print("4) Poistu")
            choice = input("Valitse toiminto: ")

            if choice == "1":
                self.create_user()

            elif choice == "2":
                self.list_users()

            elif choice == "3":
                if self.auth_service.get_logged_in_user():
                    self.log_out()
                else:
                    self.log_in()

            elif choice == "4":
                break
            else:
                print("Virheellinen valinta.")

    def create_user(self):
        username = input("Anna käyttäjänimi: ")
        password = input("Anna salasana: ")
        try:
            user = self.user_service.create_user(username, password)
            print(f"Käyttäjä {user.username} luotu!")
        except ValueError as e:
            print(e)

    def list_users(self):
        users = self.user_service.get_all_users()
        for user in users:
            print(f"{user.username}")

    def log_in(self):
        username = input("Anna käyttäjätunnus: ")
        password = input("Anna salasana: ")
        user = self.auth_service.log_in(username, password)

        if user:
            print(f"Käyttäjä {username} on nyt kirjautunut sisään.")
        else:
            print("Väärä käyttäjätunnus tai salasana.")

    def log_out(self):
        self.auth_service.log_out()
        print("Olet kirjautunut ulos.")


ui = UI(user_service, auth_service)
