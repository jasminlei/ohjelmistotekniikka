## Sovelluksen arkkitehtuuri

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

```mermaid
classDiagram
    class User
    class StudyPlan
    class AcademicYear
    class Period
    class Course

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
