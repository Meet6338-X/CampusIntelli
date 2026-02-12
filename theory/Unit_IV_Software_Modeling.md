# Unit IV: Software Modeling - Static and Dynamic

**Duration**: 5 hours

---

## 1. Introduction to Software Modeling

### What is Modeling?

```mermaid
graph TD
    A[Software Modeling] --> B[Static Modeling]
    A --> C[Dynamic Modeling]
    
    B --> B1[Structure]
    B --> B2[Classes/Objects]
    B --> B3[Relationships]
    
    C --> C1[Behavior]
    C --> C2[Interactions]
    C --> C3[Flow]
```

---

## 2. Static Modeling

### A. Use Case Diagram

#### Purpose
Shows actors, use cases, and their relationships to visualize system functionality.

#### Components

```mermaid
graph TB
    subgraph "Use Case Notation"
        A[Use Case] -.-> B[Actor]
        A --> C[System Boundary]
    end
    
    subgraph "Relationships"
        D[Include]
        E[Extend]
        F[Generalization]
    end
```

#### Use Case Diagram Example

```mermaid
graph TB
    subgraph "CampusIntelli System"
        UC1[Login]
        UC2[View Dashboard]
        UC3[Submit Assignment]
        UC4[Grade Assignment]
        UC5[Generate QR]
        UC6[Scan QR]
    end
    
    Student((Student))
    Faculty((Faculty))
    
    Student --> UC1
    Student --> UC2
    Student --> UC3
    Faculty --> UC1
    Faculty --> UC2
    Faculty --> UC4
    Faculty --> UC5
    Student --> UC6
    
    UC4 ..> UC5 : extends
```

#### Relationships

| Relationship | Notation | Meaning |
|--------------|----------|---------|
| Include | <<include>> | Mandatory inclusion |
| Extend | <<extend>> | Optional extension |
| Generalization | ─▷ | Inheritance |

---

### B. Class Diagram

#### Purpose
Shows classes, attributes, methods, and relationships in the system structure.

#### Class Notation

```
┌───────────────────────────────────────┐
│           Class Name                  │
├───────────────────────────────────────┤
│  - privateAttribute: Type             │
│  # protectedAttribute: Type           │
│  + publicAttribute: Type              │
├───────────────────────────────────────┤
│  + publicMethod(): ReturnType         │
│  # protectedMethod(): ReturnType      │
│  - privateMethod(): ReturnType        │
└───────────────────────────────────────┘
```

#### Relationships

| Symbol | Relationship | Description |
|--------|--------------|-------------|
| ──█ | Inheritance | A is-a B |
| ──◇ | Composition | A owns B (strong) |
| ──◇ | Aggregation | A has B (weak) |
| ──▷ | Association | A knows B |

#### Class Diagram Example

```mermaid
classDiagram
    class User {
        +String id
        +String email
        +String name
        +login()
        +logout()
    }
    
    class Student {
        +String rollNumber
        +enrolledCourses
        +submitAssignment()
    }
    
    class Faculty {
        +String department
        +assignedCourses
        +gradeSubmission()
    }
    
    class Course {
        +String code
        +String name
        +List~Student~ students
        +List~Assignment~ assignments
    }
    
    User <|-- Student
    User <|-- Faculty
    Course "1" --> "*" Student : enrolls
    Course "1" --> "*" Assignment : contains
```

---

### C. Component Diagram

#### Purpose
Shows the organization of physical software components and their dependencies.

#### Example

```mermaid
graph TB
    subgraph "Frontend"
        UI[User Interface]
        JS[JavaScript]
        CSS[Stylesheets]
    end
    
    subgraph "Backend"
        API[REST API]
        Auth[Authentication]
        Business[Business Logic]
    end
    
    subgraph "Database"
        DB[(Database)]
    end
    
    UI --> JS
    JS --> CSS
    UI --> API
    API --> Auth
    API --> Business
    Business --> DB
```

---

### D. Deployment Diagram

#### Purpose
Shows the physical deployment of software components on hardware nodes.

#### Example

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Browser]
    end
    
    subgraph "Application Layer"
        Server[Application Server]
        API[API Server]
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL)]
        Cache[Redis Cache]
    end
    
    Browser --> Server
    Server --> API
    API --> DB
    API --> Cache
    
    Server -->|Deploys| Container[Docker Container]
