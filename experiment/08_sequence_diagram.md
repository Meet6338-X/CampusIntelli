# Experiment 8: Analytical Sequence Diagram

## Objective
To prepare analytical sequence diagram.

---

## 1. Understanding Sequence Diagrams

### What is a Sequence Diagram?
A sequence diagram is an interaction diagram that shows how objects interact in a particular scenario, emphasizing the chronological order of messages.

### Key Components

| Symbol | Name | Description |
|--------|------|-------------|
| ▭ | Lifeline | Vertical line representing object existence |
| ▽ | Message | Arrow showing communication |
| ⬜ | Activation | Rectangle showing method execution |
| ∥∥ | Alt | Alternative paths (if-else) |
| ∗∗ | Loop | Repeated execution |

### Message Types

| Type | Syntax | Description |
|------|--------|-------------|
| Synchronous | ──▷ | Caller waits for response |
| Asynchronous | ──▷ | Caller continues without waiting |
| Return | ──▷ | Response to a message |
| Self | ──▷ | Object calls itself |

---

## 2. Sequence Diagram: User Login

```mermaid
sequenceDiagram
    participant U as User
    participant UI as LoginPage
    participant AC as AuthController
    participant AS as AuthService
    participant DB as Database

    U->>UI: Enter email/password
    UI->>AC: submitLogin(email, password)
    AC->>AS: authenticate(email, password)
    AS->>DB: findUserByEmail(email)
    DB-->>AS: user data
    AS->>AS: verifyPassword(password, hash)
    
    alt Password Valid
        AS->>AS: createSession(user)
        AS-->>AC: {success: true, token, role}
        AC-->>UI: redirectToDashboard(role)
        UI-->>U: Display Dashboard
    else Password Invalid
        AS-->>AC: {success: false, error}
        AC-->>UI: showError("Invalid credentials")
        UI-->>U: Display Error
    end
```

---

## 3. Sequence Diagram: Assignment Submission

```mermaid
sequenceDiagram
    participant S as Student
    participant UI as AssignmentPage
    participant AC as AssignmentController
    participant VS as ValidationService
    participant SS as StorageService
    participant DB as Database

    S->>UI: Select assignment
    UI->>AC: getAssignmentDetails(id)
    AC->>DB: fetchAssignment(id)
    DB-->>AC: assignment data
    AC-->>UI: Display assignment details

    S->>UI: Upload file
    UI->>AC: submitAssignment(file, assignmentId)
    AC->>VS: validateFile(file)
    VS->>VS: checkFormat()
    VS->>VS: checkSize()
    
    alt Valid File
        VS-->>AC: {valid: true}
        AC->>SS: saveFile(file)
        SS-->>AC: filePath
        AC->>DB: createSubmission(studentId, assignmentId, filePath)
        DB-->>AC: submission record
        AC-->>UI: showSuccess("Submitted!")
        UI-->>S: Display confirmation
    else Invalid File
        VS-->>AC: {valid: false, error}
        AC-->>UI: showError(error)
        UI-->>S: Display error
    end
```

---

## 4. Sequence Diagram: QR Attendance Marking

```mermaid
sequenceDiagram
    participant F as Faculty
    participant FUI as FacultyUI
    participant QC as QRController
    participant QS as QRService
    participant DB as Database
    participant S as Student
    participant SUI as StudentUI
    participant AS as AttendanceService

    Note over F,DB: QR Generation Phase
    F->>FUI: Click "Generate QR"
    FUI->>QC: generateQR(courseId, lectureId)
    QC->>QS: createQRCode()
    QS->>QS: generateUniqueCode()
    QS->>QS: setExpiry(5 minutes)
    QS->>DB: saveQRCode(code, expiry)
    DB-->>QS: qr record
    QS-->>QC: qrCodeImage
    QC-->>FUI: displayQR(image, countdown)
    FUI-->>F: Show QR with timer

    Note over S,DB: Attendance Marking Phase
    S->>SUI: Open QR Scanner
    SUI->>SUI: activateCamera()
    S->>SUI: Scan QR code
    SUI->>AS: markAttendance(qrData, studentId)
    AS->>QS: validateQR(qrData)
    QS->>DB: getQRCode(qrData)
    DB-->>QS: qr record
    QS->>QS: checkExpiry()
    
    alt QR Valid & Not Expired
        QS-->>AS: {valid: true, courseId}
        AS->>DB: checkDuplicate(studentId, courseId, date)
        alt Not Already Marked
            AS->>DB: createAttendance(studentId, courseId)
            DB-->>AS: attendance record
            AS-->>SUI: showSuccess("Attendance marked!")
            SUI-->>S: Display success
        else Already Marked
            AS-->>SUI: showError("Already marked")
            SUI-->>S: Display error
        end
    else QR Expired
        QS-->>AS: {valid: false, error: "expired"}
        AS-->>SUI: showError("QR expired")
        SUI-->>S: Display error
    end
```

---

## 5. Sequence Diagram: Room Booking

