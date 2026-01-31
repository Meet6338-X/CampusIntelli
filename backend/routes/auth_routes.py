"""
Authentication Routes
"""

from flask import Blueprint, request, jsonify
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.auth_service import AuthService
from services.storage_service import storage
from functools import wraps

auth_bp = Blueprint('auth', __name__)


def token_required(f):
    """Decorator to require valid JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        user = AuthService.get_current_user(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        return f(user, *args, **kwargs)
    return decorated


def role_required(*roles):
    """Decorator to require specific roles."""
    def decorator(f):
        @wraps(f)
        def decorated(user, *args, **kwargs):
            if user.get('role') not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(user, *args, **kwargs)
        return decorated
    return decorator


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    success, user_data, message = AuthService.authenticate(email, password)
    
    if success:
        return jsonify({'message': message, 'user': user_data}), 200
    else:
        return jsonify({'error': message}), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    for field in ['email', 'password', 'name']:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    success, user_data, message = AuthService.register(data)
    
    if success:
        return jsonify({'message': message, 'user': user_data}), 201
    else:
        return jsonify({'error': message}), 400


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(user):
    return jsonify({'user': user}), 200


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(user):
    return jsonify({'message': 'Logged out successfully'}), 200
