# Experiment 7: Analytical Classes and Class Diagram

## Objective
To identify analytical classes and prepare class diagram.

---

## 1. Understanding Class Diagrams

### What is a Class Diagram?
A class diagram is a structural diagram that shows the classes, their attributes, methods, and relationships in a system.

### Class Notation

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

### Relationship Types

| Symbol | Relationship | Description |
|--------|--------------|-------------|
| ──█ | Inheritance | A is-a B |
| ──◇ | Composition | A owns B (strong) |
| ──◇ | Aggregation | A has B (weak) |
| ──▷ | Association | A knows B |
| ──▷ | Realization | A implements B |

---

## 2. Analytical Classes for CampusIntelli

### User Class Hierarchy

```mermaid
classDiagram
    class User {
        +String id
        +String email
        +String password_hash
        +String name
        +String role
        +DateTime created_at
        +DateTime last_login
        +login()
        +logout()
        +updateProfile()
    }

    class Student {
        +String student_id
        +String department
        +int semester
        +List~Course~ enrolled_courses
        +getEnrolledCourses()
        +submitAssignment()
        +viewGrades()
        +markAttendance()
    }

    class Faculty {
        +String faculty_id
        +String department
        +String designation
        +List~Course~ assigned_courses
        +createAssignment()
        +gradeSubmission()
        +generateQRCode()
        +viewAnalytics()
    }

    class Admin {
        +String admin_id
        +manageUsers()
        +configureSystem()
        +generateReports()
    }

    User <|-- Student
    User <|-- Faculty
    User <|-- Admin
```

---

## 3. Complete Class Diagram

```mermaid
classDiagram
    class User {
        +String id
        +String email
        +String password_hash
        +String name
        +String role
        +DateTime created_at
        +DateTime last_login
        +login()
        +logout()
        +updateProfile()
    }

    class Student {
        +String student_id
        +String department
        +int semester
        +List~Course~ enrolled_courses
        +getEnrolledCourses()
        +submitAssignment()
        +viewGrades()
        +markAttendance()
    }

    class Faculty {
        +String faculty_id
        +String department
        +String designation
        +List~Course~ assigned_courses
        +createAssignment()
        +gradeSubmission()
        +generateQRCode()
        +viewAnalytics()
    }

    class Admin {
        +String admin_id
        +manageUsers()
        +configureSystem()
        +generateReports()
    }

    class Course {
        +String id
        +String code
        +String name
        +String description
        +int credits
        +String department
        +Faculty instructor
        +List~Student~ students
        +List~Assignment~ assignments
        +addStudent()
        +removeStudent()
        +getAssignments()
    }

    class Assignment {
        +String id
        +String title
        +String description
        +DateTime due_date
        +int max_marks
        +String course_id
        +List~Submission~ submissions
        +create()
        +update()
        +delete()
        +getSubmissions()
    }

    class Submission {
        +String id
        +String assignment_id
        +String student_id
        +String file_path
        +DateTime submitted_at
        +int marks
        +String feedback
        +bool is_late
        +submit()
        +grade()
    }

    class Timetable {
        +String id
        +String course_id
        +String day
        +Time start_time
        +Time end_time
        +String room_id
        +getSchedule()
    }

    class Room {
        +String id
        +String name
        +String building
        +int capacity
        +String type
        +List~String~ equipment
        +bool is_available
        +checkAvailability()
        +getBookings()
    }

    class Booking {
        +String id
        +String room_id
        +String user_id
        +DateTime start_time
        +DateTime end_time
        +String purpose
        +String status
        +create()
        +cancel()
        +confirm()
    }

    class Attendance {
        +String id
        +String course_id
        +String student_id
        +DateTime date
        +String qr_code
        +bool is_present
        +DateTime marked_at
        +markPresent()
        +validateQR()
    }

    class QRCode {
        +String id
        +String course_id
        +String lecture_id
        +String code_data
        +DateTime generated_at
        +DateTime expires_at
        +bool is_valid
        +generate()
        +validate()
        +expire()
    }

    class Announcement {
        +String id
        +String title
        +String content
        +String author_id
        +DateTime published_at
        +String target_audience
        +bool is_pinned
        +create()
        +update()
        +delete()
    }

    class Material {
        +String id
        +String course_id
        +String title
        +String file_path
        +String file_type
        +DateTime uploaded_at
        +String uploaded_by
        +upload()
        +download()
        +delete()
    }

    class Grade {
        +String id
        +String student_id
        +String course_id
        +String assignment_id
        +int marks
        +String grade_letter
        +DateTime graded_at
        +calculate()
        +update()
    }

    User <|-- Student
    User <|-- Faculty
    User <|-- Admin

    Course "1" --> "*" Assignment : contains
    Course "1" --> "*" Student : enrolls
    Course "1" --> "1" Faculty : taught by
    Course "1" --> "*" Timetable : has schedule
    Course "1" --> "*" Material : has materials

    Assignment "1" --> "*" Submission : receives
    Student "1" --> "*" Submission : submits
    Faculty "1" --> "*" Assignment : creates

    Room "1" --> "*" Booking : has
    User "1" --> "*" Booking : makes
    Timetable "*" --> "1" Room : uses

    Course "1" --> "*" Attendance : tracks
    Student "1" --> "*" Attendance : marks
    QRCode "1" --> "*" Attendance : validates

    Faculty "1" --> "*" QRCode : generates
    User "1" --> "*" Announcement : creates
    Student "1" --> "*" Grade : receives
```

