# Exo 1: Hospital Management System

**Business workflow**
1. The patient posts a health problem online.
2. The organizer reads it and consults a doctor.
3. The doctor provides a prescription.
4. The organizer sends the prescription to the patient.
5. The patient pays by check, cash or credit card.
6. The organizer forwards the payment to the doctor.

The organizer is also the administrator: maintains the database, updates the system, issues member IDs and passwords.

---

## Task 1: basic class diagram

The key point: **the patient never talks to the doctor directly**. Everything goes through the organizer, so there are only two associations.

```mermaid
classDiagram
    direction LR
    class Patient {
        -id: int
        -name: str
        -email: str
        -password: str
        +post_problem(description: str) None
        +view_prescription() str
        +pay(amount: float, method: str) None
    }
    class Organizer {
        -id: int
        -name: str
        -password: str
        +read_problem() str
        +consult_doctor(doctor: Doctor) None
        +send_prescription(patient: Patient) None
        +forward_payment(doctor: Doctor) None
        +issue_credentials(user) None
    }
    class Doctor {
        -id: int
        -name: str
        -password: str
        -specialty: str
        +review_problem(description: str) None
        +provide_prescription() str
        +receive_payment(amount: float) None
    }
    Patient "*" -- "1" Organizer : submits problems / pays
    Organizer "*" -- "1..*" Doctor : consults / pays
```

Methods come from the **verbs** of the workflow, placed on the class that **does** the action.

---

## Task 2: complete class diagram (6 classes)

```mermaid
classDiagram
    class Patient {
        -id: int
        -name: str
        -password: str
        +post_problem(description: str) HealthProblem
        +pay(amount: float, payment: Payment) None
    }
    class Organizer {
        -id: int
        -name: str
        +read_problem(problem: HealthProblem) None
        +consult_doctor(problem: HealthProblem, doctor: Doctor) Prescription
        +send_prescription(patient: Patient, prescription: Prescription) None
        +forward_payment(payment: Payment, doctor: Doctor) None
    }
    class Doctor {
        -id: int
        -name: str
        -specialty: str
        +write_prescription(problem: HealthProblem) Prescription
    }
    class HealthProblem {
        -id: int
        -description: str
    }
    class Prescription {
        -id: int
        -content: str
    }
    class Payment {
        <<abstract>>
        -amount: float
        +process()* bool
    }
    class CheckPayment {
        -check_number: str
        +process() bool
    }
    class CashPayment {
        +process() bool
    }
    class CreditCardPayment {
        -card_number: str
        +process() bool
    }

    Patient "1" *-- "*" HealthProblem : owns
    Organizer "1" --> "*" HealthProblem : reviews
    Doctor "1" --> "*" Prescription : writes
    HealthProblem "1" -- "0..1" Prescription : answered by
    Patient "1" --> "*" Payment : makes
    Organizer "1" --> "*" Payment : forwards
    Payment <|-- CheckPayment
    Payment <|-- CashPayment
    Payment <|-- CreditCardPayment
```

**Choices**
- `Patient ◆— HealthProblem` is **composition**: a problem only exists for the patient who posted it.
- Payment types use **inheritance** rather than an enumeration, because each type processes the payment differently (checking a card number vs a check number). An enumeration would fit if only the label changed.

### Sequence diagram: one patient submits a problem, receives a prescription, and pays

```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant D as Doctor
    P->>+O: post_problem(description)
    O->>O: read_problem(problem)
    O->>+D: consult_doctor(problem)
    D-->>-O: prescription
    O->>P: send_prescription(prescription)
    deactivate O
    P->>+O: pay(amount, CreditCardPayment)
    O->>O: payment.process()
    O->>D: forward_payment(payment)
    O-->>-P: receipt
```

---

## Task 3: advanced design

- **`User` superclass**: `Patient`, `Doctor` and `Organizer` repeated `id`, `name`, `password`, so they move into an abstract `User` with `login()` / `logout()`.
- **Payment strategy with polymorphism**: `Payment` delegates to a `PaymentMethod` interface; the organizer calls `method.pay(amount)` without knowing the concrete type (the **Strategy** pattern).
- **Status tracking**: `HealthProblemStatus` enumeration (pending, in review, resolved).
- **Timestamps and history**: `created_at` / `issued_at`, and a prescription can reference the previous one.

