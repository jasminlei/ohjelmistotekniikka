from services.user_service import user_service
from services.authentication_service import auth_service
from services.course_service import course_service


class UI:
    def __init__(self, user_service, auth_service, course_service):
        self.user_service = user_service
        self.auth_service = auth_service
        self.course_service = course_service

    def run(self):
        while True:
            print("\n1) Luo käyttäjä")
            print("2) Listaa käyttäjät")

            if self.auth_service.get_logged_in_user():
                print("3) Kirjaudu ulos")
                print("4) Lisää kurssi")
                print("5) Listaa kurssit")
            else:
                print("3) Kirjaudu sisään")

            print("Q) Poistu")

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
            elif choice == "4" and self.auth_service.get_logged_in_user():
                self.add_course()
            elif choice == "5" and self.auth_service.get_logged_in_user():
                self.list_courses()
            elif choice == "Q":
                break
            else:
                print("Virheellinen valinta.")

    def create_user(self):
        username = input("Anna käyttäjänimi: ")
        password = input("Anna salasana: ")
        try:
            user = self.user_service.create_user(username, password)
            print(f"Käyttäjä {user.username} luotu!")
        except ValueError as error:
            print(error)

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

    def add_course(self):
        code = None
        while not code:
            code = input("Anna kurssin koodi: ").strip()
            if not code:
                print("Virhe: Kurssin koodi ei voi olla tyhjä!")

        name = None
        while not name:
            name = input("Anna kurssin nimi: ").strip()
            if not name:
                print("Virhe: Kurssin nimi ei voi olla tyhjä!")

        while True:
            credits = input("Anna kurssin opintopisteet: ")
            try:
                credits = int(credits)
                break
            except ValueError:
                print("Virhe: Opintopisteiden tulee olla numero!")

        description = input("Anna kurssin kuvaus (valinnainen): ")

        try:
            course = self.course_service.add_course(
                code, name, int(credits), description
            )
            print(f"Kurssi {course.name} lisätty!")
        except Exception as error:
            print(f"Virhe: {error}")

    def list_courses(self):
        courses = self.course_service.get_all_courses()
        if not courses:
            print("Ei lisättyjä kursseja.")
        else:
            for course in courses:
                print(f"{course.code} - {course.name} ({course.credits} op)")


ui = UI(user_service, auth_service, course_service)
