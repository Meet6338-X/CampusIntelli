"""
Course Routes
"""

from flask import Blueprint, request, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.storage_service import storage
from models.course import Course, TimetableEntry
from routes.auth_routes import token_required, role_required

course_bp = Blueprint('courses', __name__)


@course_bp.route('/', methods=['GET'])
@token_required
def get_courses(user):
    courses = storage.get_all('courses')
    return jsonify({'courses': courses}), 200


@course_bp.route('/<course_id>', methods=['GET'])
@token_required
def get_course(user, course_id):
    course = storage.get_by_id('courses', course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    return jsonify({'course': course}), 200


@course_bp.route('/', methods=['POST'])
@token_required
@role_required('admin', 'faculty')
def create_course(user):
    data = request.get_json()
    course = Course(
        code=data.get('code', ''),
        name=data.get('name', ''),
        description=data.get('description', ''),
        credits=data.get('credits', 3),
        department=data.get('department', ''),
        instructor_id=data.get('instructor_id', user['id'])
    )
    saved = storage.create('courses', course.to_dict())
    return jsonify({'course': saved, 'message': 'Course created'}), 201


@course_bp.route('/timetable', methods=['GET'])
@token_required
def get_timetable(user):
    entries = storage.get_all('timetable')
    return jsonify({'timetable': entries}), 200
