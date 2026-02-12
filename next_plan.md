# Next Plan: Remaining Experiments to Apply

## Overview

This document outlines the experiments that need to be **applied** to the CampusIntelli project. While documentation exists in `/experiment/` and `/theory/` folders, the actual implementation and integration of these concepts into the project is still pending.

---

## Experiment Mapping to Project Implementation

### Experiment 1: Requirement Elicitation Techniques and SRS

| Status | Task | Description |
|--------|------|-------------|
| [ ] | Update SRS | Enhance existing SRS with more detailed functional requirements |
| [ ] | Add NFRs | Add comprehensive Non-Functional Requirements (performance, security) |
| [ ] | Kano Model | Apply Kano model to prioritize features for CampusIntelli |
| [ ] | Traceability | Create requirement traceability matrix linking to code |

**Files to modify**: [`docs/SRS/software_requirements_specification.md`](docs/SRS/software_requirements_specification.md)

---

### Experiment 2: Actors and Use Cases

| Status | Task | Description |
|--------|------|-------------|
| [x] | Use Cases | Use case diagram already exists in [`docs/UML/use_case_diagram.md`](docs/UML/use_case_diagram.md) |
| [ ] | Extend Use Cases | Add remaining use cases (Library, Quiz, Feedback, Grievance) |
| [ ] | Actor Details | Add detailed actor descriptions and permissions matrix |

**Files to modify**: [`docs/UML/use_case_diagram.md`](docs/UML/use_case_diagram.md)

---

### Experiment 3: Use Case Specifications

| Status | Task | Description |
|--------|------|-------------|
| [ ] | Complete UC Specs | Write detailed specifications for all 17 use cases |
| [ ] | Alternative Flows | Add comprehensive alternative flows and error handling |
| [ ] | Pre/Post Conditions | Add complete preconditions and postconditions |

**Files to create**: `docs/UML/use_case_specifications.md`

---

### Experiment 4: User Stories with Acceptance Criteria

| Status | Task | Description |
|--------|------|-------------|
| [x] | User Stories | Already exists in [`docs/Agile/user_stories.md`](docs/Agile/user_stories.md) |
| [ ] | Add More Stories | Add stories for Library, Quiz, Feedback, Grievance |
| [ ] | Definition of Done | Add Definition of Done for each story |
| [ ] | Story Mapping | Create user story map showing epic to story hierarchy |

**Files to modify**: [`docs/Agile/user_stories.md`](docs/Agile/user_stories.md)

---

### Experiment 5: Wireframe Prototype

| Status | Task | Description |
|--------|------|-------------|
| [ ] | Create Wireframes | Create actual wireframes using Figma/Balsamiq |
| [ ] | Interactive Prototype | Build interactive prototype for user testing |
| [ ] | Mobile Wireframes | Design mobile-specific wireframes |
| [ ] | Accessibility | Ensure wireframes meet WCAG guidelines |

**Files to create**: `design/wireframes/`, `design/prototype.fig`

---

### Experiment 6: Activity Diagram

| Status | Task | Description |
|--------|------|-------------|
| [x] | Activity Diagrams | Already exists in [`docs/UML/activity_diagram.md`](docs/UML/activity_diagram.md) |
| [ ] | Add More Diagrams | Create diagrams for Library, Quiz, Feedback flows |
| [ ] | Swimlanes | Add detailed swimlanes for complex processes |
| [ ] | State Diagrams | Create state diagrams for key entities |

**Files to modify**: [`docs/UML/activity_diagram.md`](docs/UML/activity_diagram.md)

---

### Experiment 7: Class Diagram

| Status | Task | Description |
|--------|------|-------------|
| [x] | Class Diagram | Already exists in [`docs/UML/class_diagram.md`](docs/UML/class_diagram.md) |
| [ ] | Add Missing Classes | Add classes for Library, Quiz, Feedback, Grievance |
| [ ] | Database Schema | Create SQL schema from class diagram |
| [ ] | API Schema | Create API request/response schemas |

**Files to modify**: [`docs/UML/class_diagram.md`](docs/UML/class_diagram.md), [`database/models.py`](database/models.py)

---

### Experiment 8: Sequence Diagram

| Status | Task | Description |
|--------|------|-------------|
| [x] | Sequence Diagrams | Already exists in [`docs/UML/sequence_diagram.md`](docs/UML/sequence_diagram.md) |
| [ ] | Add More Diagrams | Create diagrams for Library, Quiz, Feedback flows |
| [ ] | API Sequence | Create sequence diagrams for API calls |
| [ ] | Error Handling | Add error handling sequences |

**Files to modify**: [`docs/UML/sequence_diagram.md`](docs/UML/sequence_diagram.md)

---

## Remaining Features to Implement

### Based on Experiments

