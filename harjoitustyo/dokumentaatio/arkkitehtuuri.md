# Arkkitehtuurikuvaus

Ohjelman rakenne perustuu kerrosarkkitehtuuriin, joka jakautuu neljään pääkerrokseen: UI (käyttöliittymä), services, repositories ja entities.

UI-kerros vastaa ohjelman vuorovaikutuksesta käyttäjän kanssa, services-kerros sisältää sovelluslogiikan, repositories-kerros huolehtii tietokantaoperaatioista, kuten tietojen tallentamisesta, hakemisesta ja poistamisesta, ja entities-kerros määrittelee ohjelman käytössä olevat oliot.

```mermaid
graph TB
    %% UI Package
    subgraph UI [UI]
        direction TB
    end

    %% Services Package
    subgraph Services [Services]
        direction TB
        UserService
        AuthenticationService
        CourseService
        PeriodService
        StudyPlanService
        AcademicYearService
        StatisticsService
    end

    %% Repositories Package
    subgraph Repositories [Repositories]
        direction TB
        CourseRepository
        PeriodRepository
        StudyPlanRepository
        AcademicYearRepository
    end

    %% Entities Package
    subgraph Entities [Entities]
        direction TB
        User
        Course
        Period
        AcademicYear
        StudyPlan
    end

    %% Arrows for dependencies
    UI -.-> Services
    Services -.-> Repositories
    Services -.-> Entities
    Repositories -.-> Entities


```

## Käyttöliittymä

Käyttöliittymä sisältää useita eri näkymiä, jotka on toteutettu omana luokkanaan. Käyttöliittymä on eriytetty sovelluslogiikasta, ja kutsuu services-luokkien metodeita. Käyttöliittymän näkymien näyttämisestä vastaa UI-luokka.

## Sovelluksen arkkitehtuuri

Allaolevasta kuvasta näkee tärkemmin, miten eri luokat toimivat keskenään.

- CourseService vastaa kurssien hallinnasta, kuten kurssien lisäämisestä, poistamisesta, muokkaamisesta ja sijoittamisesta opintojaksoihin.
- PeriodService hallinnoi opintojaksoihin (periodit) liittyviä toimintoja, kuten niiden luomista ja hakemista.
- AcademicYearService käsittelee lukuvuosien logiikkaa ja tarjoaa tietoa eri lukuvuosista ja niiden jaksotuksesta.
- StudyPlanService vastaa opintosuunnitelmien luomisesta ja yhdistää siihen liittyviä kursseja, jaksoja ja lukuvuosia.
- StatisticsService hyödyntää muita service-luokkia tuottaakseen tilastotietoa opintosuunnitelman etenemisestä.

- Kukin service-luokka hyödyntää vastaavaa repository-luokkaa (paitsi StatisticsService, jolla ei ole omaa repositorya) tietokantayhteyksien hallintaan
- Entity-luokat kuvaavat sovelluksen keskeisiä tietorakenteita, eli Course, User, Period, AcademicYear ja StudyPlan.

```mermaid
graph TD
    %% Entities Package
    subgraph Entities [Entities]
        User
        Course
        Period
        AcademicYear
        StudyPlan
    end

    %% Services Package
    subgraph Services [Services]
        UserService
        CourseService
        PeriodService
        StudyPlanService
        AcademicYearService
        StatisticsService
    end

    %% Repositories Package
    subgraph Repositories [Repositories]
        CourseRepository
        PeriodRepository
        StudyPlanRepository
        AcademicYearRepository
    end

    %% Relationships
    StudyPlanService --> StudyPlanRepository
    StudyPlanService --> AcademicYearService
    StudyPlanService --> PeriodService
    StudyPlanService --> CourseService
    CourseService --> CourseRepository
    PeriodService --> PeriodRepository
    AcademicYearService --> AcademicYearRepository
    AcademicYearService --> PeriodService
    StatisticsService --> StudyPlanService
    StatisticsService --> PeriodService
    StatisticsService --> AcademicYearService
    StatisticsService --> CourseService

    StudyPlan --> AcademicYear
    AcademicYear --> Period
    Period --> Course
    User --> StudyPlanService
    User --> UserService

    %% Suhdeluvut tekstinä nuolen viereen
    StudyPlan --> AcademicYear
    AcademicYear --> Period
    Period --> Course
    User --> StudyPlan
```

### Sovelluslogiikka

Allaolevasta kaaviosta näkee käyttäjien, opintosuunnitelmien, vuosien, periodien ja kurssien välisen yhteyden.

- Käyttäjä voi luoda useita opintosuunnitelmia
- Yhteen opintosuunnitelmaan voi lisätä useita vuosia
- Yhdellä vuodella on viisi periodia (1, 2, 3, 4 ja kesä)
- Yhdessä periodssa voi olla rajaton määrä kursseja

