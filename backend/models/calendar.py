"""
Academic Calendar and Events Model
"""

from datetime import datetime
from typing import Optional
import uuid


class Event:
    """Event model for campus events and activities."""
    
    def __init__(
        self,
        id: str = None,
        title: str = "",
        description: str = "",
        event_type: str = "general",  # general, academic, cultural, sports, holiday
        start_date: str = "",
        end_date: str = None,
        start_time: str = None,
        end_time: str = None,
        location: str = "",
        organizer_id: str = "",
        department: str = "",
        is_public: bool = True,
        is_holiday: bool = False,
        created_at: str = None,
        created_by: str = ""
    ):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.event_type = event_type
        self.start_date = start_date
        self.end_date = end_date or start_date
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.organizer_id = organizer_id
        self.department = department
        self.is_public = is_public
        self.is_holiday = is_holiday
        self.created_at = created_at or datetime.now().isoformat()
        self.created_by = created_by
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'location': self.location,
            'organizer_id': self.organizer_id,
            'department': self.department,
            'is_public': self.is_public,
            'is_holiday': self.is_holiday,
            'created_at': self.created_at,
            'created_by': self.created_by
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        return cls(**{k: data.get(k) for k in [
            'id', 'title', 'description', 'event_type', 'start_date',
            'end_date', 'start_time', 'end_time', 'location', 'organizer_id',
            'department', 'is_public', 'is_holiday', 'created_at', 'created_by'
        ]})


class AcademicCalendar:
    """Academic Calendar model for semester dates, exams, etc."""
    
    def __init__(
        self,
        id: str = None,
        academic_year: str = "",
        semester: str = "",  # Fall, Spring, Summer
        item_type: str = "",  # semester_start, semester_end, exam_start, exam_end, holiday, break, deadline
        title: str = "",
        description: str = "",
        start_date: str = "",
        end_date: str = None,
        is_active: bool = True,
        created_at: str = None,
        created_by: str = ""
    ):
        self.id = id or str(uuid.uuid4())
        self.academic_year = academic_year
        self.semester = semester
        self.item_type = item_type
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date or start_date
        self.is_active = is_active
        self.created_at = created_at or datetime.now().isoformat()
        self.created_by = created_by
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'academic_year': self.academic_year,
            'semester': self.semester,
            'item_type': self.item_type,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'created_by': self.created_by
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AcademicCalendar':
        return cls(**{k: data.get(k) for k in [
            'id', 'academic_year', 'semester', 'item_type', 'title',
            'description', 'start_date', 'end_date', 'is_active',
            'created_at', 'created_by'
        ]})


class TimetableSlot:
    """Timetable slot for classes/lectures."""
    
    def __init__(
        self,
        id: str = None,
        course_id: str = "",
        day_of_week: int = 0,  # 0=Monday, 6=Sunday
        start_time: str = "",
        end_time: str = "",
        room: str = "",
        instructor_id: str = "",
        slot_type: str = "lecture",  # lecture, lab, tutorial
        section: str = "",
        semester: str = "",
        is_active: bool = True,
        created_at: str = None
    ):
        self.id = id or str(uuid.uuid4())
        self.course_id = course_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.room = room
        self.instructor_id = instructor_id
        self.slot_type = slot_type
        self.section = section
        self.semester = semester
        self.is_active = is_active
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'course_id': self.course_id,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'room': self.room,
            'instructor_id': self.instructor_id,
            'slot_type': self.slot_type,
            'section': self.section,
            'semester': self.semester,
            'is_active': self.is_active,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TimetableSlot':
        return cls(**{k: data.get(k) for k in [
            'id', 'course_id', 'day_of_week', 'start_time', 'end_time',
            'room', 'instructor_id', 'slot_type', 'section', 'semester',
            'is_active', 'created_at'
        ]})