| Feature | Experiment | Priority | Status |
|---------|------------|----------|--------|
| User Authentication | UC, Stories | High | Implemented |
| Dashboard | UC, Stories | High | Implemented |
| Course Management | UC, Stories | High | Implemented |
| Assignment System | UC, Stories | High | Implemented |
| Attendance (QR) | UC, Stories | High | Implemented |
| Room Booking | UC, Stories | Medium | Implemented |
| Announcements | UC, Stories | Medium | Implemented |
| Analytics | UC, Stories | Medium | Partial |
| **Library** | UC, Stories | Medium | [ ] |
| **Quiz System** | UC, Stories | Medium | [ ] |
| **Feedback** | UC, Stories | Low | [ ] |
| **Grievance** | UC, Stories | Low | [ ] |
| **TPO/Placement** | UC, Stories | Low | [ ] |

---

## Theory Application Checklist

### Unit I: Software Engineering

| Concept | Application | Status |
|---------|-------------|--------|
| Process Models | Use Agile/Scrum methodology | [x] |
| Documentation | Maintain SRS, UML docs | [x] |
| Quality Standards | Follow coding standards | [ ] |

### Unit II: Agile Development

| Concept | Application | Status |
|---------|-------------|--------|
| Scrum | Sprint planning, daily standups | [ ] |
| User Stories | Maintain product backlog | [x] |
| XP Practices | TDD, Pair programming | [ ] |

### Unit III: Requirements Engineering

| Concept | Application | Status |
|---------|-------------|--------|
| Elicitation | Stakeholder interviews | [ ] |
| SRS | Complete IEEE 830 SRS | [ ] |
| Prioritization | MoSCoW prioritization | [ ] |

### Unit IV: Software Modeling

| Concept | Application | Status |
|---------|-------------|--------|
| UML Diagrams | All 5 diagram types | [x] |
| Use Cases | Complete use case model | [ ] |
| Class Diagram | Complete class model | [ ] |

### Unit V: Project Management

| Concept | Application | Status |
|---------|-------------|--------|
| Gantt Chart | Project timeline | [ ] |
| Risk Management | Risk register, RMMM | [ ] |
| Cost Estimation | COCOMO/FP analysis | [ ] |

### Unit VI: Configuration & Quality Assurance

| Concept | Application | Status |
|---------|-------------|--------|
| Version Control | Git workflows | [x] |
| CI/CD Pipeline | Jenkins/GitHub Actions | [ ] |
| Testing Strategy | Unit, Integration, E2E | [ ] |
| Defect Management | Bug tracking process | [ ] |

---

## Implementation Roadmap

### Phase 1: Complete Core Features (Week 1-2)

- [ ] Complete Analytics module
- [ ] Add comprehensive API documentation
- [ ] Set up CI/CD pipeline

### Phase 2: Additional Features (Week 3-4)

- [ ] Implement Library module
- [ ] Implement Quiz system
- [ ] Add Feedback mechanism

### Phase 3: Advanced Features (Week 5-6)

- [ ] Implement Grievance system
- [ ] Add TPO/Placement module
- [ ] Complete mobile responsiveness

### Phase 4: Quality and Documentation (Week 7-8)

- [ ] Comprehensive testing
- [ ] Complete all UML diagrams
- [ ] Final documentation review

---

## Files to Create/Modify

### New Files Needed

| File | Description | Priority |
|------|-------------|----------|
| `docs/UML/state_diagram.md` | State diagrams for entities | Medium |
| `docs/UML/component_diagram.md` | Component architecture | Medium |
| `docs/Testing/test_plan.md` | Testing strategy | High |
| `docs/ProjectManagement/risk_register.md` | Risk management | Medium |
| `design/wireframes/wireframes.fig` | Figma wireframes | High |
| `.github/workflows/ci-cd.yml` | CI/CD pipeline | High |

### Files to Modify

| File | Modifications | Priority |
|------|---------------|----------|
| [`docs/SRS/software_requirements_specification.md`](docs/SRS/software_requirements_specification.md) | Add NFRs, more FRs | High |
| [`docs/UML/class_diagram.md`](docs/UML/class_diagram.md) | Add missing classes | High |
| [`database/models.py`](database/models.py) | Add Library, Quiz models | Medium |
| [`backend/app.py`](backend/app.py) | Add API routes for new features | Medium |

---

## Success Criteria

### Technical Deliverables

- [ ] All 8 UML diagrams complete
- [ ] Complete SRS (IEEE 830 compliant)
- [ ] Working CI/CD pipeline
- [ ] 80% code test coverage
- [ ] All features from backlog implemented

### Documentation Deliverables

- [ ] Updated SRS
- [ ] Complete user stories with acceptance criteria
- [ ] All use case specifications
- [ ] Test plan and reports
- [ ] Deployment guide

---

## Dependencies and Risks

| Risk | Impact | Mitigation |
|------|--------|-------------|
| Time constraints | High | Prioritize core features |
| Technology limitations | Medium | Use existing stack effectively |
| Resource availability | Medium | Focus on high-impact items |

---

## References

- **Experiments**: [`/experiment/`](experiment/)
- **Theory**: [`/theory/`](theory/)
- **Existing Documentation**: [`/docs/`](docs/)
- **Source Code**: [`/backend/`](backend/), [`/frontend/`](frontend/)

---

**Plan Created**: 2026-02-12  
**Next Review**: _____________  
**Approved By**: _____________
