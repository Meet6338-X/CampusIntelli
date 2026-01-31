"""
CampusIntelli Portal - Backend Application
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import routes
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.course_routes import course_bp
from routes.assignment_routes import assignment_bp
from routes.booking_routes import booking_bp
from routes.attendance_routes import attendance_bp
from routes.announcement_routes import announcement_bp
from routes.materials_routes import materials_bp
from routes.analytics_routes import analytics_bp
from routes.admin_routes import admin_bp
from routes.calendar_routes import calendar_bp
from services.auth_service import init_sample_data

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'campusintelli-dev-secret-key-2026')
app.config['DATA_DIR'] = os.path.join(os.path.dirname(__file__), '..', 'data')
app.config['UPLOAD_DIR'] = os.path.join(os.path.dirname(__file__), '..', 'uploads')

# Ensure directories exist
os.makedirs(app.config['DATA_DIR'], exist_ok=True)
os.makedirs(app.config['UPLOAD_DIR'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_DIR'], 'submissions'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_DIR'], 'materials'), exist_ok=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(course_bp, url_prefix='/api/courses')
app.register_blueprint(assignment_bp, url_prefix='/api/assignments')
app.register_blueprint(booking_bp, url_prefix='/api/bookings')
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
app.register_blueprint(announcement_bp, url_prefix='/api/announcements')
app.register_blueprint(materials_bp, url_prefix='/api/materials')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(calendar_bp, url_prefix='/api/calendar')

# Serve frontend
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# Health check
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'CampusIntelli API',
        'version': '1.0.0'
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize sample data
    init_sample_data()
    
    print("CampusIntelli Portal Starting...")
    print("Server: http://localhost:5000")
    print("API Health: http://localhost:5000/api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)
