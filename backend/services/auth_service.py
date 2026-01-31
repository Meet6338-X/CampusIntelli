"""
Authentication Service
"""

import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from typing import Optional, Tuple
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User, Student, Faculty, Admin
from services.storage_service import storage


class AuthService:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'campusintelli-dev-secret-key-2026')
    TOKEN_EXPIRY_HOURS = 24
    
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False
    
    @classmethod
    def generate_token(cls, user: dict) -> str:
        payload = {
            'user_id': user['id'],
            'email': user['email'],
            'role': user['role'],
            'exp': datetime.utcnow() + timedelta(hours=cls.TOKEN_EXPIRY_HOURS),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, cls.SECRET_KEY, algorithm='HS256')
    
    @classmethod
    def verify_token(cls, token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, cls.SECRET_KEY, algorithms=['HS256'])
        except:
            return None
    
    @classmethod
    def authenticate(cls, email: str, password: str) -> Tuple[bool, Optional[dict], str]:
        users = storage.get_by_field('users', 'email', email)
        if not users:
            return False, None, "User not found"
        
        user = users[0]
        if not cls.verify_password(password, user.get('password_hash', '')):
            return False, None, "Invalid password"
        
        storage.update('users', user['id'], {'last_login': datetime.now().isoformat()})
        token = cls.generate_token(user)
        user_data = {k: v for k, v in user.items() if k != 'password_hash'}
        user_data['token'] = token
        return True, user_data, "Login successful"
    
    @classmethod
    def register(cls, user_data: dict) -> Tuple[bool, Optional[dict], str]:
        email = user_data.get('email', '')
        if storage.get_by_field('users', 'email', email):
            return False, None, "Email already registered"
        
        password = user_data.pop('password', '')
        if len(password) < 6:
            return False, None, "Password must be at least 6 characters"
        
        user_data['password_hash'] = cls.hash_password(password)
        role = user_data.get('role', 'student')
        
        if role == 'student':
            user = Student(**{k: v for k, v in user_data.items() if k != 'password_hash'})
        elif role == 'faculty':
            user = Faculty(**{k: v for k, v in user_data.items() if k != 'password_hash'})
        elif role == 'admin':
            user = Admin(**{k: v for k, v in user_data.items() if k != 'password_hash'})
        else:
            user = User(**user_data)
        
        user.password_hash = user_data['password_hash']
        saved = storage.create('users', user.to_dict())
        result = {k: v for k, v in saved.items() if k != 'password_hash'}
        return True, result, "Registration successful"
    
    @classmethod
    def get_current_user(cls, token: str) -> Optional[dict]:
        payload = cls.verify_token(token)
        if not payload:
            return None
        user = storage.get_by_id('users', payload['user_id'])
        if not user:
            return None
        return {k: v for k, v in user.items() if k != 'password_hash'}


