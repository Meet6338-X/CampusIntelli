# Testing Strategy
## CampusIntelli Portal

---

## Testing Pyramid

```
            ┌────────────────┐
            │    E2E Tests   │  ← Few, slow, high confidence
            │   (10 tests)   │
            ├────────────────┤
            │  Integration   │  ← Medium, API testing
            │   (50 tests)   │
            ├────────────────┤
            │   Unit Tests   │  ← Many, fast, isolated
            │  (200 tests)   │
            └────────────────┘
```

---

## Test Types

### 1. Unit Tests

| Aspect | Details |
|--------|---------|
| **Scope** | Single function/method |
| **Tools** | pytest, unittest.mock |
| **Coverage Target** | >80% |
| **Run Frequency** | Every commit |

**Example:**
```python
# tests/test_auth_service.py
def test_password_hash():
    """Test password hashing creates valid hash."""
    from backend.services.auth_service import hash_password
    
    password = "TestPass123!"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) == 60  # bcrypt hash length

def test_password_verify():
    """Test password verification works correctly."""
    from backend.services.auth_service import hash_password, verify_password
    
    password = "TestPass123!"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) == True
    assert verify_password("WrongPass", hashed) == False
```

---

### 2. Integration Tests

| Aspect | Details |
|--------|---------|
| **Scope** | Multiple components together |
| **Tools** | pytest, requests |
| **Focus** | API endpoints, database |
| **Run Frequency** | Every PR |

**Example:**
```python
# tests/test_api_integration.py
def test_login_endpoint(client):
    """Test login API with valid credentials."""
    response = client.post('/api/auth/login', json={
        'email': 'student@test.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    assert 'token' in response.json
    assert response.json['role'] == 'student'

def test_booking_creates_record(client, auth_token):
    """Test booking creation updates database."""
    response = client.post('/api/bookings', 
        headers={'Authorization': f'Bearer {auth_token}'},
        json={
            'room_id': 'room-101',
            'date': '2026-02-01',
            'time_slot': '10:00-11:00'
        })
    
    assert response.status_code == 201
    # Verify in database
    from backend.services.storage_service import load_data
    bookings = load_data('bookings')
    assert any(b['id'] == response.json['id'] for b in bookings)
```

---

### 3. End-to-End (E2E) Tests

| Aspect | Details |
|--------|---------|
| **Scope** | Full user flow |
| **Tools** | Selenium, Playwright |
| **Focus** | Critical user journeys |
| **Run Frequency** | Before release |

**Critical User Journeys:**
1. Student login → View timetable → Submit assignment
2. Faculty login → Create assignment → Grade submission
3. User login → Book room → Cancel booking
4. Faculty login → Generate QR → Student marks attendance

---

### 4. Security Testing

| Test Type | Tool | Frequency |
|-----------|------|-----------|
| Dependency Scan | pip-audit | Every build |
| SQL Injection | sqlmap | Monthly |
| XSS Detection | OWASP ZAP | Monthly |
| Auth Testing | Manual | Per release |

**Security Checklist:**
- [ ] Password hashing verified
- [ ] Session tokens are secure
- [ ] Role-based access enforced
- [ ] File upload validation
- [ ] Input sanitization

---

### 5. Performance Testing

| Metric | Target | Tool |
|--------|--------|------|
| Page Load | <2s | Lighthouse |
| API Response | <500ms | locust |
| Concurrent Users | 50+ | locust |
| Database Query | <100ms | Profiler |

**Load Test Scenario:**
```python
# locustfile.py
from locust import HttpUser, task, between

class CampusUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(5)
    def view_dashboard(self):
        self.client.get("/dashboard")
    
    @task(3)
    def view_timetable(self):
        self.client.get("/api/timetable")
    
    @task(1)
    def submit_assignment(self):
        self.client.post("/api/assignments/1/submit", 
            files={"file": ("test.pdf", b"content")})
```

---

## Test Data Management

| Environment | Data Source | Reset Frequency |
|-------------|-------------|-----------------|
| Unit Tests | Mock/Fixtures | Per test |
| Integration | Test JSON files | Per test suite |
| E2E | Seeded database | Per test run |
| Staging | Anonymized prod copy | Weekly |

**Fixture Example:**
```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_user():
    return {
        "id": "user-123",
        "email": "test@test.com",
        "name": "Test User",
        "role": "student"
    }

@pytest.fixture
def sample_assignment():
    return {
        "id": "assign-001",
        "title": "Test Assignment",
        "course_id": "CS101",
        "due_date": "2026-02-15T23:59:00"
    }
```

---

## Test Coverage Requirements

| Module | Minimum Coverage |
|--------|------------------|
| Auth Service | 90% |
| Storage Service | 85% |
| API Routes | 80% |
| Models | 85% |
| Utilities | 75% |

---

## Defect Classification

| Severity | Description | Response Time |
|----------|-------------|---------------|
| Critical | System down, data loss | Immediate |
| High | Major feature broken | Same day |
| Medium | Feature degraded | Within sprint |
| Low | Minor issue, workaround exists | Backlog |

---

## Test Environment Setup

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock requests

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_auth_service.py -v

# Run marked tests only
pytest tests/ -m "unit" -v
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-31
