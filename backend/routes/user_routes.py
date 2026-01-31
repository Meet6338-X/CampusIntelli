"""
User Management Routes
"""

from flask import Blueprint, request, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.storage_service import storage
from routes.auth_routes import token_required, role_required

user_bp = Blueprint('users', __name__)


@user_bp.route('/', methods=['GET'])
@token_required
@role_required('admin')
def get_all_users(user):
    users = storage.get_all('users')
    safe_users = [{k: v for k, v in u.items() if k != 'password_hash'} for u in users]
    return jsonify({'users': safe_users}), 200


@user_bp.route('/<user_id>', methods=['GET'])
@token_required
def get_user(user, user_id):
    if user['id'] != user_id and user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    target_user = storage.get_by_id('users', user_id)
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    safe_user = {k: v for k, v in target_user.items() if k != 'password_hash'}
    return jsonify({'user': safe_user}), 200


@user_bp.route('/<user_id>', methods=['PUT'])
@token_required
def update_user(user, user_id):
    if user['id'] != user_id and user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    protected = ['id', 'email', 'password_hash', 'role', 'created_at']
    updates = {k: v for k, v in data.items() if k not in protected}
    
    if user['role'] == 'admin' and 'role' in data:
        updates['role'] = data['role']
    
    updated = storage.update('users', user_id, updates)
    if not updated:
        return jsonify({'error': 'User not found'}), 404
    
    safe_user = {k: v for k, v in updated.items() if k != 'password_hash'}
    return jsonify({'user': safe_user, 'message': 'Profile updated'}), 200


@user_bp.route('/directory', methods=['GET'])
@token_required
def get_directory(user):
    query = request.args.get('q', '').lower()
    users = storage.get_all('users')
    
    if query:
        users = [u for u in users if query in u.get('name', '').lower() or query in u.get('email', '').lower()]
    
    directory = [{'id': u['id'], 'name': u.get('name', ''), 'email': u.get('email', ''), 
                  'role': u.get('role', ''), 'department': u.get('department', '')} for u in users]
    return jsonify({'directory': directory}), 200
