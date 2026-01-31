"""
Tests for Admin Routes
"""

import pytest


class TestAdminUserManagement:
    """Test admin user management endpoints."""
    
    def test_get_all_users(self, client, auth_headers_admin, temp_data_dir):
        """Test getting all users as admin."""
        response = client.get('/api/admin/users', headers=auth_headers_admin)
        assert response.status_code == 200
        data = response.get_json()
        assert 'users' in data
        assert 'total' in data
    
    def test_get_users_without_admin_fails(self, client, auth_headers_student):
        """Test that non-admins cannot access user list."""
        response = client.get('/api/admin/users', headers=auth_headers_student)
        assert response.status_code == 403
    
    def test_create_user(self, client, auth_headers_admin, temp_data_dir):
        """Test creating a new user."""
        response = client.post('/api/admin/users',
            headers={'Content-Type': 'application/json', **auth_headers_admin},
            json={
                'email': 'newuser@campus.edu',
                'password': 'newpassword123',
                'name': 'New User',
                'role': 'student',
                'department': 'Physics'
            })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['user']['email'] == 'newuser@campus.edu'
        assert 'password' not in data['user']  # Password should be removed
    
    def test_update_user_role(self, client, auth_headers_admin, sample_user, temp_data_dir):
        """Test updating a user's role."""
        from services.storage_service import storage
        from services.auth_service import bcrypt
        
        user = sample_user.copy()
        user['password'] = bcrypt.generate_password_hash('pass').decode('utf-8')
        storage.create('users', user)
        
        response = client.put(f'/api/admin/users/{user["id"]}/role',
            headers={'Content-Type': 'application/json', **auth_headers_admin},
            json={'role': 'faculty'})
        
        assert response.status_code == 200
    
    def test_delete_user(self, client, auth_headers_admin, sample_user, temp_data_dir):
        """Test deactivating a user."""
        from services.storage_service import storage
        from services.auth_service import bcrypt
        
        user = sample_user.copy()
        user['password'] = bcrypt.generate_password_hash('pass').decode('utf-8')
        storage.create('users', user)
        
        response = client.delete(f'/api/admin/users/{user["id"]}',
            headers=auth_headers_admin)
        
        assert response.status_code == 200


class TestAdminStats:
    """Test admin stats endpoints."""
    
    def test_get_system_stats(self, client, auth_headers_admin, temp_data_dir):
        """Test getting system statistics."""
        response = client.get('/api/admin/stats', headers=auth_headers_admin)
        assert response.status_code == 200
        data = response.get_json()
        assert 'stats' in data
        assert 'users' in data['stats']
