"""
Attendance Routes
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from io import BytesIO
import base64, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import qrcode
from services.storage_service import storage
from models.attendance import Attendance, QRCode
from routes.auth_routes import token_required, role_required

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/generate-qr', methods=['POST'])
@token_required
@role_required('faculty')
def generate_qr(user):
    data = request.get_json()
    course_id = data.get('course_id')
    
    if not course_id:
        return jsonify({'error': 'course_id required'}), 400
    
    qr_code = QRCode(course_id=course_id, faculty_id=user['id'])
    qr_data = f"{qr_code.code_data}|{course_id}|{qr_code.lecture_id}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    saved = storage.create('qrcodes', qr_code.to_dict())
    return jsonify({
        'qr_code': saved,
        'qr_image': f"data:image/png;base64,{qr_image}",
        'expires_in_seconds': 300
    }), 201


@attendance_bp.route('/mark', methods=['POST'])
@token_required
@role_required('student')
def mark_attendance(user):
    data = request.get_json()
    qr_data = data.get('qr_data', '')
    
    parts = qr_data.split('|')
    if len(parts) < 3:
        return jsonify({'error': 'Invalid QR code'}), 400
    
    code_data, course_id, lecture_id = parts[0], parts[1], parts[2]
    
    qr_codes = storage.get_by_field('qrcodes', 'code_data', code_data)
    if not qr_codes:
        return jsonify({'error': 'QR code not found'}), 404
    
    qr = QRCode.from_dict(qr_codes[0])
    is_valid, error = qr.validate()
    if not is_valid:
        return jsonify({'error': error}), 400
    
    today = datetime.now().strftime('%Y-%m-%d')
    existing = storage.query('attendance', {
        'course_id': course_id, 'student_id': user['id'],
        'date': today, 'lecture_id': lecture_id
    })
    if existing:
        return jsonify({'error': 'Already marked'}), 409
    
    attendance = Attendance(
        course_id=course_id, student_id=user['id'],
        lecture_id=lecture_id, is_present=True
    )
    saved = storage.create('attendance', attendance.to_dict())
    return jsonify({'attendance': saved, 'message': 'Marked!'}), 201


@attendance_bp.route('/', methods=['GET'])
@token_required
def get_attendance(user):
    if user['role'] == 'student':
        records = storage.get_by_field('attendance', 'student_id', user['id'])
    else:
        records = storage.get_all('attendance')
    return jsonify({'attendance': records}), 200


@attendance_bp.route('/summary', methods=['GET'])
@token_required
def get_summary(user):
    if user['role'] == 'student':
        records = storage.get_by_field('attendance', 'student_id', user['id'])
    else:
        records = storage.get_all('attendance')
    
    summary = {}
    for r in records:
        cid = r.get('course_id')
        if cid not in summary:
            summary[cid] = {'present': 0, 'total': 0}
        summary[cid]['total'] += 1
        if r.get('is_present'):
            summary[cid]['present'] += 1
    
    return jsonify({'summary': summary}), 200
