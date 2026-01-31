"""
Course Routes - CRUD Operations with Faculty Management
"""

from flask import Blueprint, request, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.storage_service import storage
from models.course import Course, TimetableEntry
from routes.auth_routes import token_required, role_required

course_bp = Blueprint('courses', __name__)


# ==========================================
# COURSE CRUD OPERATIONS
# ==========================================

@course_bp.route('/', methods=['GET'])
@token_required
def get_courses(user):
    """Get all courses with optional department filter and instructor info."""
    department = request.args.get('department')
    courses = storage.get_all('courses')
    
    # Filter by department if specified
    if department:
        courses = [c for c in courses if c.get('department', '').lower() == department.lower()]
    
    # Attach instructor name to each course
    users = storage.get_all('users')
    user_map = {u['id']: u for u in users}
    
    for course in courses:
        instructor_id = course.get('instructor_id')
        if instructor_id and instructor_id in user_map:
            course['instructor_name'] = user_map[instructor_id].get('name', 'Unknown')
            course['instructor_designation'] = user_map[instructor_id].get('designation', 'Faculty')
        else:
            course['instructor_name'] = 'Not Assigned'
            course['instructor_designation'] = ''
    
    return jsonify({'courses': courses}), 200


@course_bp.route('/<course_id>', methods=['GET'])
@token_required
def get_course(user, course_id):
    """Get a single course with instructor details."""
    course = storage.get_by_id('courses', course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    # Attach instructor info
    instructor = storage.get_by_id('users', course.get('instructor_id', ''))
    if instructor:
        course['instructor_name'] = instructor.get('name', 'Unknown')
        course['instructor_designation'] = instructor.get('designation', 'Faculty')
        course['instructor_email'] = instructor.get('email', '')
    
    return jsonify({'course': course}), 200


@course_bp.route('/', methods=['POST'])
@token_required
@role_required('admin', 'faculty')
def create_course(user):
    """Create a new course."""
    data = request.get_json()
    
    # Validate required fields
    if not data.get('code') or not data.get('name'):
        return jsonify({'error': 'Course code and name are required'}), 400
    
    # Check for duplicate course code
    existing = storage.get_all('courses')
    if any(c.get('code', '').upper() == data.get('code', '').upper() for c in existing):
        return jsonify({'error': 'Course with this code already exists'}), 400
    
    course = Course(
        code=data.get('code', '').upper(),
        name=data.get('name', ''),
        description=data.get('description', ''),
        credits=int(data.get('credits', 3)),
        department=data.get('department', user.get('department', '')),
        instructor_id=data.get('instructor_id', user['id'])
    )
    saved = storage.create('courses', course.to_dict())
    return jsonify({'course': saved, 'message': 'Course created successfully'}), 201


@course_bp.route('/<course_id>', methods=['PUT'])
@token_required
@role_required('admin', 'faculty')
def update_course(user, course_id):
    """Update an existing course."""
    course = storage.get_by_id('courses', course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    # Only admin or course instructor can update
    if user['role'] != 'admin' and course.get('instructor_id') != user['id']:
        return jsonify({'error': 'Unauthorized to update this course'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    if 'name' in data:
        course['name'] = data['name']
    if 'description' in data:
        course['description'] = data['description']
    if 'credits' in data:
        course['credits'] = int(data['credits'])
    if 'department' in data:
        course['department'] = data['department']
    if 'instructor_id' in data and user['role'] == 'admin':
        course['instructor_id'] = data['instructor_id']
    
    updated = storage.update('courses', course_id, course)
    return jsonify({'course': updated, 'message': 'Course updated successfully'}), 200


@course_bp.route('/<course_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_course(user, course_id):
    """Delete a course (admin only)."""
    course = storage.get_by_id('courses', course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    # Delete associated data (assignments, attendance, etc.)
    # For now, just delete the course
    storage.delete('courses', course_id)
    
    return jsonify({'message': f'Course {course.get("code")} deleted successfully'}), 200


# ==========================================
# TIMETABLE
# ==========================================

@course_bp.route('/timetable', methods=['GET'])
@token_required
def get_timetable(user):
    """Get timetable entries with course and instructor info."""
    entries = storage.get_all('timetable')
    courses = storage.get_all('courses')
    users = storage.get_all('users')
    
    course_map = {c['id']: c for c in courses}
    user_map = {u['id']: u for u in users}
    
    # Enrich timetable entries
    for entry in entries:
        course = course_map.get(entry.get('course_id'), {})
        entry['course_name'] = course.get('name', 'Unknown Course')
        entry['course_code'] = course.get('code', '')
        
        instructor_id = course.get('instructor_id')
        if instructor_id and instructor_id in user_map:
            entry['instructor_name'] = user_map[instructor_id].get('name', '')
    
    return jsonify({'timetable': entries}), 200


# ==========================================
# FACULTY MANAGEMENT
# ==========================================

@course_bp.route('/faculty', methods=['GET'])
@token_required
def get_faculty(user):
    """Get all faculty members with optional department filter."""
    department = request.args.get('department')
    
    users = storage.get_all('users')
    faculty = [u for u in users if u.get('role') == 'faculty']
    
    # Filter by department if specified
    if department:
        faculty = [f for f in faculty if f.get('department', '').lower() == department.lower()]
    
    # Get assigned courses for each faculty
    courses = storage.get_all('courses')
    
    for fac in faculty:
        fac_courses = [c for c in courses if c.get('instructor_id') == fac.get('id')]
        fac['courses'] = [{
            'id': c['id'],
            'code': c.get('code'),
            'name': c.get('name')
        } for c in fac_courses]
        fac['course_count'] = len(fac_courses)
        
        # Remove sensitive data
        fac.pop('password_hash', None)
    
    return jsonify({'faculty': faculty}), 200


@course_bp.route('/faculty/<faculty_id>', methods=['GET'])
@token_required
def get_faculty_detail(user, faculty_id):
    """Get detailed faculty information."""
    faculty = storage.get_by_id('users', faculty_id)
    if not faculty or faculty.get('role') != 'faculty':
        return jsonify({'error': 'Faculty not found'}), 404
    
    # Get assigned courses
    courses = storage.get_all('courses')
    fac_courses = [c for c in courses if c.get('instructor_id') == faculty_id]
    
    faculty['courses'] = fac_courses
    faculty['course_count'] = len(fac_courses)
    faculty.pop('password_hash', None)
    
    return jsonify({'faculty': faculty}), 200


@course_bp.route('/departments', methods=['GET'])
@token_required
def get_departments(user):
    """Get list of all departments with faculty and course counts."""
    users = storage.get_all('users')
    courses = storage.get_all('courses')
    
    departments = {}
    
    # Count faculty per department
    for u in users:
        if u.get('role') == 'faculty':
            dept = u.get('department', 'Unassigned')
            if dept not in departments:
                departments[dept] = {'name': dept, 'faculty_count': 0, 'course_count': 0}
            departments[dept]['faculty_count'] += 1
    
    # Count courses per department
    for c in courses:
        dept = c.get('department', 'Unassigned')
        if dept not in departments:
            departments[dept] = {'name': dept, 'faculty_count': 0, 'course_count': 0}
        departments[dept]['course_count'] += 1
    
    return jsonify({'departments': list(departments.values())}), 200
