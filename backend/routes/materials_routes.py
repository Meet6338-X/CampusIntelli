"""
Materials Routes - Lecture Materials CRUD
"""

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os, sys, uuid
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.storage_service import storage
from models.materials import Material
from routes.auth_routes import token_required, role_required

materials_bp = Blueprint('materials', __name__)
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt', 'zip', 'mp4', 'mp3', 'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'uploads', 'materials')
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_type(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    type_map = {
        'pdf': 'document',
        'doc': 'document', 'docx': 'document',
        'ppt': 'presentation', 'pptx': 'presentation',
        'xls': 'spreadsheet', 'xlsx': 'spreadsheet',
        'txt': 'text',
        'zip': 'archive',
        'mp4': 'video', 'mp3': 'audio',
        'png': 'image', 'jpg': 'image', 'jpeg': 'image'
    }
    return type_map.get(ext, 'other')


def ensure_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


@materials_bp.route('/', methods=['GET'])
@token_required
def get_materials(user):
    """Get all materials with optional course filter."""
    course_id = request.args.get('course_id')
    category = request.args.get('category')
    
    if course_id:
        materials = storage.get_by_field('materials', 'course_id', course_id)
    else:
        materials = storage.get_all('materials')
    
    # Filter by category if provided
    if category:
        materials = [m for m in materials if m.get('category') == category]
    
    # Filter hidden materials for students
    if user['role'] == 'student':
        materials = [m for m in materials if m.get('is_visible', True)]
    
    # Enrich with uploader info and course name
    for material in materials:
        uploader = storage.get_by_id('users', material.get('uploaded_by', ''))
        if uploader:
            material['uploader_name'] = uploader.get('name', 'Unknown')
        
        course = storage.get_by_id('courses', material.get('course_id', ''))
        if course:
            material['course_name'] = course.get('name', '')
    
    return jsonify({'materials': materials, 'total': len(materials)}), 200


@materials_bp.route('/<material_id>', methods=['GET'])
@token_required
def get_material(user, material_id):
    """Get a single material."""
    material = storage.get_by_id('materials', material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404
    
    # Check visibility for students
    if user['role'] == 'student' and not material.get('is_visible', True):
        return jsonify({'error': 'Material not available'}), 403
    
    return jsonify({'material': material}), 200


@materials_bp.route('/', methods=['POST'])
@token_required
@role_required('faculty', 'admin')
def upload_material(user):
    """Upload a new material."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    # Get form data
    title = request.form.get('title', file.filename)
    description = request.form.get('description', '')
    course_id = request.form.get('course_id', '')
    category = request.form.get('category', 'lecture')
    
    if not course_id:
        return jsonify({'error': 'Course ID is required'}), 400
    
    # Verify course exists
    course = storage.get_by_id('courses', course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    ensure_upload_folder()
    
    # Create unique filename
    filename = secure_filename(file.filename)
    unique_filename = f"{course_id}_{uuid.uuid4().hex[:8]}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    material = Material(
        course_id=course_id,
        title=title,
        description=description,
        file_path=file_path,
        file_name=filename,
        file_type=get_file_type(filename),
        file_size=file_size,
        uploaded_by=user['id'],
        category=category
    )
    
    saved = storage.create('materials', material.to_dict())
    return jsonify({'material': saved, 'message': 'Material uploaded successfully'}), 201


@materials_bp.route('/<material_id>', methods=['PUT'])
@token_required
@role_required('faculty', 'admin')
def update_material(user, material_id):
    """Update material metadata."""
    material = storage.get_by_id('materials', material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404
    
    # Only uploader or admin can update
    if user['role'] != 'admin' and material.get('uploaded_by') != user['id']:
        return jsonify({'error': 'Not authorized'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    updatable_fields = ['title', 'description', 'category', 'is_visible', 'course_id']
    for field in updatable_fields:
        if field in data:
            material[field] = data[field]
    
    updated = storage.update('materials', material_id, material)
    return jsonify({'material': updated}), 200


@materials_bp.route('/<material_id>', methods=['DELETE'])
@token_required
@role_required('faculty', 'admin')
def delete_material(user, material_id):
    """Delete a material."""
    material = storage.get_by_id('materials', material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404
    
    # Only uploader or admin can delete
    if user['role'] != 'admin' and material.get('uploaded_by') != user['id']:
        return jsonify({'error': 'Not authorized'}), 403
    
    # Delete file
    if material.get('file_path') and os.path.exists(material['file_path']):
        try:
            os.remove(material['file_path'])
        except:
            pass
    
    storage.delete('materials', material_id)
    return jsonify({'message': 'Material deleted successfully'}), 200


@materials_bp.route('/<material_id>/download', methods=['GET'])
@token_required
def download_material(user, material_id):
    """Download a material file."""
    material = storage.get_by_id('materials', material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404
    
    # Check visibility for students
    if user['role'] == 'student' and not material.get('is_visible', True):
        return jsonify({'error': 'Material not available'}), 403
    
    if not os.path.exists(material['file_path']):
        return jsonify({'error': 'File not found on server'}), 404
    
    return send_file(
        material['file_path'],
        as_attachment=True,
        download_name=material['file_name']
    )
