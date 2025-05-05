## Viikko 3

- Lisätty luokat User, Course, UserRepository, CourseRepository, UserService, AuthenticationService, CourseService sekä väliaikainen komentorivi-UI
- Repository-luokat vastaavat käyttäjien ja kurssien tallennuksesta sqlite-tietokantaan, ja service-luokat vastaavat kurssien ja käyttäjien toimintalogiikasta
- Käyttäjä voi luoda käyttäjätunnuksen, kirjautua sisään ja ulos, sekä listata kaikki järjestelmään luodut käyttäjätunnukset
- Kirjautunut käyttäjä voi luoda järjestelmään kursseja sekä listata kaikki lisätyt kurssit
- UserRepositoryn, CourseRepositoryn, UserServicen, AuthenticationService ja CourseServicen tämänhetkiset toiminnot on testattu

## Viikko 4

- Refaktoroitu olemassaolevaa koodia siistimmäksi.
- Lisätty luokat StudyPlan, Period, AcademicYear, StudyPlanRepository, PeriodRepository, AcademicYearRepository, StudyPlanService, PeriodService ja AcademicYearService.
- Lisätty Tkinter-UI, jossa voi tällä hetkellä rekisteröityä, kirjautua sisään, lisätä kursseja, tarkastella lisättyjä kursseja, lisätä opintosuunnitelmia, lisätä opintosuunnitelmiin vuosia, tarkastella kunkin vuoden periodeita.
- Jokaiselle luokalle on tehty testejä tärkeimmistä ominaisuuksista.

## Viikko 5

- Paranneltu UI:ta
- Lisätty testejä
- Refaktroitu koodia
- Tällä hetkellä käyttäjä voi aiempien viikkojen ominaisuuksien lisäksi lisätä kursseja opintosuunnitelmaan tiettyyn periodiin, poistaa kurssin opintosuunnitelmasta ja merkitä kurssin suoritetuksi.

## Viikko 6

- Lisätty StatisticsService luokka
- Lisätty testejä
- Refaktoroitu koodia siistimmäksi ja selkeämmäksi
- Lisätty StudyPlan luokkaan goal_credits
- Lisätty käyttäliittymään mahdollisuus tarkastella erilaisia tilastoja opinnoista (kuten opintopisteiden jakautuminen eri periodeille, keskiarvo, kuinka monta prosenttia suoritettu tavoitteesta)
- Paranneltu ja siistitty käyttöliittymää

## Viikko 7

- Refaktoroitu olemassaolemaa koodia
- Siistitty käyttöliittymää
- Paranneltu testejä
- Lisätty testausdokumentti ja paranneltu olemassaolevaa dokumentaatiota