```mermaid
sequenceDiagram
    participant U as User
    participant UI as BookingPage
    participant BC as BookingController
    participant RS as RoomService
    participant BS as BookingService
    participant DB as Database

    U->>UI: Select date/time
    UI->>BC: getAvailableRooms(date, timeSlot)
    BC->>RS: checkAvailability(date, timeSlot)
    RS->>DB: getRoomBookings(date)
    DB-->>RS: bookings list
    RS->>RS: filterAvailable()
    RS-->>BC: available rooms
    BC-->>UI: displayRooms(rooms)
    UI-->>U: Show available rooms

    U->>UI: Select room & confirm
    UI->>BC: createBooking(roomId, userId, timeSlot)
    BC->>BS: validateBooking(roomId, timeSlot)
    BS->>DB: checkConflict(roomId, timeSlot)
    
    alt No Conflict
        DB-->>BS: no conflicts
        BS->>DB: createBooking(details)
        DB-->>BS: booking record
        BS-->>BC: {success: true, bookingId}
        BC-->>UI: showConfirmation(bookingId)
        UI-->>U: Display booking confirmation
    else Conflict Exists
        DB-->>BS: conflict found
        BS-->>BC: {success: false, error}
        BC-->>UI: showError("Slot no longer available")
        UI-->>U: Display error
    end
```

---

## 6. Sequence Diagram: Grade Submission

```mermaid
sequenceDiagram
    participant F as Faculty
    participant UI as GradingPage
    participant GC as GradeController
    participant GS as GradeService
    participant DB as Database
    participant NS as NotificationService

    F->>UI: View submissions
    UI->>GC: getSubmissions(assignmentId)
    GC->>DB: fetchSubmissions(assignmentId)
    DB-->>GC: submissions list
    GC-->>UI: displaySubmissions(list)
    UI-->>F: Show submissions table

    F->>UI: Enter marks & feedback
    UI->>GC: submitGrade(submissionId, marks, feedback)
    GC->>GS: validateGrade(marks, maxMarks)
    
    alt Valid Marks
        GS-->>GC: {valid: true}
        GC->>DB: updateSubmission(submissionId, marks, feedback)
        DB-->>GC: updated record
        GC->>GS: calculateGradeLetter(marks, maxMarks)
        GS-->>GC: grade letter
        GC->>DB: createGradeRecord(studentId, courseId, marks)
        DB-->>GC: grade record
        GC->>NS: notifyStudent(studentId, "Grade posted")
        GC-->>UI: showSuccess("Grade saved")
        UI-->>F: Display success
    else Invalid Marks
        GS-->>GC: {valid: false, error}
        GC-->>UI: showError(error)
        UI-->>F: Display error
    end
```

---

## 7. Sequence Diagram: View Analytics

```mermaid
sequenceDiagram
    participant F as Faculty
    participant UI as AnalyticsPage
    participant AC as AnalyticsController
    participant AS as AnalyticsService
    participant DB as Database

    F->>UI: Select course
    UI->>AC: getAnalytics(courseId)
    
    par Parallel Data Fetch
        AC->>AS: getGradeDistribution(courseId)
        AS->>DB: fetchGrades(courseId)
        DB-->>AS: grades data
        AS-->>AC: gradeDistribution
    and
        AC->>AS: getAttendanceTrends(courseId)
        AS->>DB: fetchAttendance(courseId)
        DB-->>AS: attendance data
        AS-->>AC: attendanceTrends
    and
        AC->>AS: getSubmissionStats(courseId)
        AS->>DB: fetchSubmissions(courseId)
        DB-->>AS: submission data
        AS-->>AC: submissionStats
    end

    AC->>AS: compileReport(all data)
    AS-->>AC: compiled analytics
    AC-->>UI: renderCharts(analytics)
    UI-->>F: Display dashboard with charts
```

---

## 8. Key Patterns Used

| Pattern | Usage | Example |
|---------|-------|---------|
| **Controller** | Handles requests, coordinates services | AuthController, GradeController |
| **Service** | Business logic and validation | AuthService, GradeService |
| **Repository** | Data access abstraction | Database operations |
| **Parallel Processing** | Analytics data fetching | Multiple data fetches simultaneously |
| **Alternative Flows** | Error handling paths | Password invalid, duplicate attendance |

---

## 9. Practical Exercise

### Task 1: Draw Sequence Diagram
Create a sequence diagram for the "Cancel Booking" use case.

### Task 2: Identify Messages
For the User Login sequence, list all messages exchanged between objects.

### Task 3: Add Alternative Flows
Add alternative flow handling to the Room Booking sequence for:
- No available rooms
- User cancellation before confirmation

---

## 10. Summary

| Concept | Description |
|---------|-------------|
| Sequence Diagram | Interaction diagram showing message sequence |
| Lifeline | Vertical line representing object existence |
| Message | Communication between objects |
| Synchronous | Caller waits for response |
| Asynchronous | Caller continues without waiting |
| Alt | Alternative paths (if-else conditions) |
| Loop | Repeated message exchanges |

---

**Experiment Completed**: [ ] Yes [ ] No  
**Date**: _____________  
**Signature**: _____________
