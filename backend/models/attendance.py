"""
Attendance and QR Code Models
"""

from datetime import datetime, timedelta
from typing import Optional
import uuid
import hashlib


class Attendance:
    """Attendance record for a student in a lecture."""
    
    def __init__(
        self,
        id: str = None,
        course_id: str = "",
        student_id: str = "",
        date: str = None,
        lecture_id: str = "",
        is_present: bool = True,
        marked_at: str = None,
        marked_via: str = "qr"  # qr, manual
    ):
        self.id = id or str(uuid.uuid4())
        self.course_id = course_id
        self.student_id = student_id
        self.date = date or datetime.now().strftime('%Y-%m-%d')
        self.lecture_id = lecture_id
        self.is_present = is_present
        self.marked_at = marked_at or datetime.now().isoformat()
        self.marked_via = marked_via
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'date': self.date,
            'lecture_id': self.lecture_id,
            'is_present': self.is_present,
            'marked_at': self.marked_at,
            'marked_via': self.marked_via
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Attendance':
        return cls(
            id=data.get('id'),
            course_id=data.get('course_id', ''),
            student_id=data.get('student_id', ''),
            date=data.get('date'),
            lecture_id=data.get('lecture_id', ''),
            is_present=data.get('is_present', True),
            marked_at=data.get('marked_at'),
            marked_via=data.get('marked_via', 'qr')
        )


class QRCode:
    """QR Code model for attendance marking."""
    
    EXPIRY_MINUTES = 5
    
    def __init__(
        self,
        id: str = None,
        course_id: str = "",
        lecture_id: str = "",
        faculty_id: str = "",
        code_data: str = None,
        generated_at: str = None,
        expires_at: str = None,
        is_valid: bool = True
    ):
        self.id = id or str(uuid.uuid4())
        self.course_id = course_id
        self.lecture_id = lecture_id or str(uuid.uuid4())
        self.faculty_id = faculty_id
        self.generated_at = generated_at or datetime.now().isoformat()
        
        # Generate expiry time
        gen_time = datetime.fromisoformat(self.generated_at)
        exp_time = gen_time + timedelta(minutes=self.EXPIRY_MINUTES)
        self.expires_at = expires_at or exp_time.isoformat()
        
        # Generate unique code data
        self.code_data = code_data or self._generate_code()
        self.is_valid = is_valid
    
    def _generate_code(self) -> str:
        """Generate unique QR code data."""
        data = f"{self.course_id}|{self.lecture_id}|{self.generated_at}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def is_expired(self) -> bool:
        """Check if QR code has expired."""
        exp_time = datetime.fromisoformat(self.expires_at)
        return datetime.now() > exp_time
    
    def validate(self) -> tuple:
        """Validate QR code. Returns (is_valid, error_message)."""
        if not self.is_valid:
            return False, "QR code has been invalidated"
        if self.is_expired():
            return False, "QR code has expired"
        return True, None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'course_id': self.course_id,
            'lecture_id': self.lecture_id,
            'faculty_id': self.faculty_id,
            'code_data': self.code_data,
            'generated_at': self.generated_at,
            'expires_at': self.expires_at,
            'is_valid': self.is_valid
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'QRCode':
        return cls(
            id=data.get('id'),
            course_id=data.get('course_id', ''),
            lecture_id=data.get('lecture_id', ''),
            faculty_id=data.get('faculty_id', ''),
            code_data=data.get('code_data'),
            generated_at=data.get('generated_at'),
            expires_at=data.get('expires_at'),
            is_valid=data.get('is_valid', True)
        )
