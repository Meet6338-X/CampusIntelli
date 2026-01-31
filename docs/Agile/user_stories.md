# User Stories
## CampusIntelli Portal - Detailed Story Cards

---

## Story Format
Each story follows the standard format:
> **As a** [role], **I want to** [goal], **So that** [benefit]

---

## Authentication Stories

### US-1.1: User Login

```
┌──────────────────────────────────────────────────┐
│  USER STORY                           Sprint: 1  │
├──────────────────────────────────────────────────┤
│  As a registered user                            │
│  I want to log in with my email and password     │
│  So that I can access my personalized dashboard  │
├──────────────────────────────────────────────────┤
│  ACCEPTANCE CRITERIA                             │
│  ☐ Login form with email and password fields     │
│  ☐ Form validation (required, email format)      │
│  ☐ Error message for invalid credentials         │
│  ☐ Success redirects to role-based dashboard     │
│  ☐ Session token stored securely                 │
│  ☐ "Remember me" option (optional)               │
├──────────────────────────────────────────────────┤
│  POINTS: 5   │  PRIORITY: High   │  RISK: Low   │
└──────────────────────────────────────────────────┘
```

---

### US-1.2: Role-Based Dashboard

```
┌──────────────────────────────────────────────────┐
│  USER STORY                           Sprint: 1  │
├──────────────────────────────────────────────────┤
│  As a logged-in user                             │
│  I want to see a dashboard tailored to my role   │
│  So that I can quickly access relevant features  │
├──────────────────────────────────────────────────┤
│  ACCEPTANCE CRITERIA                             │
│  STUDENT DASHBOARD:                              │
│  ☐ Today's classes                               │
│  ☐ Upcoming assignments (due soon)              │
│  ☐ Recent grades                                 │
│  ☐ Attendance summary                            │
│  ☐ Quick links: Timetable, Assignments, Booking │
│                                                  │
│  FACULTY DASHBOARD:                              │
│  ☐ Today's lectures                              │
│  ☐ Pending submissions to grade                  │
│  ☐ Generate QR button                            │
│  ☐ Quick links: Courses, Grading, Analytics     │
│                                                  │
│  ADMIN DASHBOARD:                                │
│  ☐ System statistics (users, courses)           │
│  ☐ Recent activity log                           │
│  ☐ Quick links: Users, Reports, Settings        │
├──────────────────────────────────────────────────┤
│  POINTS: 8   │  PRIORITY: High   │  RISK: Med   │
└──────────────────────────────────────────────────┘
```

---

### US-1.3: User Logout

```
┌──────────────────────────────────────────────────┐
│  USER STORY                           Sprint: 1  │
├──────────────────────────────────────────────────┤
│  As a logged-in user                             │
│  I want to log out of my account                 │
│  So that my session is securely terminated       │
├──────────────────────────────────────────────────┤
│  ACCEPTANCE CRITERIA                             │
│  ☐ Logout button in navigation/profile menu      │
│  ☐ Clears session token                          │
│  ☐ Clears cached user data                       │
│  ☐ Redirects to login page                       │
│  ☐ Shows "Logged out successfully" message       │
├──────────────────────────────────────────────────┤
│  POINTS: 2   │  PRIORITY: High   │  RISK: Low   │
└──────────────────────────────────────────────────┘
```

---

## Academic Stories

### US-3.2: Submit Assignment

```
┌──────────────────────────────────────────────────┐
│  USER STORY                           Sprint: 2  │
├──────────────────────────────────────────────────┤
│  As a student                                    │
│  I want to upload my assignment submission       │
│  So that it's recorded before the deadline       │
├──────────────────────────────────────────────────┤
│  ACCEPTANCE CRITERIA                             │
│  ☐ Select assignment from list                   │
│  ☐ View assignment details and due date          │
│  ☐ File upload button (drag & drop optional)     │
│  ☐ Accepted formats: PDF, DOC, DOCX, ZIP        │
│  ☐ Max file size: 10MB                           │
│  ☐ Progress indicator during upload              │
│  ☐ Success confirmation with timestamp           │
│  ☐ Late submission flagged if after due date     │
│  ☐ Option to resubmit (replaces previous)        │
├──────────────────────────────────────────────────┤
│  DEV NOTES                                       │
│  - Validate file type on both client and server  │
│  - Store files in uploads/ with unique names     │
│  - Update submission record in database          │
├──────────────────────────────────────────────────┤
│  POINTS: 8   │  PRIORITY: High   │  RISK: Med   │
└──────────────────────────────────────────────────┘
```

---

### US-3.4: Grade Submissions

