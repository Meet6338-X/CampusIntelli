# Product Backlog
## CampusIntelli Portal

---

## Backlog Overview

| Priority | Theme | Epic Count | Story Points |
|----------|-------|------------|--------------|
| 🔴 High | Authentication & Core | 3 | 21 |
| 🟠 Medium | Academic Features | 4 | 34 |
| 🟡 Normal | Campus Services | 3 | 21 |
| 🟢 Low | Analytics & Polish | 4 | 26 |

---

## Epic 1: User Authentication (Sprint 1)

### US-1.1: User Login
**As a** user  
**I want to** log in with my email and password  
**So that** I can access my personalized dashboard

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 5 |
| Sprint | 1 |

**Acceptance Criteria:**
- [ ] User can enter email and password
- [ ] System validates credentials
- [ ] Invalid credentials show error message
- [ ] Successful login redirects to dashboard
- [ ] Session persists for 24 hours

---

### US-1.2: Role-Based Dashboard
**As a** logged-in user  
**I want to** see a dashboard customized for my role  
**So that** I can quickly access relevant features

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 8 |
| Sprint | 1 |

**Acceptance Criteria:**
- [ ] Student sees: Timetable, Assignments, Grades, Attendance
- [ ] Faculty sees: Courses, Grading, QR Generation, Analytics
- [ ] Admin sees: User Management, Reports, Configuration

---

### US-1.3: User Logout
**As a** logged-in user  
**I want to** log out securely  
**So that** my session is terminated

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 2 |
| Sprint | 1 |

**Acceptance Criteria:**
- [ ] Logout button visible in navigation
- [ ] Session cleared on logout
- [ ] Redirected to login page

---

### US-1.4: Profile Management
**As a** user  
**I want to** view and edit my profile  
**So that** my information stays current

| Field | Value |
|-------|-------|
| Priority | 🟠 Medium |
| Story Points | 5 |
| Sprint | 1 |

**Acceptance Criteria:**
- [ ] User can view profile details
- [ ] User can update name and contact info
- [ ] Password change requires current password

---

## Epic 2: Timetable Viewer (Sprint 2)

### US-2.1: View Weekly Timetable
**As a** student or faculty  
**I want to** view my weekly class schedule  
**So that** I can plan my time

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 5 |
| Sprint | 2 |

**Acceptance Criteria:**
- [ ] Shows Monday-Friday schedule
- [ ] Displays course name, time, room
- [ ] Current class highlighted
- [ ] Mobile responsive view

---

### US-2.2: View Monthly Calendar
**As a** user  
**I want to** see a monthly calendar view  
**So that** I can see upcoming events

| Field | Value |
|-------|-------|
| Priority | 🟡 Normal |
| Story Points | 3 |
| Sprint | 2 |

---

## Epic 3: Assignment Management (Sprint 2)

### US-3.1: View Assignments
**As a** student  
**I want to** see all my pending assignments  
**So that** I don't miss deadlines

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 3 |
| Sprint | 2 |

**Acceptance Criteria:**
- [ ] List shows assignment title, course, due date
- [ ] Sorted by due date (nearest first)
- [ ] Status shown: Pending, Submitted, Graded

---

### US-3.2: Submit Assignment
**As a** student  
**I want to** upload my assignment submission  
**So that** it's recorded before the deadline

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 8 |
| Sprint | 2 |

**Acceptance Criteria:**
- [ ] File upload (PDF, DOC, ZIP, max 10MB)
- [ ] Validates file format
- [ ] Confirms successful submission
- [ ] Shows timestamp
- [ ] Late submissions flagged

---

### US-3.3: Create Assignment (Faculty)
**As a** faculty member  
**I want to** create new assignments  
**So that** students can see and submit them

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 5 |
| Sprint | 2 |

**Acceptance Criteria:**
- [ ] Set title, description, due date
- [ ] Set maximum marks
- [ ] Attach reference materials
- [ ] Publish to enrolled students

---

### US-3.4: Grade Submissions (Faculty)
**As a** faculty member  
**I want to** grade student submissions  
**So that** students receive feedback

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 8 |
| Sprint | 2 |

**Acceptance Criteria:**
- [ ] View list of submissions
- [ ] Download/view submitted files
- [ ] Enter marks and feedback
- [ ] Bulk grading option

---

## Epic 4: Gradebook (Sprint 2)

### US-4.1: View Grades
**As a** student  
**I want to** see my grades for all courses  
**So that** I can track my performance

| Field | Value |
|-------|-------|
| Priority | 🟠 Medium |
| Story Points | 5 |
| Sprint | 2 |

---

## Epic 5: Room Booking (Sprint 3)

### US-5.1: View Available Rooms
**As a** user  
**I want to** see available rooms for a date/time  
**So that** I can plan my booking

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 5 |
| Sprint | 3 |

---

### US-5.2: Book a Room
**As a** user  
**I want to** reserve a room for a time slot  
**So that** it's available for my use

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 8 |
| Sprint | 3 |

---

### US-5.3: Cancel Booking
**As a** user  
**I want to** cancel my booking  
**So that** the room is available for others

| Field | Value |
|-------|-------|
| Priority | 🟠 Medium |
| Story Points | 3 |
| Sprint | 3 |

---

## Epic 6: Announcements (Sprint 3)

### US-6.1: View Announcements
**As a** user  
**I want to** see campus announcements  
**So that** I stay informed

| Field | Value |
|-------|-------|
| Priority | 🟠 Medium |
| Story Points | 3 |
| Sprint | 3 |

---

### US-6.2: Create Announcement (Admin/Faculty)
**As an** admin or faculty  
**I want to** post announcements  
**So that** users are informed of updates

| Field | Value |
|-------|-------|
| Priority | 🟠 Medium |
| Story Points | 5 |
| Sprint | 3 |

---

## Epic 7: QR Attendance (Sprint 4)

### US-7.1: Generate QR Code (Faculty)
**As a** faculty member  
**I want to** generate a QR code for my lecture  
**So that** students can mark attendance

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 8 |
| Sprint | 4 |

---

### US-7.2: Scan QR for Attendance
**As a** student  
**I want to** scan a QR code to mark attendance  
**So that** my presence is recorded

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 8 |
| Sprint | 4 |

---

## Epic 8: Analytics Dashboard (Sprint 4)

### US-8.1: View Performance Analytics
**As a** user  
**I want to** see performance charts  
**So that** I can understand trends

| Field | Value |
|-------|-------|
| Priority | 🟠 Medium |
| Story Points | 8 |
| Sprint | 4 |

---

## Epic 9: User Management (Sprint 1 & 4)

### US-9.1: Manage Users (Admin)
**As an** admin  
**I want to** add/edit/delete users  
**So that** the system has correct user data

| Field | Value |
|-------|-------|
| Priority | 🔴 High |
| Story Points | 8 |
| Sprint | 1 |

---

## Backlog Summary by Sprint

| Sprint | Stories | Total Points |
|--------|---------|--------------|
| Sprint 1 | 5 | 28 |
| Sprint 2 | 8 | 37 |
| Sprint 3 | 5 | 24 |
| Sprint 4 | 4 | 32 |

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-31
