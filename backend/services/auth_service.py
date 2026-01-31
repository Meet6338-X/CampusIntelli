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
    users = storage.get_all('users')
    if not users:
        samples = [
            {'email': 'student@campus.edu', 'password': 'student123', 'name': 'John Student', 'role': 'student', 'department': 'Computer Science'},
            {'email': 'faculty@campus.edu', 'password': 'faculty123', 'name': 'Dr. Sarah Faculty', 'role': 'faculty', 'department': 'Computer Science'},
            {'email': 'admin@campus.edu', 'password': 'admin123', 'name': 'System Admin', 'role': 'admin', 'department': 'IT'}
        ]
        for s in samples:
            AuthService.register(s)
        print("[OK] Sample users created")
