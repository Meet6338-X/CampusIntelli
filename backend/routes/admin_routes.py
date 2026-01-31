"""
Admin Routes - User Management and System Configuration
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.storage_service import storage
from models.user import User
from routes.auth_routes import token_required, role_required

admin_bp = Blueprint('admin', __name__)


# ==========================================
# USER MANAGEMENT
# ==========================================

@admin_bp.route('/users', methods=['GET'])
@token_required
@role_required('admin')
def get_all_users(user):
    """Get all users with pagination and filtering."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    role_filter = request.args.get('role')
    search = request.args.get('search', '').lower()
    
    users = storage.get_all('users')
    
    # Filter by role
    if role_filter:
        users = [u for u in users if u.get('role') == role_filter]
    
    # Search by name or email
    if search:
        users = [u for u in users if 
                 search in u.get('name', '').lower() or 
                 search in u.get('email', '').lower()]
    
    # Remove sensitive data
    for u in users:
        u.pop('password', None)
    
    # Pagination
    total = len(users)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = users[start:end]
    
    return jsonify({
        'users': paginated,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }), 200


@admin_bp.route('/users', methods=['POST'])
@token_required
@role_required('admin')
def create_user(user):
    """Create a new user."""
    data = request.get_json()
    
    required_fields = ['email', 'password', 'name', 'role']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if email exists
    existing = storage.get_by_field('users', 'email', data['email'])
    if existing:
        return jsonify({'error': 'Email already registered'}), 400
    
    # Validate role
    valid_roles = ['student', 'faculty', 'admin']
    if data['role'] not in valid_roles:
        return jsonify({'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}'}), 400
    
    # Hash password and create user
    from services.auth_service import bcrypt
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    new_user = User(
        email=data['email'],
        password=hashed_password,
        name=data['name'],
        role=data['role'],
        department=data.get('department', '')
    )
    
    saved = storage.create('users', new_user.to_dict())
    saved.pop('password', None)
    
    return jsonify({'user': saved, 'message': 'User created successfully'}), 201


@admin_bp.route('/users/<user_id>', methods=['GET'])
@token_required
@role_required('admin')
def get_user(user, user_id):
    """Get a single user by ID."""
    target_user = storage.get_by_id('users', user_id)
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    target_user.pop('password', None)
    return jsonify({'user': target_user}), 200


@admin_bp.route('/users/<user_id>', methods=['PUT'])
@token_required
@role_required('admin')
def update_user(user, user_id):
    """Update user details."""
    target_user = storage.get_by_id('users', user_id)
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update allowed fields
    updatable_fields = ['name', 'role', 'department', 'is_active']
    for field in updatable_fields:
        if field in data:
            target_user[field] = data[field]
    
    # Validate role if being updated
    if 'role' in data:
        valid_roles = ['student', 'faculty', 'admin']
        if data['role'] not in valid_roles:
            return jsonify({'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}'}), 400
    
    # Update password if provided
    if data.get('password'):
        from services.auth_service import bcrypt
        target_user['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    updated = storage.update('users', user_id, target_user)
    updated.pop('password', None)
    
    return jsonify({'user': updated, 'message': 'User updated successfully'}), 200


@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_user(user, user_id):
    """Delete or deactivate a user."""
    target_user = storage.get_by_id('users', user_id)
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    # Prevent self-deletion
    if user_id == user['id']:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    # Soft delete by setting is_active to False
    target_user['is_active'] = False
    target_user['deleted_at'] = datetime.now().isoformat()
    storage.update('users', user_id, target_user)
    
    return jsonify({'message': 'User deactivated successfully'}), 200


@admin_bp.route('/users/<user_id>/restore', methods=['POST'])
@token_required
@role_required('admin')
def restore_user(user, user_id):
    """Restore a deactivated user."""
    target_user = storage.get_by_id('users', user_id)
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    target_user['is_active'] = True
    target_user.pop('deleted_at', None)
    storage.update('users', user_id, target_user)
    
    return jsonify({'message': 'User restored successfully'}), 200


# ==========================================
# ROLE MANAGEMENT
# ==========================================

@admin_bp.route('/users/<user_id>/role', methods=['PUT'])
@token_required
@role_required('admin')
def update_user_role(user, user_id):
    """Update a user's role specifically."""
    target_user = storage.get_by_id('users', user_id)
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    new_role = data.get('role')
    
    valid_roles = ['student', 'faculty', 'admin']
    if new_role not in valid_roles:
        return jsonify({'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}'}), 400
    
    old_role = target_user.get('role')
    target_user['role'] = new_role
    storage.update('users', user_id, target_user)
    
    return jsonify({
        'message': f'Role updated from {old_role} to {new_role}',
        'user_id': user_id
    }), 200


# ==========================================
# SYSTEM STATS
# ==========================================

@admin_bp.route('/stats', methods=['GET'])
@token_required
@role_required('admin')
def get_system_stats(user):
    """Get system-wide statistics."""
    users = storage.get_all('users')
    courses = storage.get_all('courses')
    assignments = storage.get_all('assignments')
    submissions = storage.get_all('submissions')
    bookings = storage.get_all('bookings')
    attendance = storage.get_all('attendance')
    
    # User breakdown
    role_counts = {'student': 0, 'faculty': 0, 'admin': 0}
    active_users = 0
    for u in users:
        role = u.get('role', 'student')
        role_counts[role] = role_counts.get(role, 0) + 1
        if u.get('is_active', True):
            active_users += 1
    
    # Submission stats
    graded = len([s for s in submissions if s.get('marks') is not None])
    pending = len(submissions) - graded
    
    # Booking stats
    today = datetime.now().strftime('%Y-%m-%d')
    today_bookings = len([b for b in bookings if b.get('date') == today])
    
    stats = {
        'users': {
            'total': len(users),
            'active': active_users,
            'by_role': role_counts
        },
        'courses': {
            'total': len(courses)
        },
        'assignments': {
            'total': len(assignments),
            'submissions': len(submissions),
            'graded': graded,
            'pending_grading': pending
        },
        'bookings': {
            'total': len(bookings),
            'today': today_bookings
        },
        'attendance': {
            'total_records': len(attendance)
        }
    }
    
    return jsonify({'stats': stats}), 200


# ==========================================
# BULK OPERATIONS
# ==========================================

@admin_bp.route('/users/bulk-create', methods=['POST'])
@token_required
@role_required('admin')
def bulk_create_users(user):
    """Bulk create users from a list."""
    data = request.get_json()
    users_data = data.get('users', [])
    
    if not users_data:
        return jsonify({'error': 'No users provided'}), 400
    
    from services.auth_service import bcrypt
    
    created = []
    errors = []
    
    for idx, user_data in enumerate(users_data):
        try:
            # Check required fields
            if not all([user_data.get('email'), user_data.get('name'), user_data.get('password')]):
                errors.append({'index': idx, 'error': 'Missing required fields'})
                continue
            
            # Check if email exists
            existing = storage.get_by_field('users', 'email', user_data['email'])
            if existing:
                errors.append({'index': idx, 'error': 'Email already exists', 'email': user_data['email']})
                continue
            
            hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            
            new_user = User(
                email=user_data['email'],
                password=hashed_password,
                name=user_data['name'],
                role=user_data.get('role', 'student'),
                department=user_data.get('department', '')
            )
            
            saved = storage.create('users', new_user.to_dict())
            saved.pop('password', None)
            created.append(saved)
            
        except Exception as e:
            errors.append({'index': idx, 'error': str(e)})
    
    return jsonify({
        'created': len(created),
        'failed': len(errors),
        'users': created,
        'errors': errors
    }), 201 if created else 400