```mermaid
classDiagram
    class User {
        <<abstract>>
        #id: int
        #name: str
        #password: str
        +login(password: str) bool
        +logout() None
    }
    class Patient {
        +post_problem(description: str) HealthProblem
        +pay(payment: Payment) None
        +prescription_history() list
    }
    class Doctor {
        -specialty: str
        +write_prescription(problem: HealthProblem) Prescription
    }
    class Organizer {
        +register_member(name: str, role: str) User
        +update_system() None
        +read_problem(problem: HealthProblem) None
        +consult_doctor(problem: HealthProblem, doctor: Doctor) Prescription
        +send_prescription(patient: Patient, prescription: Prescription) None
        +forward_payment(payment: Payment, doctor: Doctor) None
    }
    class HealthProblem {
        -id: int
        -description: str
        -created_at: datetime
        -status: HealthProblemStatus
        +set_status(status: HealthProblemStatus) None
    }
    class HealthProblemStatus {
        <<enumeration>>
        PENDING
        IN_REVIEW
        RESOLVED
    }
    class Prescription {
        -id: int
        -content: str
        -issued_at: datetime
    }
    class Payment {
        -amount: float
        -paid_at: datetime
        -method: PaymentMethod
        +execute() bool
    }
    class PaymentMethod {
        <<interface>>
        +pay(amount: float)* bool
    }
    class CheckPayment {
        -check_number: str
        +pay(amount: float) bool
    }
    class CashPayment {
        +pay(amount: float) bool
    }
    class CreditCardPayment {
        -card_number: str
        +pay(amount: float) bool
    }

    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    Patient "1" *-- "*" HealthProblem : owns
    HealthProblem --> HealthProblemStatus
    Organizer "1" --> "*" HealthProblem : reviews
    Doctor "1" --> "*" Prescription : writes
    HealthProblem "1" -- "0..*" Prescription : answered by
    Prescription "0..1" --> "0..1" Prescription : previous
    Patient "1" --> "*" Payment : makes
    Payment "*" o-- "1" PaymentMethod : uses
    PaymentMethod <|.. CheckPayment
    PaymentMethod <|.. CashPayment
    PaymentMethod <|.. CreditCardPayment
```

### System sequence diagram 1: patient registration

```mermaid
sequenceDiagram
    actor O as Organizer
    participant S as System
    participant DB as Database
    O->>+S: register_member(name, "patient")
    S->>S: generate id and password
    S->>+DB: save(patient)
    DB-->>-S: ok
    S-->>-O: member id + password
    O->>O: send credentials to the new patient
```

### System sequence diagram 2: consultation flow

```mermaid
sequenceDiagram
    actor P as Patient
    participant S as System
    actor O as Organizer
    actor D as Doctor
    P->>+S: post_problem(description)
    S->>S: create HealthProblem (status PENDING)
    S-->>-P: problem id
    O->>+S: read_problem(id)
    S->>S: set_status(IN_REVIEW)
    S-->>-O: problem
    O->>D: consult_doctor(problem)
    D-->>O: prescription
    O->>+S: send_prescription(patient, prescription)
    S->>S: set_status(RESOLVED)
    S-->>-P: notification: prescription available
```

### System sequence diagram 3: payment processing

```mermaid
sequenceDiagram
    actor P as Patient
    participant S as System
    participant M as PaymentMethod
    actor O as Organizer
    actor D as Doctor
    P->>+S: pay(amount, method)
    S->>+M: pay(amount)
    alt payment accepted
        M-->>S: True
        S-->>P: receipt
        S->>O: payment received
        O->>D: forward_payment(amount)
    else payment refused
        M-->>-S: False
        S-->>-P: error: payment refused
    end
```

---

## Questions to consider

**How would you handle a patient consulting multiple doctors?**
`HealthProblem` → `Prescription` is `1 — 0..*`, and each prescription is linked to the doctor who wrote it. One problem can therefore get opinions from several doctors, and the patient's history gathers all of them. A `Consultation` class (problem + doctor + date) would make it explicit if more data were needed per consultation.

**Should prescriptions be reusable?**
Not as the same object: each prescription is a medical record tied to one patient, one doctor and one date. "Reuse" means **renewal**: a new `Prescription` that references the previous one (the `previous` self-association), so the history stays intact.

**Which design pattern fits the payment system?**
**Strategy**: every payment method implements the same `pay(amount)` interface, and `Payment` delegates to whichever one it holds. Adding Apple Pay means adding one class, without touching existing code (Open/Closed principle). A **Factory** can create the right `PaymentMethod` from the patient's choice.

**How do you ensure data integrity when payments are processed?**
Make the payment **atomic**: save it and update its status in a single database transaction, so a crash never leaves a half-recorded payment. Only forward money to the doctor once the payment is confirmed (`alt` block above), give each payment a unique id so it can't be processed twice, and keep an audit log with timestamps.