```
┌──────────────────────────────────────────────────┐
│  USER STORY                           Sprint: 2  │
├──────────────────────────────────────────────────┤
│  As a faculty member                             │
│  I want to grade student submissions             │
│  So that students receive marks and feedback     │
├──────────────────────────────────────────────────┤
│  ACCEPTANCE CRITERIA                             │
│  ☐ View list of submissions for assignment       │
│  ☐ Show student name, submission time, status    │
│  ☐ Download/preview submitted file               │
│  ☐ Enter marks (0 to max_marks)                  │
│  ☐ Add text feedback                             │
│  ☐ Save grade (individual)                       │
│  ☐ Grade letter auto-calculated                  │
│  ☐ Bulk actions (optional): grade all present    │
│  ☐ Student notified of grade                     │
├──────────────────────────────────────────────────┤
│  POINTS: 8   │  PRIORITY: High   │  RISK: Med   │
└──────────────────────────────────────────────────┘
```

---

## Attendance Stories

### US-7.1: Generate QR Code

```
┌──────────────────────────────────────────────────┐
│  USER STORY                           Sprint: 4  │
├──────────────────────────────────────────────────┤
│  As a faculty member                             │
│  I want to generate a QR code for my lecture     │
│  So that students can mark their attendance      │
├──────────────────────────────────────────────────┤
│  ACCEPTANCE CRITERIA                             │
│  ☐ Select course and lecture from dropdown       │
│  ☐ Click "Generate QR" button                    │
│  ☐ QR code displayed (large, scannable)          │
│  ☐ Countdown timer (5 minutes default)           │
│  ☐ QR contains: course_id, lecture_id, timestamp │
│  ☐ QR auto-expires after countdown               │
│  ☐ Option to regenerate new QR                   │
│  ☐ View students who marked attendance           │
├──────────────────────────────────────────────────┤
│  SECURITY NOTES                                  │
│  - QR code is time-bound (5 min expiry)          │
│  - Unique code per session (not reusable)        │
│  - Consider location verification (future)       │
├──────────────────────────────────────────────────┤
│  POINTS: 8   │  PRIORITY: High   │  RISK: High  │
└──────────────────────────────────────────────────┘
```

---

### US-7.2: Scan QR for Attendance

```
┌──────────────────────────────────────────────────┐
│  USER STORY                           Sprint: 4  │
├──────────────────────────────────────────────────┤
│  As a student                                    │
│  I want to scan a QR code to mark attendance     │
│  So that my presence is recorded automatically   │
├──────────────────────────────────────────────────┤
│  ACCEPTANCE CRITERIA                             │
│  ☐ "Mark Attendance" button on dashboard         │
│  ☐ Opens camera/QR scanner                       │
│  ☐ Scans and decodes QR data                     │
│  ☐ Validates: QR not expired, student enrolled   │
│  ☐ Success: "Attendance marked!" message         │
│  ☐ Error: "QR expired" or "Already marked"       │
│  ☐ Works on mobile browsers                      │
├──────────────────────────────────────────────────┤
│  EDGE CASES                                      │
│  - QR expired: Show "Contact faculty" message    │
│  - Already marked: Prevent duplicate entry       │
│  - Not enrolled: Deny with error message         │
├──────────────────────────────────────────────────┤
│  POINTS: 8   │  PRIORITY: High   │  RISK: High  │
└──────────────────────────────────────────────────┘
```

---

## Booking Stories

### US-5.2: Book a Room

```
┌──────────────────────────────────────────────────┐
│  USER STORY                           Sprint: 3  │
├──────────────────────────────────────────────────┤
│  As a user (student or faculty)                  │
│  I want to reserve a room for a time slot        │
│  So that it's available for my use               │
├──────────────────────────────────────────────────┤
│  ACCEPTANCE CRITERIA                             │
│  ☐ Select date from calendar                     │
│  ☐ Select time slot (1-hour blocks)              │
│  ☐ View available rooms with capacity info       │
│  ☐ Select preferred room                         │
│  ☐ Enter booking purpose                         │
│  ☐ Confirm booking                               │
│  ☐ Receive confirmation (on-screen + email)      │
│  ☐ Booking appears in "My Bookings"              │
├──────────────────────────────────────────────────┤
│  BUSINESS RULES                                  │
│  - Max booking: 2 hours per day per user         │
│  - Advance booking: up to 7 days ahead           │
│  - Cancellation: up to 2 hours before start      │
├──────────────────────────────────────────────────┤
│  POINTS: 8   │  PRIORITY: High   │  RISK: Med   │
└──────────────────────────────────────────────────┘
```

---

## Story Summary by Epic

| Epic | Stories | Total Points |
|------|---------|--------------|
| Authentication | 4 | 20 |
| Academic - Timetable | 2 | 8 |
| Academic - Assignments | 4 | 24 |
| Academic - Grades | 1 | 5 |
| Campus - Booking | 3 | 16 |
| Campus - Announcements | 2 | 8 |
| Attendance - QR | 2 | 16 |
| Analytics | 1 | 8 |
| Administration | 1 | 8 |

**Total Story Points**: 113

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-31
