"""
Room and Booking Models
"""

from datetime import datetime
from typing import List, Optional
import uuid


class Room:
    """Room model for bookable spaces."""
    
    def __init__(
        self,
        id: str = None,
        name: str = "",
        building: str = "",
        floor: int = 1,
        capacity: int = 30,
        room_type: str = "classroom",  # classroom, lab, conference, auditorium
        equipment: List[str] = None,
        is_available: bool = True
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.building = building
        self.floor = floor
        self.capacity = capacity
        self.room_type = room_type
        self.equipment = equipment or []
        self.is_available = is_available
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'building': self.building,
            'floor': self.floor,
            'capacity': self.capacity,
            'room_type': self.room_type,
            'equipment': self.equipment,
            'is_available': self.is_available
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Room':
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            building=data.get('building', ''),
            floor=data.get('floor', 1),
            capacity=data.get('capacity', 30),
            room_type=data.get('room_type', 'classroom'),
            equipment=data.get('equipment', []),
            is_available=data.get('is_available', True)
        )


class Booking:
    """Booking model for room reservations."""
    
    def __init__(
        self,
        id: str = None,
        room_id: str = "",
        user_id: str = "",
        date: str = "",
        start_time: str = "",
        end_time: str = "",
        purpose: str = "",
        status: str = "confirmed",  # pending, confirmed, cancelled
        created_at: str = None
    ):
        self.id = id or str(uuid.uuid4())
        self.room_id = room_id
        self.user_id = user_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.purpose = purpose
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'room_id': self.room_id,
            'user_id': self.user_id,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'purpose': self.purpose,
            'status': self.status,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Booking':
        return cls(
            id=data.get('id'),
            room_id=data.get('room_id', ''),
            user_id=data.get('user_id', ''),
            date=data.get('date', ''),
            start_time=data.get('start_time', ''),
            end_time=data.get('end_time', ''),
            purpose=data.get('purpose', ''),
            status=data.get('status', 'confirmed'),
            created_at=data.get('created_at')
        )
