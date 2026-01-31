"""
Materials Model - Lecture Materials and Course Resources
"""

from datetime import datetime
from typing import Optional
import uuid


class Material:
    """Material model for lecture materials and course resources."""
    
    def __init__(
        self,
        id: str = None,
        course_id: str = "",
        title: str = "",
        description: str = "",
        file_path: str = "",
        file_name: str = "",
        file_type: str = "",
        file_size: int = 0,
        uploaded_by: str = "",
        uploaded_at: str = None,
        category: str = "lecture",  # lecture, assignment, reference, other
        is_visible: bool = True
    ):
        self.id = id or str(uuid.uuid4())
        self.course_id = course_id
        self.title = title
        self.description = description
        self.file_path = file_path
        self.file_name = file_name
        self.file_type = file_type
        self.file_size = file_size
        self.uploaded_by = uploaded_by
        self.uploaded_at = uploaded_at or datetime.now().isoformat()
        self.category = category
        self.is_visible = is_visible
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'file_path': self.file_path,
            'file_name': self.file_name,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'uploaded_by': self.uploaded_by,
            'uploaded_at': self.uploaded_at,
            'category': self.category,
            'is_visible': self.is_visible
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Material':
        return cls(
            id=data.get('id'),
            course_id=data.get('course_id', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            file_path=data.get('file_path', ''),
            file_name=data.get('file_name', ''),
            file_type=data.get('file_type', ''),
            file_size=data.get('file_size', 0),
            uploaded_by=data.get('uploaded_by', ''),
            uploaded_at=data.get('uploaded_at'),
            category=data.get('category', 'lecture'),
            is_visible=data.get('is_visible', True)
        )
