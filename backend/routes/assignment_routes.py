"""
Assignment Routes - Complete CRUD with Submissions and Grading
"""

from flask import Blueprint, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
import os, sys, uuid
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.storage_service import storage
from models.assignment import Assignment, Submission, Grade
from routes.auth_routes import token_required, role_required

assignment_bp = Blueprint('assignments', __name__)
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'zip', 'txt', 'py', 'java', 'cpp', 'c', 'js'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'uploads', 'submissions')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def ensure_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


# ==========================================
# ASSIGNMENT CRUD
# ==========================================

@assignment_bp.route('/', methods=['GET'])
@token_required
def get_assignments(user):
    """Get all assignments with submission status for students."""
    assignments = storage.get_all('assignments')
    
    if user['role'] == 'student':
        submissions = storage.get_by_field('submissions', 'student_id', user['id'])
        submitted_ids = {s['assignment_id'] for s in submissions}
        for a in assignments:
            a['submitted'] = a['id'] in submitted_ids
            # Get submission details if exists
            sub = next((s for s in submissions if s['assignment_id'] == a['id']), None)
            if sub:
                a['submission'] = sub
    
    return jsonify({'assignments': assignments}), 200


@assignment_bp.route('/<assignment_id>', methods=['GET'])
@token_required
def get_assignment(user, assignment_id):
    """Get a single assignment with submission details."""
    assignment = storage.get_by_id('assignments', assignment_id)
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    
    # Include submission status for students
    if user['role'] == 'student':
        submissions = storage.get_by_field('submissions', 'student_id', user['id'])
        sub = next((s for s in submissions if s['assignment_id'] == assignment_id), None)
        if sub:
            assignment['submission'] = sub
            assignment['submitted'] = True
        else:
            assignment['submitted'] = False
    
    return jsonify({'assignment': assignment}), 200


@assignment_bp.route('/', methods=['POST'])
@token_required
@role_required('faculty', 'admin')
def create_assignment(user):
    """Create a new assignment."""
    data = request.get_json()
    
    if not data.get('title') or not data.get('course_id'):
        return jsonify({'error': 'Title and course_id are required'}), 400
    
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


