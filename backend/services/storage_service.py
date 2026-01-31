"""
Storage Service - JSON-based local storage
"""

import json
import os
from typing import List, Optional, Any
from datetime import datetime
import shutil


class StorageService:
    """Service for reading and writing JSON data files."""
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.join(
            os.path.dirname(__file__), '..', '..', 'data'
        )
        os.makedirs(self.data_dir, exist_ok=True)
        self._initialize_data_files()
    
    def _initialize_data_files(self):
        """Create empty data files if they don't exist."""
        files = [
            'users.json', 'courses.json', 'timetable.json',
            'assignments.json', 'submissions.json', 'grades.json',
            'rooms.json', 'bookings.json',
            'attendance.json', 'qrcodes.json',
            'announcements.json'
        ]
        for filename in files:
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                self._write_file(filepath, [])
    
    def _get_filepath(self, collection: str) -> str:
        """Get full path for a collection file."""
        return os.path.join(self.data_dir, f"{collection}.json")
    
    def _read_file(self, filepath: str) -> List[dict]:
        """Read JSON file and return data."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write_file(self, filepath: str, data: List[dict]):
        """Write data to JSON file with backup."""
        # Create backup before writing
        if os.path.exists(filepath):
            backup_path = filepath + '.backup'
            shutil.copy2(filepath, backup_path)
        
        # Write atomically (write to temp, then rename)
        temp_path = filepath + '.tmp'
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Replace original with temp
        os.replace(temp_path, filepath)
    
    # CRUD Operations
    
    def get_all(self, collection: str) -> List[dict]:
        """Get all records from a collection."""
        filepath = self._get_filepath(collection)
        return self._read_file(filepath)
    
    def get_by_id(self, collection: str, id: str) -> Optional[dict]:
        """Get a single record by ID."""
        data = self.get_all(collection)
        for item in data:
            if item.get('id') == id:
                return item
        return None
    
    def get_by_field(self, collection: str, field: str, value: Any) -> List[dict]:
        """Get records matching a field value."""
        data = self.get_all(collection)
        return [item for item in data if item.get(field) == value]
    
    def create(self, collection: str, record: dict) -> dict:
        """Create a new record."""
        data = self.get_all(collection)
        data.append(record)
        filepath = self._get_filepath(collection)
        self._write_file(filepath, data)
        return record
    
    def update(self, collection: str, id: str, updates: dict) -> Optional[dict]:
        """Update an existing record."""
        data = self.get_all(collection)
        for i, item in enumerate(data):
            if item.get('id') == id:
                data[i].update(updates)
                filepath = self._get_filepath(collection)
                self._write_file(filepath, data)
                return data[i]
        return None
    
    def delete(self, collection: str, id: str) -> bool:
        """Delete a record by ID."""
        data = self.get_all(collection)
        original_length = len(data)
        data = [item for item in data if item.get('id') != id]
        
        if len(data) < original_length:
            filepath = self._get_filepath(collection)
            self._write_file(filepath, data)
            return True
        return False
    
    def query(self, collection: str, filters: dict) -> List[dict]:
        """Query records with multiple filters."""
        data = self.get_all(collection)
        results = data
        
        for field, value in filters.items():
            if value is not None:
                results = [item for item in results if item.get(field) == value]
        
        return results
    
    def count(self, collection: str, filters: dict = None) -> int:
        """Count records, optionally with filters."""
        if filters:
            return len(self.query(collection, filters))
        return len(self.get_all(collection))


# Global storage instance
storage = StorageService()


# Helper functions for easy access
def load_data(collection: str) -> List[dict]:
    return storage.get_all(collection)

def save_data(collection: str, record: dict) -> dict:
    return storage.create(collection, record)

def get_by_id(collection: str, id: str) -> Optional[dict]:
    return storage.get_by_id(collection, id)

def update_record(collection: str, id: str, updates: dict) -> Optional[dict]:
    return storage.update(collection, id, updates)

def delete_record(collection: str, id: str) -> bool:
    return storage.delete(collection, id)