def init_sample_data():
    """Initialize comprehensive sample data with faculty, students, and courses."""
    users = storage.get_all('users')
    if not users:
        # Sample faculty across departments
        faculty_samples = [
            {
                'email': 'faculty@campus.edu', 
                'password': 'faculty123', 
                'name': 'Dr. Sarah Miller', 
                'role': 'faculty', 
                'department': 'Computer Science',
                'designation': 'Professor',
                'qualification': 'Ph.D. in Computer Science',
                'specialization': 'Machine Learning, AI',
                'experience_years': 12,
                'phone': '+91 9876543210',
                'office': 'CSE Block, Room 201',
                'office_hours': 'Mon-Fri 10:00-12:00'
            },
            {
                'email': 'rajesh.kumar@campus.edu', 
                'password': 'faculty123', 
                'name': 'Dr. Rajesh Kumar', 
                'role': 'faculty', 
                'department': 'Computer Science',
                'designation': 'Associate Professor',
                'qualification': 'Ph.D. in Software Engineering',
                'specialization': 'Software Architecture, DevOps',
                'experience_years': 8,
                'phone': '+91 9876543211',
                'office': 'CSE Block, Room 205',
                'office_hours': 'Tue-Thu 14:00-16:00'
            },
            {
                'email': 'priya.sharma@campus.edu', 
                'password': 'faculty123', 
                'name': 'Prof. Priya Sharma', 
                'role': 'faculty', 
                'department': 'Computer Science',
                'designation': 'Assistant Professor',
                'qualification': 'M.Tech in Data Science',
                'specialization': 'Data Analytics, Big Data',
                'experience_years': 5,
                'phone': '+91 9876543212',
                'office': 'CSE Block, Room 210',
                'office_hours': 'Mon-Wed 11:00-13:00'
            },
            {
                'email': 'amit.verma@campus.edu', 
                'password': 'faculty123', 
                'name': 'Dr. Amit Verma', 
                'role': 'faculty', 
                'department': 'Electronics',
                'designation': 'Professor',
                'qualification': 'Ph.D. in Electronics',
                'specialization': 'VLSI Design, Embedded Systems',
                'experience_years': 15,
                'phone': '+91 9876543213',
                'office': 'ECE Block, Room 101',
                'office_hours': 'Mon-Fri 09:00-11:00'
            },
            {
                'email': 'sunita.patel@campus.edu', 
                'password': 'faculty123', 
                'name': 'Dr. Sunita Patel', 
                'role': 'faculty', 
                'department': 'Electronics',
                'designation': 'Associate Professor',
                'qualification': 'Ph.D. in Communication Systems',
                'specialization': 'Wireless Networks, IoT',
                'experience_years': 10,
                'phone': '+91 9876543214',
                'office': 'ECE Block, Room 105',
                'office_hours': 'Tue-Thu 10:00-12:00'
            },
            {
                'email': 'mehul.joshi@campus.edu', 
                'password': 'faculty123', 
                'name': 'Prof. Mehul Joshi', 
                'role': 'faculty', 
                'department': 'Mechanical',
                'designation': 'Professor',
                'qualification': 'Ph.D. in Thermal Engineering',
                'specialization': 'Thermodynamics, Heat Transfer',
                'experience_years': 18,
                'phone': '+91 9876543215',
                'office': 'ME Block, Room 301',
                'office_hours': 'Mon-Wed 14:00-16:00'
            },
            {
                'email': 'anjali.singh@campus.edu', 
                'password': 'faculty123', 
                'name': 'Dr. Anjali Singh', 
                'role': 'faculty', 
                'department': 'Civil',
                'designation': 'Associate Professor',
                'qualification': 'Ph.D. in Structural Engineering',
                'specialization': 'Structural Design, Earthquake Engineering',
                'experience_years': 9,
                'phone': '+91 9876543216',
                'office': 'Civil Block, Room 102',
                'office_hours': 'Wed-Fri 09:00-11:00'
            },
            {
                'email': 'vikram.rao@campus.edu', 
                'password': 'faculty123', 
                'name': 'Prof. Vikram Rao', 
                'role': 'faculty', 
                'department': 'Mathematics',
                'designation': 'Professor',
                'qualification': 'Ph.D. in Applied Mathematics',
                'specialization': 'Numerical Methods, Statistics',
                'experience_years': 20,
                'phone': '+91 9876543217',
                'office': 'Science Block, Room 401',
                'office_hours': 'Mon-Fri 11:00-13:00'
            }
        ]
        
        # Register all faculty
        faculty_ids = {}
        for f in faculty_samples:
            success, user, msg = AuthService.register(f)
            if success:
                faculty_ids[f['email']] = user['id']
        
        # Sample students
        student_samples = [
            {'email': 'student@campus.edu', 'password': 'student123', 'name': 'Rahul Sharma', 'role': 'student', 'department': 'Computer Science'},
            {'email': 'student2@campus.edu', 'password': 'student123', 'name': 'Priya Patel', 'role': 'student', 'department': 'Computer Science'},
            {'email': 'student3@campus.edu', 'password': 'student123', 'name': 'Amit Kumar', 'role': 'student', 'department': 'Electronics'},
        ]
        for s in student_samples:
            AuthService.register(s)
        
        # Admin
        AuthService.register({
            'email': 'admin@campus.edu', 
            'password': 'admin123', 
            'name': 'System Admin', 
            'role': 'admin', 
            'department': 'IT'
        })
        
        # Sample courses
        from models.course import Course
        courses_data = [
            {'code': 'CS201', 'name': 'Data Structures', 'department': 'Computer Science', 'credits': 4, 
             'instructor_id': faculty_ids.get('faculty@campus.edu', ''),
             'description': 'Fundamental data structures including arrays, linked lists, trees, and graphs.'},
            {'code': 'CS301', 'name': 'Database Management Systems', 'department': 'Computer Science', 'credits': 4,
             'instructor_id': faculty_ids.get('rajesh.kumar@campus.edu', ''),
             'description': 'Introduction to database concepts, SQL, normalization, and transaction management.'},
            {'code': 'CS401', 'name': 'Machine Learning', 'department': 'Computer Science', 'credits': 4,
             'instructor_id': faculty_ids.get('faculty@campus.edu', ''),
             'description': 'Supervised and unsupervised learning, neural networks, and deep learning fundamentals.'},
            {'code': 'CS302', 'name': 'Web Development', 'department': 'Computer Science', 'credits': 3,
             'instructor_id': faculty_ids.get('priya.sharma@campus.edu', ''),
             'description': 'Full-stack web development with modern frameworks.'},
            {'code': 'EC201', 'name': 'Digital Electronics', 'department': 'Electronics', 'credits': 4,
             'instructor_id': faculty_ids.get('amit.verma@campus.edu', ''),
             'description': 'Digital logic, combinational and sequential circuits.'},
            {'code': 'EC301', 'name': 'Communication Systems', 'department': 'Electronics', 'credits': 4,
             'instructor_id': faculty_ids.get('sunita.patel@campus.edu', ''),
             'description': 'Analog and digital communication principles.'},
            {'code': 'ME201', 'name': 'Thermodynamics', 'department': 'Mechanical', 'credits': 4,
             'instructor_id': faculty_ids.get('mehul.joshi@campus.edu', ''),
             'description': 'Laws of thermodynamics and their applications.'},
            {'code': 'CE201', 'name': 'Structural Analysis', 'department': 'Civil', 'credits': 4,
             'instructor_id': faculty_ids.get('anjali.singh@campus.edu', ''),
             'description': 'Analysis of determinate and indeterminate structures.'},
            {'code': 'MA201', 'name': 'Engineering Mathematics', 'department': 'Mathematics', 'credits': 3,
             'instructor_id': faculty_ids.get('vikram.rao@campus.edu', ''),
             'description': 'Calculus, linear algebra, and differential equations.'},
        ]
        
        for c in courses_data:
            course = Course(**c)
            storage.create('courses', course.to_dict())
        
        print("[OK] Sample data created: 8 faculty, 3 students, 1 admin, 9 courses")
