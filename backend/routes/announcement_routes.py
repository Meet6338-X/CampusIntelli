"""
Announcement Routes
"""

from flask import Blueprint, request, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.storage_service import storage
from models.announcement import Announcement
from routes.auth_routes import token_required, role_required

announcement_bp = Blueprint('announcements', __name__)


@announcement_bp.route('/', methods=['GET'])
@token_required
def get_announcements(user):
    announcements = storage.get_all('announcements')
    announcements.sort(key=lambda x: (not x.get('is_pinned', False), x.get('published_at', '')), reverse=True)
    return jsonify({'announcements': announcements}), 200


@announcement_bp.route('/', methods=['POST'])
@token_required
@role_required('admin', 'faculty')
def create_announcement(user):
    data = request.get_json()
    announcement = Announcement(
        title=data.get('title', ''),
        content=data.get('content', ''),
        author_id=user['id'],
        author_name=user.get('name', ''),
        category=data.get('category', 'general'),
        target_audience=data.get('target_audience', 'all'),
        is_pinned=data.get('is_pinned', False)
    )
    saved = storage.create('announcements', announcement.to_dict())
    return jsonify({'announcement': saved}), 201


@announcement_bp.route('/<announcement_id>', methods=['GET'])
@token_required
def get_announcement(user, announcement_id):
    """Get single announcement by ID."""
    announcement = storage.get_by_id('announcements', announcement_id)
    if not announcement:
        return jsonify({'error': 'Announcement not found'}), 404
    return jsonify({'announcement': announcement}), 200


@announcement_bp.route('/<announcement_id>', methods=['PUT'])
@token_required
@role_required('admin', 'faculty')
def update_announcement(user, announcement_id):
    """Update announcement - Author or Admin only."""
    announcement = storage.get_by_id('announcements', announcement_id)
    if not announcement:
        return jsonify({'error': 'Announcement not found'}), 404
    
    # Only admin or the author can update
    if user['role'] != 'admin' and announcement.get('author_id') != user['id']:
        return jsonify({'error': 'Not authorized to edit this announcement'}), 403
    
    data = request.get_json()
    
    updatable = ['title', 'content', 'category', 'target_audience', 
                 'is_pinned', 'expires_at', 'priority']
    
    for field in updatable:
        if field in data:
            announcement[field] = data[field]
    
    announcement['updated_at'] = __import__('datetime').datetime.now().isoformat()
    announcement['updated_by'] = user['id']
    
    updated = storage.update('announcements', announcement_id, announcement)
    return jsonify({'announcement': updated, 'message': 'Announcement updated successfully'}), 200


@announcement_bp.route('/<announcement_id>', methods=['DELETE'])
@token_required
@role_required('admin', 'faculty')
def delete_announcement(user, announcement_id):
    """Delete announcement - Author or Admin only."""
    announcement = storage.get_by_id('announcements', announcement_id)
    if not announcement:
        return jsonify({'error': 'Announcement not found'}), 404
    
    # Only admin or the author can delete
    if user['role'] != 'admin' and announcement.get('author_id') != user['id']:
        return jsonify({'error': 'Not authorized to delete this announcement'}), 403
    
    storage.delete('announcements', announcement_id)
    return jsonify({'message': 'Announcement deleted successfully'}), 200