```mermaid
classDiagram
    class User {
    username
    password
    id
    }
    class StudyPlan {
    plan_id
    plan_name
    user_id
    goal_credits
    }
    class AcademicYear {
    year_id
    start_year
    end_year
    }
    class Period {
    period_id
    academicyear_id
    period_number
    }

    class Course {
    course_id
    user_id
    code
    name
    credits
    description
    is_completed
    grade
    completion_date
    }

    User "1" --> "1..*" StudyPlan
    StudyPlan "1" --> "1..*" AcademicYear
    AcademicYear "1" --> "5" Period
    Period "1" --> "0..*" Course
```

### Sekvenssikaavio

Kaavio kuvaa, miten käyttäjä luo kurssin ja opintosuunnitelman, lisää kurssin suunnitelmaan ja merkitsee sen suoritetuksi.

```mermaid
sequenceDiagram
    participant Käyttäjä
    participant UI
    participant CourseService
    participant StudyPlanService
    participant AcademicYearService
    participant PeriodService

    Käyttäjä->>UI: Luo kurssi
    UI->>CourseService: add_course("TKT101", "Ohjelmistotekniikka", 5)
    CourseService-->>UI: Kurssi luotu

    Käyttäjä->>UI: Luo opintosuunnitelma
    UI->>StudyPlanService: create_studyplan("Ensisijainen suunnitelma", user_id)
    StudyPlanService-->>UI: Suunnitelma luotu

    Käyttäjä->>UI: Lisää vuosi suunnitelmaan
    UI->>AcademicYearService: create(plan_id, "2024", "2025)
    AcademicYearService->>PeriodService: create(year_id)
    PeriodService-->>AcademicYearService: 5 periodia luotu
    AcademicYearService-->>UI: Vuosi luotu

    Käyttäjä->>UI: Hae kurssit jotka eivät vielä suunnitelmassa
    UI->>CourseService: get_courses_not_in_period(user_id, year_id)
    CourseService-->>UI: Lista kursseista

    Käyttäjä->>UI: Aseta kurssi periodille
    UI->>CourseService: add_course_to_period(course, period)
    CourseService-->>UI: Kurssi asetettu periodille

    Käyttäjä->>UI: Merkitse kurssi suoritetuksi
    UI->>CourseService: mark_as_completed(course_id, "Hyväksytty", "2025-01-01")
    CourseService-->>UI: Kurssi merkitty suoritetuksi

```

Sovelluksen muissakin toiminnallisuuksissa noudatetaan samankaltaista rakennetta: käyttöliittymä reagoi käyttäjän toimintaan kutsumalla jonkin services-luokan metodia. Tämä services-luokka käsittelee tarvittavan sovelluslogiikan ja tekee mahdolliset tietokantakyselyt repositories-luokkien kautta. Kun tarvittavat muutokset on tehty, tieto palautuu services-luokan kautta käyttöliittymälle, joka päivittää näkymän vastaavasti.

## Tietojen tallennus

Sovellus käyttää SQLite tietokantaa. Tietokanta alustetaan initialize_database.py-tiedostossa. Aluksi poistetaan mahdolliset olemassaolevat taulut, ja luodaan sitten seuraavat taulut:

- users: sisältää käyttäjän tiedot (id, käyttäjätunnus, salasana).

- courses: Sisältää kursseja koskevat tiedot (id, käyttäjä-id, kurssikoodi, kurssin nimi, opintopisteet, kuvaus, suoritustiedot kuten arvosana ja suorituspäivämäärä).

- periods: sisältää periodit ja viittaa academicyears-tauluun, jolloin jokainen periodi on yhdistetty johonkin akateemiseen vuoteen suunnitelmassa

- course_periods: yhdistää kurssit tiettyihin periodeihin

- academicyears: sisältää akateemisten vuosien aloitus- ja lopetusvuodet, ja vuosien id:t

- studyplans: Sisältää opintosuunnitelmat (id, nimi, käyttäjän id ja tavoite opintopisteet).

- studyplan_academicyear: yhdistää opintosuunnitelmat ja akateemiset vuodet, jolloin jokainen akateeminen vuosi periodeineen ja kursseineen on sidottu johonkin opintosuunnitelmaan

Kun käyttäjä lisää, muuttaa tai hakee tietoja käyttöliittymässä, services-luokat (esimerkiksi CourseService, StudyPlanService) kutsuvat tietokannan käsittelyyn liittyviä metodeja, jotka sijaitsevat repository-luokissa. Nämä Repository-luokat käsittelevät SQL-kyselyt ja tietokannan muokkaukset.