@assignment_bp.route('/<assignment_id>', methods=['PUT'])
@token_required
@role_required('faculty', 'admin')
def update_assignment(user, assignment_id):
    """Update an existing assignment."""
    assignment = storage.get_by_id('assignments', assignment_id)
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    
    # Only creator or admin can update
    if user['role'] != 'admin' and assignment.get('created_by') != user['id']:
        return jsonify({'error': 'Not authorized to update this assignment'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    updatable_fields = ['title', 'description', 'due_date', 'max_marks', 'course_id']
    for field in updatable_fields:
        if field in data:
            assignment[field] = data[field]
    
    updated = storage.update('assignments', assignment_id, assignment)
    return jsonify({'assignment': updated}), 200


@assignment_bp.route('/<assignment_id>', methods=['DELETE'])
@token_required
@role_required('faculty', 'admin')
def delete_assignment(user, assignment_id):
    """Delete an assignment."""
    assignment = storage.get_by_id('assignments', assignment_id)
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    
    # Only creator or admin can delete
    if user['role'] != 'admin' and assignment.get('created_by') != user['id']:
        return jsonify({'error': 'Not authorized to delete this assignment'}), 403
    
    # Also delete all submissions for this assignment
    submissions = storage.get_by_field('submissions', 'assignment_id', assignment_id)
    for sub in submissions:
        # Delete submission files
        if sub.get('file_path') and os.path.exists(sub['file_path']):
            try:
                os.remove(sub['file_path'])
            except:
                pass
        storage.delete('submissions', sub['id'])
    
    storage.delete('assignments', assignment_id)
    return jsonify({'message': 'Assignment deleted successfully'}), 200


# ==========================================
# SUBMISSIONS
# ==========================================

@assignment_bp.route('/<assignment_id>/submit', methods=['POST'])
@token_required
@role_required('student')
def submit_assignment(user, assignment_id):
    """Submit assignment with file upload."""
    assignment = storage.get_by_id('assignments', assignment_id)
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    
    # Check for existing submission
    existing = storage.get_by_field('submissions', 'assignment_id', assignment_id)
    student_submission = next((s for s in existing if s['student_id'] == user['id']), None)
    
    if student_submission:
        return jsonify({'error': 'You have already submitted this assignment'}), 400
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    ensure_upload_folder()
    
    # Create unique filename
    filename = secure_filename(file.filename)
    unique_filename = f"{user['id']}_{assignment_id}_{uuid.uuid4().hex[:8]}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)
    
    # Check if late submission
    is_late = False
    if assignment.get('due_date'):
        try:
            due = datetime.fromisoformat(assignment['due_date'].replace('Z', '+00:00'))
            is_late = datetime.now() > due.replace(tzinfo=None)
        except:
            pass
    
    submission = Submission(
        assignment_id=assignment_id,
        student_id=user['id'],
        file_path=file_path,
        file_name=filename,
        is_late=is_late
    )
    
    saved = storage.create('submissions', submission.to_dict())
    return jsonify({'submission': saved, 'message': 'Assignment submitted successfully'}), 201


@assignment_bp.route('/<assignment_id>/submissions', methods=['GET'])
@token_required
@role_required('faculty', 'admin')
def get_submissions(user, assignment_id):
    """Get all submissions for an assignment (faculty/admin only)."""
    assignment = storage.get_by_id('assignments', assignment_id)
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    
    submissions = storage.get_by_field('submissions', 'assignment_id', assignment_id)
    
    # Enrich with student info
    for sub in submissions:
        student = storage.get_by_id('users', sub['student_id'])
        if student:
            sub['student_name'] = student.get('name', 'Unknown')
            sub['student_email'] = student.get('email', '')
    
    return jsonify({'submissions': submissions, 'total': len(submissions)}), 200


@assignment_bp.route('/submissions/<submission_id>/download', methods=['GET'])
@token_required
def download_submission(user, submission_id):
    """Download a submission file."""
    submission = storage.get_by_id('submissions', submission_id)
    if not submission:
        return jsonify({'error': 'Submission not found'}), 404
    
    # Only the submitter, faculty, or admin can download
    if user['role'] == 'student' and submission['student_id'] != user['id']:
        return jsonify({'error': 'Not authorized'}), 403
    
    if not os.path.exists(submission['file_path']):
        return jsonify({'error': 'File not found on server'}), 404
    
    return send_file(
        submission['file_path'],
        as_attachment=True,
        download_name=submission['file_name']
    )


# ==========================================
# GRADING
# ==========================================

@assignment_bp.route('/submissions/<submission_id>/grade', methods=['POST'])
@token_required
@role_required('faculty', 'admin')
def grade_submission(user, submission_id):
    """Grade a student submission."""
    submission = storage.get_by_id('submissions', submission_id)
    if not submission:
        return jsonify({'error': 'Submission not found'}), 404
    
    data = request.get_json()
    marks = data.get('marks')
    feedback = data.get('feedback', '')
    
    if marks is None:
        return jsonify({'error': 'Marks are required'}), 400
    
    # Get assignment for max marks
    assignment = storage.get_by_id('assignments', submission['assignment_id'])
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    
    if marks < 0 or marks > assignment.get('max_marks', 100):
        return jsonify({'error': f'Marks must be between 0 and {assignment.get("max_marks", 100)}'}), 400
    
    # Update submission
    submission['marks'] = marks
    submission['feedback'] = feedback
    submission['graded_at'] = datetime.now().isoformat()
    submission['graded_by'] = user['id']
    
    storage.update('submissions', submission_id, submission)
    
    # Create/update grade record
    grade = Grade(
        student_id=submission['student_id'],
        course_id=assignment.get('course_id', ''),
        assignment_id=submission['assignment_id'],
        marks=marks,
        max_marks=assignment.get('max_marks', 100)
    )
    
    # Check if grade exists for this assignment+student
    existing_grades = storage.get_by_field('grades', 'assignment_id', submission['assignment_id'])
    existing = next((g for g in existing_grades if g['student_id'] == submission['student_id']), None)
    
    if existing:
        storage.update('grades', existing['id'], grade.to_dict())
    else:
        storage.create('grades', grade.to_dict())
    
    return jsonify({
        'message': 'Submission graded successfully',
        'submission': submission,
        'grade_letter': grade.grade_letter
    }), 200


@assignment_bp.route('/grades', methods=['GET'])
@token_required
def get_grades(user):
    """Get grades for the current user or all grades for faculty."""
    if user['role'] == 'student':
        grades = storage.get_by_field('grades', 'student_id', user['id'])
    else:
        grades = storage.get_all('grades')
    
    # Enrich with assignment and course info
    for grade in grades:
        assignment = storage.get_by_id('assignments', grade.get('assignment_id', ''))
        if assignment:
            grade['assignment_title'] = assignment.get('title', '')
        
        course = storage.get_by_id('courses', grade.get('course_id', ''))
        if course:
            grade['course_name'] = course.get('name', '')
    
    return jsonify({'grades': grades}), 200