```

---

## 3. Dynamic Modeling

### A. Sequence Diagram

#### Purpose
Shows object interactions in a sequential order (message flow over time).

#### Components

| Symbol | Description |
|--------|-------------|
| ▭ | Lifeline (object) |
| ──▷ | Synchronous message |
| ──▷ | Asynchronous message |
| ──▷ | Return message |
| ⬜ | Activation box |
| ∥∥ | Alt (alternative) |

#### Sequence Diagram Example: Login

```mermaid
sequenceDiagram
    participant U as User
    participant UI as LoginPage
    participant Auth as AuthService
    participant DB as Database
    
    U->>UI: Enter credentials
    UI->>Auth: login(email, password)
    Auth->>DB: validateUser(email)
    DB-->>Auth: user data
    Auth->>Auth: verifyPassword()
    
    alt Success
        Auth-->>UI: {token, user}
        UI-->>U: Show Dashboard
    else Failure
        Auth-->>UI: Error
        UI-->>U: Show Error
    end
```

---

### B. Communication Diagram

#### Purpose
Shows object relationships and messages between them (emphasizes connections).

#### Example

```mermaid
graph LR
    S[Student] --> AS[AssignmentSystem]
    AS --> DB[Database]
    F[Faculty] --> AS
    AS --> F
    AS --> C[CourseSystem]
    C --> DB
```

---

### C. Activity Diagram

#### Purpose
Shows the flow of control between activities (business processes).

#### Components

| Symbol | Description |
|--------|-------------|
| ⬭ | Start node |
| ◉ | End node |
| ▭ | Activity |
| ◇ | Decision |
| ▷ | Control flow |

#### Activity Diagram Example: Assignment Submission

```mermaid
flowchart TB
    Start((Start)) --> A[Student views assignment]
    A --> B{Due date check}
    B -->|Before| C[Upload file]
    B -->|After| D[Mark as late]
    C --> E{Valid format?}
    E -->|Yes| F[Save submission]
    E -->|No| G[Show error]
    G --> C
    F --> H[Confirm success]
    D --> C
    H --> End((End))
```

---

### D. Interaction Overview Diagram

#### Purpose
Shows sequence of interactions between multiple scenarios.

#### Example

```mermaid
flowchart TD
    A[Login Flow] --> B[Dashboard Flow]
    B --> C[Assignment Flow]
    C --> D[Submission Flow]
```

---

## 4. UML Diagram Summary

| Diagram | Type | Purpose |
|---------|------|---------|
| Use Case | Static | Functional requirements |
| Class | Static | System structure |
| Component | Static | Component organization |
| Deployment | Static | Physical deployment |
| Sequence | Dynamic | Object interactions |
| Communication | Dynamic | Message flow |
| Activity | Dynamic | Business process |
| Interaction | Dynamic | Sequence overview |

---

## 5. UML in Practice

### Diagram Selection Guide

```mermaid
graph TD
    A[What to Model?] --> B[Structure?]
    A --> C[Behavior?]
    
    B --> D[Classes?] --> E[Class Diagram]
    B --> F[Components?] --> G[Component Diagram]
    B --> H[Deployment?] --> I[Deployment Diagram]
    B --> J[Use Cases?] --> K[Use Case Diagram]
    
    C --> L[Message flow?] --> M[Sequence Diagram]
    C --> N[Process flow?] --> O[Activity Diagram]
    C --> P[Collaboration?] --> Q[Communication Diagram]
```

---

## 6. Summary

| Modeling Type | Key Diagrams | Focus |
|---------------|--------------|-------|
| **Static** | Use Case, Class, Component, Deployment | Structure, relationships |
| **Dynamic** | Sequence, Communication, Activity | Behavior, interactions |

---

## 7. Practical Exercise

### Questions
1. Draw a use case diagram for a library management system.
2. What is the difference between composition and aggregation in class diagrams?
3. Draw a sequence diagram for the "Withdraw Money" ATM transaction.
4. Explain when to use activity diagrams vs sequence diagrams.
5. Draw a class diagram for an online shopping system with Customer, Order, and Product classes.

### Assignment
Create UML diagrams for CampusIntelli:
- Use Case Diagram (main actors and use cases)
- Class Diagram (key classes and relationships)
- Sequence Diagram (user login process)

---

**Unit Completed**: [ ] Yes [ ] No  
**Date**: _____________  
**Signature**: _____________
