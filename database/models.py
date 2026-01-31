# CampusIntelli Database Models
# SQLAlchemy ORM models for all portal entities
# These models are ready for database connection when needed

from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime, Date, Time,
    ForeignKey, Enum, Table, JSON
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()


# ============================================
# ENUMS
# ============================================

class UserRole(enum.Enum):
    STUDENT = "student"
    FACULTY = "faculty"
    ADMIN = "admin"
    HOD = "hod"
    PRINCIPAL = "principal"

class AttendanceStatus(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"

class AssignmentStatus(enum.Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    GRADED = "graded"
    LATE = "late"

class BookingStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class FeeStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    PARTIAL = "partial"
    OVERDUE = "overdue"

class GrievanceStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class ExamType(enum.Enum):
    INTERNAL = "internal"
    MIDTERM = "midterm"
    FINAL = "final"
    PRACTICAL = "practical"
    VIVA = "viva"


# ============================================
# ASSOCIATION TABLES
# ============================================

course_students = Table(
    'course_students', Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('student_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('enrolled_at', DateTime, default=func.now())
)


# ============================================
# USER & AUTHENTICATION
# ============================================

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    department = Column(String(100))
    phone = Column(String(20))
    avatar_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Student-specific fields
    roll_number = Column(String(50))
    semester = Column(Integer)
    batch_year = Column(Integer)
    guardian_name = Column(String(255))
    guardian_phone = Column(String(20))
    address = Column(Text)
    
    # Faculty-specific fields
    employee_id = Column(String(50))
    designation = Column(String(100))
    qualification = Column(String(255))
    
    # Relationships
    courses_enrolled = relationship('Course', secondary=course_students, back_populates='students')
    courses_taught = relationship('Course', back_populates='instructor')
    submissions = relationship('Submission', back_populates='student')
    attendance_records = relationship('AttendanceRecord', back_populates='student')
    bookings = relationship('Booking', back_populates='user')
    feedbacks = relationship('Feedback', back_populates='user')
    grievances = relationship('Grievance', back_populates='user')


# ============================================
# COURSES & ACADEMICS
# ============================================

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    credits = Column(Integer, default=3)
    department = Column(String(100))
    semester = Column(Integer)
    instructor_id = Column(Integer, ForeignKey('users.id'))
    max_students = Column(Integer, default=60)
    schedule = Column(JSON)  # {"mon": "09:00-10:00", "wed": "09:00-10:00"}
    syllabus_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    instructor = relationship('User', back_populates='courses_taught')
    students = relationship('User', secondary=course_students, back_populates='courses_enrolled')
    assignments = relationship('Assignment', back_populates='course')
    attendance_sessions = relationship('AttendanceSession', back_populates='course')
    examinations = relationship('Examination', back_populates='course')


class Assignment(Base):
    __tablename__ = 'assignments'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime, nullable=False)
    max_marks = Column(Float, default=100)
    attachment_url = Column(String(500))
    status = Column(Enum(AssignmentStatus), default=AssignmentStatus.PENDING)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    course = relationship('Course', back_populates='assignments')
    submissions = relationship('Submission', back_populates='assignment')


class Submission(Base):
    __tablename__ = 'submissions'
    
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text)
    file_url = Column(String(500))
    marks = Column(Float)
    feedback = Column(Text)
    submitted_at = Column(DateTime, default=func.now())
    graded_at = Column(DateTime)
    
    # Relationships
    assignment = relationship('Assignment', back_populates='submissions')
    student = relationship('User', back_populates='submissions')


# ============================================
# ATTENDANCE
# ============================================

class AttendanceSession(Base):
    __tablename__ = 'attendance_sessions'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    session_date = Column(Date, nullable=False)
    start_time = Column(Time)
    end_time = Column(Time)
    qr_code = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    course = relationship('Course', back_populates='attendance_sessions')
    records = relationship('AttendanceRecord', back_populates='session')


class AttendanceRecord(Base):
    __tablename__ = 'attendance_records'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('attendance_sessions.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.ABSENT)
    marked_at = Column(DateTime, default=func.now())
    remarks = Column(String(255))
    
    # Relationships
    session = relationship('AttendanceSession', back_populates='records')
    student = relationship('User', back_populates='attendance_records')


# ============================================
# EXAMINATIONS
# ============================================

class Examination(Base):
    __tablename__ = 'examinations'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(255), nullable=False)
    exam_type = Column(Enum(ExamType), default=ExamType.INTERNAL)
    exam_date = Column(Date, nullable=False)
    start_time = Column(Time)
    end_time = Column(Time)
    venue = Column(String(255))
    max_marks = Column(Float, default=100)
    passing_marks = Column(Float, default=40)
    instructions = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    course = relationship('Course', back_populates='examinations')
    results = relationship('ExamResult', back_populates='examination')


class ExamResult(Base):
    __tablename__ = 'exam_results'
    
    id = Column(Integer, primary_key=True)
    examination_id = Column(Integer, ForeignKey('examinations.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    marks_obtained = Column(Float)
    grade = Column(String(5))
    remarks = Column(Text)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime)
    
    # Relationships
    examination = relationship('Examination', back_populates='results')


# ============================================
# EVENTS
# ============================================

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    event_type = Column(String(50))  # cultural, technical, workshop, seminar
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    venue = Column(String(255))
    organizer = Column(String(255))
    max_participants = Column(Integer)
    registration_deadline = Column(DateTime)
    is_featured = Column(Boolean, default=False)
    image_url = Column(String(500))
    created_at = Column(DateTime, default=func.now())


# ============================================
# FEES & ACCOUNTS
# ============================================

class FeeStructure(Base):
    __tablename__ = 'fee_structures'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    fee_type = Column(String(50))  # tuition, hostel, library, exam, lab
    semester = Column(Integer)
    department = Column(String(100))
    due_date = Column(Date)
    academic_year = Column(String(20))
    is_active = Column(Boolean, default=True)


class FeePayment(Base):
    __tablename__ = 'fee_payments'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey('fee_structures.id'), nullable=False)
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=func.now())
    payment_method = Column(String(50))  # card, upi, netbanking, cash
    transaction_id = Column(String(100))
    status = Column(Enum(FeeStatus), default=FeeStatus.PENDING)
    receipt_url = Column(String(500))


