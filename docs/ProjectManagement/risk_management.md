# Risk Management (RMMM Plan)
## CampusIntelli Portal

---

## Risk Management Overview

The RMMM (Risk Mitigation, Monitoring, and Management) Plan identifies potential risks and defines strategies to handle them.

---

## Risk Register

### Technical Risks

| ID | Risk | Probability | Impact | Score | Category |
|----|------|-------------|--------|-------|----------|
| R1 | QR code system vulnerable to proxy attendance | High | Medium | 🟠 6 | Security |
| R2 | Local storage data corruption | Medium | High | 🟠 6 | Data |
| R3 | File upload security vulnerabilities | Medium | High | 🟠 6 | Security |
| R4 | Browser compatibility issues | Low | Medium | 🟢 3 | Technical |
| R5 | Session management flaws | Medium | High | 🟠 6 | Security |

### Project Risks

| ID | Risk | Probability | Impact | Score | Category |
|----|------|-------------|--------|-------|----------|
| R6 | Scope creep during development | High | Medium | 🟠 6 | Schedule |
| R7 | Integration failures between modules | Medium | High | 🟠 6 | Technical |
| R8 | Insufficient testing time | Medium | Medium | 🟡 4 | Quality |
| R9 | Key developer unavailability | Low | High | 🟡 4 | Resource |
| R10 | Database migration issues (future Supabase) | Medium | Medium | 🟡 4 | Technical |

---

## Risk Score Matrix

```
        │ Low Impact(1) │ Med Impact(2) │ High Impact(3)
────────┼───────────────┼───────────────┼───────────────
High(3) │     🟡 3      │     🟠 6      │     🔴 9
        │               │     R1, R6    │
────────┼───────────────┼───────────────┼───────────────
Med(2)  │     🟢 2      │     🟡 4      │     🟠 6
        │               │   R8,R9,R10   │   R2,R3,R5,R7
────────┼───────────────┼───────────────┼───────────────
Low(1)  │     🟢 1      │     🟢 2      │     🟡 3
        │               │               │      R4
────────┴───────────────┴───────────────┴───────────────
```

---

## Detailed Risk Analysis & RMMM

### R1: QR Code Proxy Attendance

| Aspect | Details |
|--------|---------|
| **Description** | Students may share QR codes with absent peers |
| **Probability** | High |
| **Impact** | Medium (data integrity, trust) |

**Mitigation Strategies:**
- [ ] Time-bound QR codes (5-minute expiry)
- [ ] Unique code per generation (no reuse)
- [ ] IP/device fingerprinting (future)
- [ ] Location verification via GPS (future)

**Monitoring:**
- Track attendance patterns (unusual spikes)
- Compare scan times with QR generation
- Flag multiple scans from same device

**Management:**
- Review flagged cases weekly
- Faculty can manually adjust attendance
- Warning system for suspicious patterns

---

### R2: Local Storage Data Corruption

| Aspect | Details |
|--------|---------|
| **Description** | JSON files may become corrupted or inconsistent |
| **Probability** | Medium |
| **Impact** | High (data loss, system failure) |

**Mitigation Strategies:**
- [ ] Atomic file writes (write to temp, then rename)
- [ ] JSON schema validation on read/write
- [ ] Automated backup on each write
- [ ] Version control for data files (git)

**Monitoring:**
- Validate JSON structure on application start
- Log all data write operations
- Check file integrity periodically

**Management:**
- Automatic rollback to last valid backup
- Manual recovery script available
- Data export feature for users

---

### R3: File Upload Security Vulnerabilities

| Aspect | Details |
|--------|---------|
| **Description** | Malicious file uploads (executable, XSS) |
| **Probability** | Medium |
| **Impact** | High (system compromise) |

**Mitigation Strategies:**
- [ ] Whitelist file extensions (PDF, DOC, DOCX, ZIP only)
- [ ] Validate MIME types
- [ ] File size limits (10MB max)
- [ ] Rename uploaded files (strip original name)
- [ ] Store uploads outside web root

**Monitoring:**
- Log all upload attempts
- Alert on rejected file types
- Scan uploads with antivirus (optional)

**Management:**
- Quarantine suspicious files
- Block repeat offenders
- Regular security audits

---

### R5: Session Management Flaws

| Aspect | Details |
|--------|---------|
| **Description** | Session hijacking, fixation, or improper expiry |
| **Probability** | Medium |
| **Impact** | High (unauthorized access) |

**Mitigation Strategies:**
- [ ] Secure, HttpOnly, SameSite cookies
- [ ] Regenerate session ID after login
- [ ] Session expiry (24 hours)
- [ ] Single session per user (optional)
- [ ] Logout invalidates all sessions

**Monitoring:**
- Track concurrent sessions per user
- Log session creation/destruction
- Alert on unusual login locations

**Management:**
- Force logout on security alerts
- User can view/terminate sessions
- Admin can terminate any session

---

### R6: Scope Creep

| Aspect | Details |
|--------|---------|
| **Description** | New features added beyond original scope |
| **Probability** | High |
| **Impact** | Medium (delays, budget) |

**Mitigation Strategies:**
- [ ] Clearly defined MVP in SRS
- [ ] Strict backlog prioritization
- [ ] Change request process
- [ ] Sprint goal protection

**Monitoring:**
- Track backlog changes per sprint
- Compare planned vs. delivered
- Burndown chart analysis

**Management:**
- Product Owner approves all changes
- Document and defer non-critical requests
- Re-negotiate deadlines if needed

---

### R7: Integration Failures

| Aspect | Details |
|--------|---------|
| **Description** | Modules fail to work together |
| **Probability** | Medium |
| **Impact** | High (system unusable) |

**Mitigation Strategies:**
- [ ] Modular architecture with clear interfaces
- [ ] Integration tests from Sprint 1
- [ ] API contracts documented
- [ ] Regular integration testing

**Monitoring:**
- Run integration tests on each merge
- Track API response consistency
- Monitor end-to-end test results

**Management:**
- Prioritize integration fixes
- Dedicated integration sprint buffer
- Technical debt tracking

---

## Risk Response Plan

| Risk Score | Response Strategy |
|------------|------------------|
| 🔴 7-9 | Immediate action required, escalate to stakeholders |
| 🟠 4-6 | Actively manage, weekly review, mitigation in progress |
| 🟡 2-3 | Monitor closely, have contingency ready |
| 🟢 1 | Accept risk, periodic review |

---

## Risk Tracking Template

| Date | Risk ID | Status | Action Taken | Next Review |
|------|---------|--------|--------------|-------------|
| Week 1 | R1 | Open | Implemented 5-min expiry | Week 2 |
| Week 1 | R2 | Open | Added backup on write | Week 3 |
| Week 2 | R3 | Open | Added file validation | Week 3 |

---

## Contingency Budget

| Category | Buffer | Usage |
|----------|--------|-------|
| Time | +20% per sprint | Unexpected technical issues |
| Scope | 2 stories deferrable | Can be moved to future release |

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-31
