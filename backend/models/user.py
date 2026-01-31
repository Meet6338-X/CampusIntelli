"""
User Models
"""

from datetime import datetime
from typing import List
import uuid


class User:
    """Base User class."""
    
    def __init__(self, id=None, email="", password_hash="", name="", 
                 role="student", department="", created_at=None, last_login=None):
        self.id = id or str(uuid.uuid4())
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.role = role
        self.department = department
        self.created_at = created_at or datetime.now().isoformat()
        self.last_login = last_login
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password_hash': self.password_hash,
            'name': self.name,
            'role': self.role,
            'department': self.department,
            'created_at': self.created_at,
            'last_login': self.last_login
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class Student(User):
    """Student user."""
    
    def __init__(self, student_id="", semester=1, enrolled_courses=None, **kwargs):
        # Remove role if passed, we set it ourselves
        kwargs.pop('role', None)
        super().__init__(role='student', **kwargs)
        self.student_id = student_id or f"STU{self.id[:8].upper()}"
        self.semester = semester
        self.enrolled_courses = enrolled_courses or []
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
            'semester': self.semester,
            'enrolled_courses': self.enrolled_courses
        })
        return data


class Faculty(User):
    """Faculty user."""
    
    def __init__(self, faculty_id="", designation="", assigned_courses=None, **kwargs):
        kwargs.pop('role', None)
        super().__init__(role='faculty', **kwargs)
        self.faculty_id = faculty_id or f"FAC{self.id[:8].upper()}"
        self.designation = designation
        self.assigned_courses = assigned_courses or []
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'faculty_id': self.faculty_id,
            'designation': self.designation,
            'assigned_courses': self.assigned_courses
        })
        return data


class Admin(User):
    """Admin user."""
    
    def __init__(self, admin_id="", permissions=None, **kwargs):
        kwargs.pop('role', None)
        super().__init__(role='admin', **kwargs)
        self.admin_id = admin_id or f"ADM{self.id[:8].upper()}"
        self.permissions = permissions or ['all']
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'admin_id': self.admin_id,
            'permissions': self.permissions
        })
        return data


def create_user_from_dict(data):
    role = data.get('role', 'student')
    if role == 'student':
        return Student(**data)
    elif role == 'faculty':
        return Faculty(**data)
    elif role == 'admin':
        return Admin(**data)
    return User(**data)
