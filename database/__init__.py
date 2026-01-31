# CampusIntelli Database Initialization
# SQLAlchemy database setup with connection (COMMENTED OUT for now)
# Currently using local JSON storage - uncomment when ready to use database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .config import DatabaseConfig
from .models import Base

# Database engine - COMMENTED OUT (using local JSON storage for now)
# Uncomment these lines when ready to connect to database:
#
# engine = create_engine(
#     DatabaseConfig.get_connection_string(),
#     **DatabaseConfig.ENGINE_OPTIONS
# )
#
# # Create session factory
# SessionFactory = sessionmaker(bind=engine)
# Session = scoped_session(SessionFactory)
#
# def init_db():
#     """Initialize database - create all tables"""
#     Base.metadata.create_all(engine)
#     print("[DB] Database tables created successfully")
#
# def get_session():
#     """Get a database session"""
#     return Session()
#
# def close_session(session):
#     """Close a database session"""
#     session.close()

# Placeholder functions for when database is not connected
engine = None
Session = None

def init_db():
    """Placeholder - database not connected"""
    print("[DB] Database not connected - using local JSON storage")
    print("[DB] To connect, uncomment the engine and session code in database/__init__.py")

def get_session():
    """Placeholder - database not connected"""
    return None

def close_session(session):
    """Placeholder - database not connected"""
    pass

# Export models for easy access
from .models import (
    # Core
    User, UserRole,
    # Academics
    Course, Assignment, Submission, AssignmentStatus,
    # Attendance
    AttendanceSession, AttendanceRecord, AttendanceStatus,
    # Examinations
    Examination, ExamResult, ExamType,
    # Events
    Event,
    # Fees
    FeeStructure, FeePayment, FeeStatus,
    # Rooms & Bookings
    Room, Booking, BookingStatus,
    # Announcements
    Announcement,
    # Library
    Book, BookIssue,
    # Quiz
    Quiz, QuizQuestion, QuizAttempt,
    # Feedback & Grievance
    Feedback, Grievance, GrievanceStatus,
    # Hostel
    Hostel, HostelRoom, HostelAllotment,
    # TPO
    Company, PlacementDrive, PlacementApplication,
    # Certificate
    Certificate,
    # Timetable
    Timetable,
)

__all__ = [
    'init_db', 'get_session', 'close_session', 'engine', 'Session', 'Base',
    'User', 'UserRole', 'Course', 'Assignment', 'Submission',
    'AttendanceSession', 'AttendanceRecord', 'AttendanceStatus',
    'Examination', 'ExamResult', 'ExamType', 'Event',
    'FeeStructure', 'FeePayment', 'FeeStatus',
    'Room', 'Booking', 'BookingStatus', 'Announcement',
    'Book', 'BookIssue', 'Quiz', 'QuizQuestion', 'QuizAttempt',
    'Feedback', 'Grievance', 'GrievanceStatus',
    'Hostel', 'HostelRoom', 'HostelAllotment',
    'Company', 'PlacementDrive', 'PlacementApplication',
    'Certificate', 'Timetable'
]
