from tkinter import Tk
from ttkbootstrap import Style
from services.user_service import user_service
from services.authentication_service import auth_service
from services.course_service import course_service
from services.studyplan_service import studyplan_service
from services.academicyear_service import academicyear_service
from services.period_service import period_service

from ui.ui import UI


def main():
    window = Tk()
    window.title("Opintojenseurantasovellus Gifu")
    window.geometry("1000x600")

    style = Style(theme="sandstone")
    window.tk_setPalette(background=style.colors.primary)
    style.configure(".", font=("Helvetica Neue", 13))

    ui = UI(
        window,
        user_service,
        auth_service,
        course_service,
        studyplan_service,
        academicyear_service,
        period_service,
    )
    ui.start()

    window.mainloop()


if __name__ == "__main__":
    main()
