"""
Announcement Model
"""

from datetime import datetime
from typing import Optional
import uuid


class Announcement:
    """Announcement model for campus news and updates."""
    
    def __init__(
        self,
        id: str = None,
        title: str = "",
        content: str = "",
        author_id: str = "",
        author_name: str = "",
        category: str = "general",  # general, academic, event, urgent
        target_audience: str = "all",  # all, students, faculty, department-specific
        is_pinned: bool = False,
        published_at: str = None,
        expires_at: str = None
    ):
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.content = content
        self.author_id = author_id
        self.author_name = author_name
        self.category = category
        self.target_audience = target_audience
        self.is_pinned = is_pinned
        self.published_at = published_at or datetime.now().isoformat()
        self.expires_at = expires_at
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'author_name': self.author_name,
            'category': self.category,
            'target_audience': self.target_audience,
            'is_pinned': self.is_pinned,
            'published_at': self.published_at,
            'expires_at': self.expires_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Announcement':
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            content=data.get('content', ''),
            author_id=data.get('author_id', ''),
            author_name=data.get('author_name', ''),
            category=data.get('category', 'general'),
            target_audience=data.get('target_audience', 'all'),
            is_pinned=data.get('is_pinned', False),
            published_at=data.get('published_at'),
            expires_at=data.get('expires_at')
        )
