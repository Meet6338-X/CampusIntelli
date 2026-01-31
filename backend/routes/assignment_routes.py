"""
Assignment Routes
"""

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os, sys, uuid
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.storage_service import storage
from models.assignment import Assignment, Submission, Grade
from routes.auth_routes import token_required, role_required

assignment_bp = Blueprint('assignments', __name__)
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'zip', 'txt'}


@assignment_bp.route('/', methods=['GET'])
@token_required
def get_assignments(user):
    assignments = storage.get_all('assignments')
    
    if user['role'] == 'student':
        submissions = storage.get_by_field('submissions', 'student_id', user['id'])
        submitted_ids = {s['assignment_id'] for s in submissions}
        for a in assignments:
            a['submitted'] = a['id'] in submitted_ids
    
    return jsonify({'assignments': assignments}), 200


@assignment_bp.route('/<assignment_id>', methods=['GET'])
@token_required
def get_assignment(user, assignment_id):
    assignment = storage.get_by_id('assignments', assignment_id)
    if not assignment:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'assignment': assignment}), 200


@assignment_bp.route('/', methods=['POST'])
@token_required
@role_required('faculty', 'admin')
def create_assignment(user):
    data = request.get_json()
    assignment = Assignment(
        course_id=data.get('course_id', ''),
        title=data.get('title', ''),
        description=data.get('description', ''),
        due_date=data.get('due_date', ''),
        max_marks=data.get('max_marks', 100),
        created_by=user['id']
    )
    saved = storage.create('assignments', assignment.to_dict())
    return jsonify({'assignment': saved}), 201


@assignment_bp.route('/grades', methods=['GET'])
@token_required
def get_grades(user):
    if user['role'] == 'student':
        grades = storage.get_by_field('grades', 'student_id', user['id'])
    else:
        grades = storage.get_all('grades')
    return jsonify({'grades': grades}), 200