---

## 4. Class Specifications

### User (Abstract Base Class)

| Attribute | Type | Description |
|-----------|------|-------------|
| id | String | Unique identifier (UUID) |
| email | String | User email (unique) |
| password_hash | String | Bcrypt hashed password |
| name | String | Full name |
| role | String | "student", "faculty", "admin" |
| created_at | DateTime | Account creation timestamp |
| last_login | DateTime | Last login timestamp |

| Method | Returns | Description |
|--------|---------|-------------|
| login() | bool | Authenticate user |
| logout() | void | End session |
| updateProfile() | bool | Update user details |

---

### Course

| Attribute | Type | Description |
|-----------|------|-------------|
| id | String | Unique identifier |
| code | String | Course code (e.g., "CS101") |
| name | String | Course title |
| description | String | Course description |
| credits | int | Credit hours |
| department | String | Department name |
| instructor | Faculty | Assigned faculty |
| students | List[Student] | Enrolled students |
| assignments | List[Assignment] | Course assignments |

---

### Assignment

| Attribute | Type | Description |
|-----------|------|-------------|
| id | String | Unique identifier |
| title | String | Assignment title |
| description | String | Instructions |
| due_date | DateTime | Submission deadline |
| max_marks | int | Maximum marks |
| course_id | String | Parent course reference |
| submissions | List[Submission] | Student submissions |

---

### Booking

| Attribute | Type | Description |
|-----------|------|-------------|
| id | String | Unique identifier |
| room_id | String | Room reference |
| user_id | String | Booker reference |
| start_time | DateTime | Booking start |
| end_time | DateTime | Booking end |
| purpose | String | Booking reason |
| status | String | "pending", "confirmed", "cancelled" |

---

### QRCode

| Attribute | Type | Description |
|-----------|------|-------------|
| id | String | Unique identifier |
| course_id | String | Course reference |
| lecture_id | String | Lecture reference |
| code_data | String | Encoded QR data |
| generated_at | DateTime | Generation timestamp |
| expires_at | DateTime | Expiry timestamp (5 min) |
| is_valid | bool | Validity status |

---

## 5. Relationships Summary

| Relationship | Type | Description |
|--------------|------|-------------|
| User ↔ Student/Faculty/Admin | Inheritance | Role-based specialization |
| Course ↔ Assignment | Composition | Course contains assignments |
| Course ↔ Student | Association | Many-to-many enrollment |
| Assignment ↔ Submission | Composition | Assignment has submissions |
| Room ↔ Booking | Composition | Room has bookings |
| QRCode ↔ Attendance | Association | QR validates attendance |

---

## 6. Practical Exercise

### Task 1: Identify Classes
Identify the analytical classes for an Online Library System.

### Task 2: Draw Class Diagram
Draw a class diagram showing:
- Book class
- Member class
- Loan class
- Librarian class
- Appropriate relationships

### Task 3: Add Methods
Add relevant methods to the Room and Booking classes.

---

## 7. Summary

| Concept | Description |
|---------|-------------|
| Class Diagram | Structural diagram showing classes and relationships |
| Class | Blueprint for objects with attributes and methods |
| Attribute | Data fields of a class |
| Method | Functions/behaviors of a class |
| Inheritance | "is-a" relationship between classes |
| Composition | Strong "has-a" relationship |
| Association | Connection between classes |

---

**Experiment Completed**: [ ] Yes [ ] No  
**Date**: _____________  
**Signature**: _____________