# ============================================
# ROOM BOOKINGS
# ============================================

class Room(Base):
    __tablename__ = 'rooms'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    building = Column(String(100))
    floor = Column(Integer)
    capacity = Column(Integer)
    room_type = Column(String(50))  # classroom, lab, conference, auditorium
    facilities = Column(JSON)  # ["projector", "ac", "whiteboard"]
    is_available = Column(Boolean, default=True)


class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    purpose = Column(String(255), nullable=False)
    booking_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    approved_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    room = relationship('Room')
    user = relationship('User', foreign_keys=[user_id], back_populates='bookings')


# ============================================
# ANNOUNCEMENTS
# ============================================

class Announcement(Base):
    __tablename__ = 'announcements'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    target_audience = Column(String(50))  # all, students, faculty, department
    department = Column(String(100))
    is_pinned = Column(Boolean, default=False)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())


# ============================================
# LIBRARY
# ============================================

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    isbn = Column(String(20), unique=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    publisher = Column(String(255))
    category = Column(String(100))
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    shelf_location = Column(String(50))
    cover_url = Column(String(500))


class BookIssue(Base):
    __tablename__ = 'book_issues'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    issue_date = Column(Date, default=date.today)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    fine_amount = Column(Float, default=0)
    status = Column(String(20), default='issued')  # issued, returned, overdue


# ============================================
# QUIZ & ONLINE TESTS
# ============================================

class Quiz(Base):
    __tablename__ = 'quizzes'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer, default=30)
    total_marks = Column(Float, default=10)
    passing_marks = Column(Float, default=4)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_published = Column(Boolean, default=False)
    shuffle_questions = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())


