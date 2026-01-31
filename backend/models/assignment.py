"""
Assignment and Submission Models
"""

from datetime import datetime
from typing import Optional
import uuid


class Assignment:
    """Assignment model for course assignments."""
    
    def __init__(
        self,
        id: str = None,
        course_id: str = "",
        title: str = "",
        description: str = "",
        due_date: str = "",
        max_marks: int = 100,
        created_by: str = "",
        created_at: str = None,
        attachments: list = None
    ):
        self.id = id or str(uuid.uuid4())
        self.course_id = course_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.max_marks = max_marks
        self.created_by = created_by
        self.created_at = created_at or datetime.now().isoformat()
        self.attachments = attachments or []
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'max_marks': self.max_marks,
            'created_by': self.created_by,
            'created_at': self.created_at,
            'attachments': self.attachments
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Assignment':
        return cls(
            id=data.get('id'),
            course_id=data.get('course_id', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            due_date=data.get('due_date', ''),
            max_marks=data.get('max_marks', 100),
            created_by=data.get('created_by', ''),
            created_at=data.get('created_at'),
            attachments=data.get('attachments', [])
        )


class Submission:
    """Submission model for assignment submissions."""
    
    def __init__(
        self,
        id: str = None,
        assignment_id: str = "",
        student_id: str = "",
        file_path: str = "",
        file_name: str = "",
        submitted_at: str = None,
        marks: int = None,
        feedback: str = "",
        is_late: bool = False,
        graded_at: str = None,
        graded_by: str = ""
    ):
        self.id = id or str(uuid.uuid4())
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.file_path = file_path
        self.file_name = file_name
        self.submitted_at = submitted_at or datetime.now().isoformat()
        self.marks = marks
        self.feedback = feedback
        self.is_late = is_late
        self.graded_at = graded_at
        self.graded_by = graded_by
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'assignment_id': self.assignment_id,
            'student_id': self.student_id,
            'file_path': self.file_path,
            'file_name': self.file_name,
            'submitted_at': self.submitted_at,
            'marks': self.marks,
            'feedback': self.feedback,
            'is_late': self.is_late,
            'graded_at': self.graded_at,
            'graded_by': self.graded_by
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Submission':
        return cls(
            id=data.get('id'),
            assignment_id=data.get('assignment_id', ''),
            student_id=data.get('student_id', ''),
            file_path=data.get('file_path', ''),
            file_name=data.get('file_name', ''),
            submitted_at=data.get('submitted_at'),
            marks=data.get('marks'),
            feedback=data.get('feedback', ''),
            is_late=data.get('is_late', False),
            graded_at=data.get('graded_at'),
            graded_by=data.get('graded_by', '')
        )


class Grade:
    """Grade record for student course grades."""
    
    def __init__(
        self,
        id: str = None,
        student_id: str = "",
        course_id: str = "",
        assignment_id: str = "",
        marks: int = 0,
        max_marks: int = 100,
        grade_letter: str = "",
        graded_at: str = None
    ):
        self.id = id or str(uuid.uuid4())
        self.student_id = student_id
        self.course_id = course_id
        self.assignment_id = assignment_id
        self.marks = marks
        self.max_marks = max_marks
        self.grade_letter = grade_letter or self._calculate_grade()
        self.graded_at = graded_at or datetime.now().isoformat()
    
    def _calculate_grade(self) -> str:
        """Calculate letter grade from percentage."""
        if self.max_marks == 0:
            return 'N/A'
        percentage = (self.marks / self.max_marks) * 100
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B'
        elif percentage >= 60:
            return 'C'
        elif percentage >= 50:
            return 'D'
        else:
            return 'F'
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'assignment_id': self.assignment_id,
            'marks': self.marks,
            'max_marks': self.max_marks,
            'grade_letter': self.grade_letter,
            'graded_at': self.graded_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Grade':
        return cls(
            id=data.get('id'),
            student_id=data.get('student_id', ''),
            course_id=data.get('course_id', ''),
            assignment_id=data.get('assignment_id', ''),
            marks=data.get('marks', 0),
            max_marks=data.get('max_marks', 100),
            grade_letter=data.get('grade_letter', ''),
            graded_at=data.get('graded_at')
        )
