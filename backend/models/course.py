"""
Course and Timetable Models
"""

from datetime import datetime
from typing import List, Optional
import uuid


class Course:
    """Course model with schedule and assignment info."""
    
    def __init__(
        self,
        id: str = None,
        code: str = "",
        name: str = "",
        description: str = "",
        credits: int = 3,
        department: str = "",
        instructor_id: str = "",
        students: List[str] = None,
        created_at: str = None
    ):
        self.id = id or str(uuid.uuid4())
        self.code = code
        self.name = name
        self.description = description
        self.credits = credits
        self.department = department
        self.instructor_id = instructor_id
        self.students = students or []
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'credits': self.credits,
            'department': self.department,
            'instructor_id': self.instructor_id,
            'students': self.students,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Course':
        return cls(
            id=data.get('id'),
            code=data.get('code', ''),
            name=data.get('name', ''),
            description=data.get('description', ''),
            credits=data.get('credits', 3),
            department=data.get('department', ''),
            instructor_id=data.get('instructor_id', ''),
            students=data.get('students', []),
            created_at=data.get('created_at')
        )


class TimetableEntry:
    """Single timetable entry for a course session."""
    
    def __init__(
        self,
        id: str = None,
        course_id: str = "",
        day: str = "",  # Monday, Tuesday, etc.
        start_time: str = "",  # HH:MM format
        end_time: str = "",
        room_id: str = "",
        room_name: str = ""
    ):
        self.id = id or str(uuid.uuid4())
        self.course_id = course_id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.room_id = room_id
        self.room_name = room_name
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'course_id': self.course_id,
            'day': self.day,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'room_id': self.room_id,
            'room_name': self.room_name
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TimetableEntry':
        return cls(
            id=data.get('id'),
            course_id=data.get('course_id', ''),
            day=data.get('day', ''),
            start_time=data.get('start_time', ''),
            end_time=data.get('end_time', ''),
            room_id=data.get('room_id', ''),
            room_name=data.get('room_name', '')
        )
