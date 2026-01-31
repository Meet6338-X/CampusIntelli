# Gantt Chart
## CampusIntelli Portal - Project Timeline

---

## Project Timeline Overview

**Project Duration**: 8 weeks (4 sprints × 2 weeks)  
**Start Date**: Week 1  
**End Date**: Week 8

---

## Gantt Chart Visualization

```
                    Week 1  Week 2  Week 3  Week 4  Week 5  Week 6  Week 7  Week 8
                    ────────────────────────────────────────────────────────────
SPRINT 1: AUTH     ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 └─ Login System   ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 └─ Dashboard      ░░░░░░░░░░████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 └─ User Mgmt      ░░░░░░████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                    ────────────────────────────────────────────────────────────
SPRINT 2: ACADEMIC ░░░░░░░░░░░░░░░░████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 └─ Timetable      ░░░░░░░░░░░░░░░░████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 └─ Assignments    ░░░░░░░░░░░░░░░░░░░░████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 └─ Gradebook      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░████░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                    ────────────────────────────────────────────────────────────
SPRINT 3: SERVICES ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████████████░░░░░░░░░░░░
 └─ Room Booking   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████████░░░░░░░░░░░░░░░░
 └─ Announcements  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████░░░░░░░░░░░░
                    ────────────────────────────────────────────────────────────
SPRINT 4: ANALYTICS░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████████
 └─ QR Attendance  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████░░░░
 └─ Analytics      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████
 └─ Integration    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████
                    ────────────────────────────────────────────────────────────
DOCUMENTATION      ████████████████████████████████████████████████████████████
                    ────────────────────────────────────────────────────────────
TESTING            ░░░░░░░░░░░░████░░░░░░░░░░░░████░░░░░░░░░░░░████░░░░░░░░████
                    ────────────────────────────────────────────────────────────

Legend:  ████ = Active Work   ░░░░ = Inactive
```

---

## Detailed Timeline

### Sprint 1: Authentication & Dashboard (Week 1-2)

| Task | Start | End | Duration | Dependencies |
|------|-------|-----|----------|--------------|
| Project Setup | Day 1 | Day 1 | 1 day | - |
| User Model | Day 1 | Day 2 | 2 days | - |
| Auth Service | Day 2 | Day 4 | 3 days | User Model |
| Login Page UI | Day 3 | Day 5 | 3 days | - |
| Login API | Day 4 | Day 6 | 3 days | Auth Service |
| Dashboard UI | Day 6 | Day 9 | 4 days | Login API |
| User Management | Day 7 | Day 10 | 4 days | User Model |
| Sprint 1 Testing | Day 9 | Day 10 | 2 days | All above |

### Sprint 2: Academic Core (Week 3-4)

| Task | Start | End | Duration | Dependencies |
|------|-------|-----|----------|--------------|
| Course Model | Day 11 | Day 12 | 2 days | Sprint 1 |
| Timetable Service | Day 12 | Day 14 | 3 days | Course Model |
| Timetable UI | Day 13 | Day 16 | 4 days | Timetable Service |
| Assignment Model | Day 14 | Day 15 | 2 days | Course Model |
| Submission Service | Day 15 | Day 18 | 4 days | Assignment Model |
| Assignment UI | Day 16 | Day 19 | 4 days | Submission Service |
| Grade Service | Day 18 | Day 20 | 3 days | Submission Service |
| Sprint 2 Testing | Day 19 | Day 20 | 2 days | All above |

### Sprint 3: Campus Services (Week 5-6)

| Task | Start | End | Duration | Dependencies |
|------|-------|-----|----------|--------------|
| Room Model | Day 21 | Day 22 | 2 days | Sprint 2 |
| Booking Service | Day 22 | Day 25 | 4 days | Room Model |
| Booking UI | Day 24 | Day 28 | 5 days | Booking Service |
| Announcement Model | Day 26 | Day 27 | 2 days | - |
| Announcement Feed | Day 27 | Day 30 | 4 days | Announcement Model |
| Sprint 3 Testing | Day 29 | Day 30 | 2 days | All above |

### Sprint 4: Analytics & QR (Week 7-8)

| Task | Start | End | Duration | Dependencies |
|------|-------|-----|----------|--------------|
| QR Code Service | Day 31 | Day 34 | 4 days | Sprint 3 |
| Attendance Model | Day 32 | Day 33 | 2 days | QR Code Service |
| QR Generate UI | Day 34 | Day 36 | 3 days | QR Code Service |
| QR Scanner UI | Day 35 | Day 38 | 4 days | Attendance Model |
| Analytics Service | Day 36 | Day 39 | 4 days | All data models |
| Analytics Dashboard | Day 38 | Day 40 | 3 days | Analytics Service |
| Integration Testing | Day 39 | Day 40 | 2 days | All above |

---

## Critical Path

The critical path determines the minimum project duration:

```
Project Setup → User Model → Auth Service → Login API → Dashboard UI
    ↓
Course Model → Assignment Model → Submission Service
    ↓
Room Model → QR Code Service → Analytics Service → Final Integration
```

**Critical Path Duration**: 40 days (8 weeks)

---

## Milestones

| Milestone | Date | Deliverable |
|-----------|------|-------------|
| M1: Auth Complete | Week 2 | Login, Dashboard, User Management |
| M2: Academic Ready | Week 4 | Timetable, Assignments, Grading |
| M3: Services Live | Week 6 | Room Booking, Announcements |
| M4: Full Release | Week 8 | QR Attendance, Analytics, Integration |

---

## Resource Allocation

| Role | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 |
|------|----------|----------|----------|----------|
| Backend Dev | 80% | 70% | 60% | 50% |
| Frontend Dev | 60% | 80% | 80% | 70% |
| QA/Testing | 20% | 30% | 30% | 50% |
| Documentation | 40% | 20% | 20% | 30% |

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-31
