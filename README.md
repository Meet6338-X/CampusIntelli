# CampusIntelli Portal

🎓 A unified digital hub for students and faculty.

## Features

- **User Authentication** - Secure login with role-based access
- **Dashboard** - Overview of courses, assignments, and announcements
- **Course Management** - View enrolled courses and timetables
- **Assignment System** - Submit and track assignments with grading
- **QR & Code Attendance** - Generate QR codes and secure session codes for attendance marking
- **Room Booking** - Reserve campus spaces and equipment
- **Announcements** - Stay updated with campus news
- **AI Chatbot Integration** - Intelligent campus assistance powered by Google Gemini API
- **Academic Module** - Manage student marks, grades, and CGPA with MySQL backend support
- **Library Module** - Comprehensive book borrowing, returning, and directory workflows

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
cd backend
python app.py
```

### Access
Open http://localhost:5000 in your browser.

### Demo Accounts
| Role | Email | Password |
|------|-------|----------|
| Student | student@campus.edu | student123 |
| Faculty | faculty@campus.edu | faculty123 |
| Admin | admin@campus.edu | admin123 |

## Project Structure

```
CampusIntelli/
├── backend/
│   ├── app.py              # Flask application
│   ├── models/             # Data models
│   ├── routes/             # API endpoints
│   └── services/           # Business logic
├── frontend/
│   ├── index.html          # Main HTML
│   ├── css/style.css       # Styles
│   └── js/                 # JavaScript
├── data/                   # JSON storage
├── docs/                   # Documentation
│   ├── SRS/               # Requirements
│   ├── UML/               # Diagrams
│   ├── Agile/             # Sprint docs
│   ├── ProjectManagement/ # PM docs
│   └── DevOps/            # CI/CD docs
└── requirements.txt
```

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Storage**: JSON files (local)
- **Auth**: JWT, bcrypt

## Documentation

Comprehensive documentation available in `/docs`:
- Software Requirements Specification (SRS)
- UML Diagrams (Use Case, Class, Sequence, Activity, Deployment)
- Agile Artifacts (Backlog, Sprint Planning, User Stories)
- Project Management (Gantt Chart, Risk Management, Cost Estimation)
- DevOps (CI/CD Pipeline, Testing Strategy, QA Plan)

## License

MIT License - CampusIntelli 2026
