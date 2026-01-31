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


@announcement_bp.route('/<announcement_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_announcement(user, announcement_id):
    storage.delete('announcements', announcement_id)
    return jsonify({'message': 'Deleted'}), 200
