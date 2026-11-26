# UniManager API

Backend RESTful ad alte prestazioni per la gestione dell'anagrafica accademica, dei corsi, delle iscrizioni e della verbalizzazione dei voti universitari.

## Architettura del Sistema

Il progetto segue una **Layered Architecture** (Architettura a Livelli) per garantire la netta separazione delle responsabilità:

* **API Layer (`app/api`):** Espone gli endpoint REST, gestisce le richieste/risposte HTTP e delega la validazione a Pydantic.
* **Service Layer (`app/services`):** Contiene la *Business Logic* pura (controllo posti disponibili, validazione range voti, calcolo media ponderata e CFU), completamente disaccoppiata dal framework web.
* **Data Layer (`app/models`):** Definisce i modelli ORM tramite SQLAlchemy mappati su PostgreSQL.

### Stack Tecnologico
* **Linguaggio:** Python 3.12+
* **Framework Web:** FastAPI + Uvicorn
* **Validazione Dati:** Pydantic v2
* **Database & ORM:** PostgreSQL 16 + SQLAlchemy 2.0
* **Testing:** Pytest + HTTPX
* **Infrastruttura & CI/CD:** Docker, Docker Compose, GitHub Actions

---

## Modello dei Dati (UML Class Diagram)

L'ereditarietà tra `User`, `Student` e `Professor` è implementata tramite **Joined Table Inheritance** per mantenere il database normalizzato ed evitare campi `NULL` superflui.

```mermaid
classDiagram
    class User {
        +int id
        +str email
        +str full_name
        +str role
    }
    class Student {
        +str matricola
        +int enrollment_year
        +calculate_weighted_average() float
    }
    class Professor {
        +str department
        +str title
    }
    class Course {
        +int id
        +str code
        +str title
        +int cfu
        +int max_students
        +int professor_id
    }
    class Enrollment {
        +int id
        +int student_id
        +int course_id
        +int grade
        +datetime enrolled_at
    }

    User <|-- Student : inherits
    User <|-- Professor : inherits
    Professor "1" --> "0..*" Course : teaches
    Student "1" --> "0..*" Enrollment : has
    Course "1" --> "0..*" Enrollment : includes
```

---

## Flusso di Esecuzione (Sequence Diagram)

Esempio del flusso completo di una richiesta di iscrizione a un corso (`POST /courses/{id}/enroll`):

```mermaid
sequenceDiagram
    actor Client
    participant Router as FastAPI Router
    participant Service as Academic Service
    participant DB as PostgreSQL (SQLAlchemy)

    Client->>Router: POST /courses/10/enroll {"student_id": 42}
    Router->>Service: enroll_student(course_id=10, student_id=42)
    Service->>DB: Verifica esistenza corso, studente e posti liberi
    alt Corso pieno o studente già iscritto
        DB-->>Service: Vincolo violato
        Service-->>Router: Solleva eccezione di dominio
        Router-->>Client: 400 Bad Request
    else Iscrizione valida
        Service->>DB: INSERT INTO enrollments
        DB-->>Service: Record salvato
        Service-->>Router: Oggetto Enrollment
        Router-->>Client: 201 Created (JSON)
    end
```

---

## Contratti delle API Principali

| Metodo | Endpoint | Descrizione | Codici di Risposta |
| :--- | :--- | :--- | :--- |
| `POST` | `/students` | Registra un nuovo studente | `201 Created`, `409 Conflict` |
| `POST` | `/professors` | Registra un nuovo docente | `201 Created`, `409 Conflict` |
| `POST` | `/courses` | Crea un nuovo corso universitario | `201 Created`, `404 Not Found` |
| `POST` | `/courses/{id}/enroll` | Iscrive uno studente a un corso | `201 Created`, `400 Bad Request`, `404 Not Found` |
| `PATCH` | `/enrollments/{id}/grade` | Verbalizza il voto (18-31, dove 31 = 30L) | `200 OK`, `400 Bad Request`, `404 Not Found` |
| `GET` | `/students/{id}/transcript` | Restituisce libretto, CFU e media ponderata | `200 OK`, `404 Not Found` |