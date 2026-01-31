# Sprint Planning
## CampusIntelli Portal - 4-Sprint Execution

---

## Sprint Overview

| Sprint | Duration | Goal | Team Capacity |
|--------|----------|------|---------------|
| Sprint 1 | 2 weeks | User Authentication & Profile | 28 points |
| Sprint 2 | 2 weeks | Academic Core (Timetable, Assignments) | 37 points |
| Sprint 3 | 2 weeks | Campus Services (Booking, Announcements) | 24 points |
| Sprint 4 | 2 weeks | Analytics & QR Attendance | 32 points |

---

## Sprint 1: Authentication & Dashboard

### Sprint Goal
> Deliver secure login system with role-based personalized dashboards for Students, Faculty, and Administrators.

### Sprint Backlog

| ID | Story | Points | Status |
|----|-------|--------|--------|
| US-1.1 | User Login | 5 | 📋 To Do |
| US-1.2 | Role-Based Dashboard | 8 | 📋 To Do |
| US-1.3 | User Logout | 2 | 📋 To Do |
| US-1.4 | Profile Management | 5 | 📋 To Do |
| US-9.1 | User Management (Admin) | 8 | 📋 To Do |

**Total Points**: 28

### Definition of Done
- [ ] All code reviewed and merged
- [ ] Unit tests passing (>80% coverage)
- [ ] Manual testing completed
- [ ] Documentation updated
- [ ] Demo to stakeholders

### Burndown Chart

```
Points │
  30   │█
  25   │█ █
  20   │█ █ █
  15   │█ █ █ █
  10   │█ █ █ █ █
   5   │█ █ █ █ █ █
   0   │█ █ █ █ █ █ █
       └─────────────────
        D1 D2 D3 D4 D5 D6 D7
              Days
```

### Daily Stand-up Template
1. What did I complete yesterday?
2. What will I work on today?
3. Any blockers?

---

## Sprint 2: Academic Core

### Sprint Goal
> Deliver timetable viewer and complete assignment management system (submission and grading).

### Sprint Backlog

| ID | Story | Points | Status |
|----|-------|--------|--------|
| US-2.1 | View Weekly Timetable | 5 | 📋 To Do |
| US-2.2 | View Monthly Calendar | 3 | 📋 To Do |
| US-3.1 | View Assignments | 3 | 📋 To Do |
| US-3.2 | Submit Assignment | 8 | 📋 To Do |
| US-3.3 | Create Assignment | 5 | 📋 To Do |
| US-3.4 | Grade Submissions | 8 | 📋 To Do |
| US-4.1 | View Grades | 5 | 📋 To Do |

**Total Points**: 37

### Key Dependencies
- Sprint 1 authentication must be complete
- File upload system needed for assignments
- Grade calculation logic required

### Technical Tasks
- [ ] Implement file upload service
- [ ] Create assignment data model
- [ ] Build grading interface
- [ ] Add calendar component

---

## Sprint 3: Campus Services

### Sprint Goal
> Deliver room booking system and campus announcement feed.

### Sprint Backlog

| ID | Story | Points | Status |
|----|-------|--------|--------|
| US-5.1 | View Available Rooms | 5 | 📋 To Do |
| US-5.2 | Book a Room | 8 | 📋 To Do |
| US-5.3 | Cancel Booking | 3 | 📋 To Do |
| US-6.1 | View Announcements | 3 | 📋 To Do |
| US-6.2 | Create Announcement | 5 | 📋 To Do |

**Total Points**: 24

### Key Dependencies
- Room data model
- Booking conflict detection
- Calendar integration

### Technical Tasks
- [ ] Room availability algorithm
- [ ] Booking confirmation flow
- [ ] Announcement feed component
- [ ] Admin announcement creation

---

## Sprint 4: Analytics & QR Attendance

### Sprint Goal
> Deliver QR-based attendance system and analytics dashboard. Complete system integration.

### Sprint Backlog

| ID | Story | Points | Status |
|----|-------|--------|--------|
| US-7.1 | Generate QR Code | 8 | 📋 To Do |
| US-7.2 | Scan QR Attendance | 8 | 📋 To Do |
| US-8.1 | Performance Analytics | 8 | 📋 To Do |
| - | System Integration | 8 | 📋 To Do |

**Total Points**: 32

### Key Dependencies
- QR code library integration
- Attendance data aggregation
- Chart library (Chart.js)

### Technical Tasks
- [ ] QR generation utility
- [ ] Camera-based QR scanner
- [ ] Attendance validation logic
- [ ] Analytics chart components
- [ ] End-to-end testing

---

## Velocity Tracking

| Sprint | Planned | Completed | Velocity |
|--------|---------|-----------|----------|
| Sprint 1 | 28 | - | - |
| Sprint 2 | 37 | - | - |
| Sprint 3 | 24 | - | - |
| Sprint 4 | 32 | - | - |

---

## Scrum Ceremonies Schedule

| Ceremony | When | Duration | Participants |
|----------|------|----------|--------------|
| Sprint Planning | Day 1, 10:00 AM | 2 hours | All team |
| Daily Stand-up | Daily, 9:30 AM | 15 min | All team |
| Sprint Review | Day 14, 2:00 PM | 1 hour | All + Stakeholders |
| Sprint Retrospective | Day 14, 3:30 PM | 1 hour | All team |

---

## Roles

| Role | Name | Responsibilities |
|------|------|-----------------|
| Product Owner | TBD | Backlog prioritization, acceptance |
| Scrum Master | TBD | Facilitate ceremonies, remove blockers |
| Development Team | TBD | Design, develop, test features |

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-31