class QuizQuestion(Base):
    __tablename__ = 'quiz_questions'
    
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(20))  # mcq, true_false, short_answer
    options = Column(JSON)  # ["option1", "option2", "option3", "option4"]
    correct_answer = Column(Text)
    marks = Column(Float, default=1)
    explanation = Column(Text)


class QuizAttempt(Base):
    __tablename__ = 'quiz_attempts'
    
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    answers = Column(JSON)
    marks_obtained = Column(Float)
    started_at = Column(DateTime, default=func.now())
    submitted_at = Column(DateTime)
    is_completed = Column(Boolean, default=False)


# ============================================
# FEEDBACK & GRIEVANCE
# ============================================

class Feedback(Base):
    __tablename__ = 'feedbacks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String(50))  # course, faculty, facilities, general
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    rating = Column(Integer)  # 1-5 stars
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship('User', back_populates='feedbacks')


class Grievance(Base):
    __tablename__ = 'grievances'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ticket_number = Column(String(20), unique=True)
    category = Column(String(50))  # academic, hostel, fees, harassment, other
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(GrievanceStatus), default=GrievanceStatus.OPEN)
    priority = Column(String(20), default='medium')  # low, medium, high, urgent
    assigned_to = Column(Integer, ForeignKey('users.id'))
    resolution = Column(Text)
    created_at = Column(DateTime, default=func.now())
    resolved_at = Column(DateTime)
    
    # Relationships
    user = relationship('User', foreign_keys=[user_id], back_populates='grievances')


# ============================================
# HOSTEL
# ============================================

class Hostel(Base):
    __tablename__ = 'hostels'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20))  # boys, girls
    warden_id = Column(Integer, ForeignKey('users.id'))
    total_rooms = Column(Integer)
    contact = Column(String(20))


class HostelRoom(Base):
    __tablename__ = 'hostel_rooms'
    
    id = Column(Integer, primary_key=True)
    hostel_id = Column(Integer, ForeignKey('hostels.id'), nullable=False)
    room_number = Column(String(20), nullable=False)
    floor = Column(Integer)
    capacity = Column(Integer, default=2)
    current_occupancy = Column(Integer, default=0)
    room_type = Column(String(20))  # single, double, triple
    is_available = Column(Boolean, default=True)


class HostelAllotment(Base):
    __tablename__ = 'hostel_allotments'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('hostel_rooms.id'), nullable=False)
    allotment_date = Column(Date, nullable=False)
    valid_till = Column(Date)
    is_active = Column(Boolean, default=True)


# ============================================
# TPO (TRAINING & PLACEMENT)
# ============================================

class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    industry = Column(String(100))
    website = Column(String(500))
    logo_url = Column(String(500))
    description = Column(Text)


class PlacementDrive(Base):
    __tablename__ = 'placement_drives'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    job_role = Column(String(255))
    package_lpa = Column(Float)
    eligibility_criteria = Column(Text)
    drive_date = Column(Date)
    registration_deadline = Column(Date)
    venue = Column(String(255))
    is_active = Column(Boolean, default=True)


class PlacementApplication(Base):
    __tablename__ = 'placement_applications'
    
    id = Column(Integer, primary_key=True)
    drive_id = Column(Integer, ForeignKey('placement_drives.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    resume_url = Column(String(500))
    status = Column(String(50), default='applied')  # applied, shortlisted, selected, rejected
    applied_at = Column(DateTime, default=func.now())


# ============================================
# CERTIFICATE
# ============================================

class Certificate(Base):
    __tablename__ = 'certificates'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    certificate_type = Column(String(50))  # bonafide, character, transfer, course_completion
    request_date = Column(DateTime, default=func.now())
    issue_date = Column(DateTime)
    status = Column(String(20), default='pending')  # pending, approved, issued, rejected
    certificate_number = Column(String(50))
    download_url = Column(String(500))


# ============================================
# TIMETABLE
# ============================================

class Timetable(Base):
    __tablename__ = 'timetables'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    day_of_week = Column(Integer)  # 0=Monday, 6=Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    faculty_id = Column(Integer, ForeignKey('users.id'))
    is_active = Column(Boolean, default=True)
