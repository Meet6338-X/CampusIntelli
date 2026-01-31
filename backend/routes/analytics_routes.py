"""
Analytics Routes - Dashboard Stats and Performance Data
"""

from flask import Blueprint, request, jsonify
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.analytics_service import analytics
from routes.auth_routes import token_required, role_required

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard_stats(user):
    """Get dashboard statistics for the current user."""
    stats = analytics.get_dashboard_stats(user['id'], user['role'])
    return jsonify({'stats': stats}), 200


@analytics_bp.route('/grades/distribution', methods=['GET'])
@token_required
@role_required('faculty', 'admin')
def get_grade_distribution(user):
    """Get grade distribution for charts."""
    course_id = request.args.get('course_id')
    distribution = analytics.get_grade_distribution(course_id)
    return jsonify(distribution), 200


@analytics_bp.route('/attendance/trends', methods=['GET'])
@token_required
def get_attendance_trends(user):
    """Get attendance trends over time."""
    course_id = request.args.get('course_id')
    days = request.args.get('days', 30, type=int)
    trends = analytics.get_attendance_trends(course_id, days)
    return jsonify(trends), 200


@analytics_bp.route('/performance/class/<course_id>', methods=['GET'])
@token_required
@role_required('faculty', 'admin')
def get_class_performance(user, course_id):
    """Get class performance metrics for a course."""
    performance = analytics.get_class_performance(course_id)
    return jsonify({'performance': performance}), 200


@analytics_bp.route('/performance/student', methods=['GET'])
@token_required
def get_student_performance(user):
    """Get performance metrics for the current student or specified student."""
    student_id = request.args.get('student_id', user['id'])
    
    # Students can only view their own performance
    if user['role'] == 'student' and student_id != user['id']:
        return jsonify({'error': 'Not authorized'}), 403
    
    performance = analytics.get_student_performance(student_id)
    return jsonify({'performance': performance}), 200


@analytics_bp.route('/summary', methods=['GET'])
@token_required
@role_required('admin')
def get_institution_summary(user):
    """Get institution-wide summary (admin only)."""
    from services.storage_service import storage
    
    users = storage.get_all('users')
    courses = storage.get_all('courses')
    assignments = storage.get_all('assignments')
    submissions = storage.get_all('submissions')
    attendance = storage.get_all('attendance')
    
    # Count by role
    role_counts = {}
    for u in users:
        role = u.get('role', 'unknown')
        role_counts[role] = role_counts.get(role, 0) + 1
    
    # Submissions stats
    graded = len([s for s in submissions if s.get('marks') is not None])
    
    # Attendance stats
    present = len([a for a in attendance if a.get('present', False)])
    
    summary = {
        'users': {
            'total': len(users),
            'by_role': role_counts
        },
        'academics': {
            'total_courses': len(courses),
            'total_assignments': len(assignments),
            'total_submissions': len(submissions),
            'graded_submissions': graded
        },
        'attendance': {
            'total_records': len(attendance),
            'present_count': present,
            'average_rate': round((present/len(attendance)*100) if attendance else 0, 1)
        }
    }
    
    return jsonify({'summary': summary}), 200
