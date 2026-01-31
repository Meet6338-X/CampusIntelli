"""
Pytest Configuration and Fixtures
"""

import pytest
import sys
import os
import json
import tempfile
import shutil

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app as flask_app
from services.storage_service import storage


@pytest.fixture
def app():
    """Create application for testing."""
    flask_app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key'
    })
    yield flask_app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def temp_data_dir():
    """Create temporary data directory for tests."""
    temp_dir = tempfile.mkdtemp()
    old_data_dir = storage.data_dir
    storage.data_dir = temp_dir
    yield temp_dir
    storage.data_dir = old_data_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_user():
    """Sample student user."""
    return {
        'id': 'test-student-001',
        'email': 'test.student@campus.edu',
        'name': 'Test Student',
        'role': 'student',
        'department': 'Computer Science',
        'is_active': True
    }


@pytest.fixture
def sample_faculty():
    """Sample faculty user."""
    return {
        'id': 'test-faculty-001',
        'email': 'test.faculty@campus.edu',
        'name': 'Test Faculty',
        'role': 'faculty',
        'department': 'Computer Science',
        'is_active': True
    }


@pytest.fixture
def sample_admin():
    """Sample admin user."""
    return {
        'id': 'test-admin-001',
        'email': 'test.admin@campus.edu',
        'name': 'Test Admin',
        'role': 'admin',
        'department': 'Administration',
        'is_active': True
    }


@pytest.fixture
def sample_course():
    """Sample course."""
    return {
        'id': 'course-test-001',
        'code': 'CS101',
        'name': 'Introduction to Programming',
        'department': 'Computer Science',
        'credits': 4,
        'instructor_id': 'test-faculty-001'
    }


@pytest.fixture
def sample_assignment():
    """Sample assignment."""
    return {
        'id': 'assign-test-001',
        'course_id': 'course-test-001',
        'title': 'Test Assignment',
        'description': 'Test assignment description',
        'due_date': '2026-02-15T23:59:00',
        'max_marks': 100,
        'created_by': 'test-faculty-001'
    }


@pytest.fixture
def auth_headers_student(client, sample_user, temp_data_dir):
    """Get authentication headers for student."""
    from services.auth_service import bcrypt
    
    # Create user in storage
    user = sample_user.copy()
    user['password'] = bcrypt.generate_password_hash('password123').decode('utf-8')
    storage.create('users', user)
    
    # Login
    response = client.post('/api/auth/login', json={
        'email': sample_user['email'],
        'password': 'password123'
    })
    
    data = response.get_json()
    return {'Authorization': f'Bearer {data.get("token", "")}'}


@pytest.fixture
def auth_headers_faculty(client, sample_faculty, temp_data_dir):
    """Get authentication headers for faculty."""
    from services.auth_service import bcrypt
    
    user = sample_faculty.copy()
    user['password'] = bcrypt.generate_password_hash('password123').decode('utf-8')
    storage.create('users', user)
    
    response = client.post('/api/auth/login', json={
        'email': sample_faculty['email'],
        'password': 'password123'
    })
    
    data = response.get_json()
    return {'Authorization': f'Bearer {data.get("token", "")}'}


@pytest.fixture
def auth_headers_admin(client, sample_admin, temp_data_dir):
    """Get authentication headers for admin."""
    from services.auth_service import bcrypt
    
    user = sample_admin.copy()
    user['password'] = bcrypt.generate_password_hash('password123').decode('utf-8')
    storage.create('users', user)
    
    response = client.post('/api/auth/login', json={
        'email': sample_admin['email'],
        'password': 'password123'
    })
    
    data = response.get_json()
    return {'Authorization': f'Bearer {data.get("token", "")}'}
