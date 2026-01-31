"""
Tests for Assignment Routes
"""

import pytest
import io


class TestAssignmentRoutes:
    """Test assignment CRUD and submissions."""
    
    def test_get_assignments(self, client, auth_headers_student):
        """Test getting all assignments."""
        response = client.get('/api/assignments/', headers=auth_headers_student)
        assert response.status_code == 200
        data = response.get_json()
        assert 'assignments' in data
    
    def test_create_assignment_as_faculty(self, client, auth_headers_faculty, sample_course, temp_data_dir):
        """Test creating assignment as faculty."""
        from services.storage_service import storage
        storage.create('courses', sample_course)
        
        response = client.post('/api/assignments/', 
            headers={'Content-Type': 'application/json', **auth_headers_faculty},
            json={
                'course_id': sample_course['id'],
                'title': 'New Assignment',
                'description': 'Test description',
                'due_date': '2026-02-20T23:59:00',
                'max_marks': 100
            })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['assignment']['title'] == 'New Assignment'
    
    def test_create_assignment_as_student_fails(self, client, auth_headers_student):
        """Test that students cannot create assignments."""
        response = client.post('/api/assignments/',
            headers={'Content-Type': 'application/json', **auth_headers_student},
            json={
                'course_id': 'course-001',
                'title': 'Unauthorized Assignment'
            })
        
        assert response.status_code == 403
    
    def test_update_assignment(self, client, auth_headers_faculty, sample_assignment, temp_data_dir):
        """Test updating an assignment."""
        from services.storage_service import storage
        storage.create('assignments', sample_assignment)
        
        response = client.put(f'/api/assignments/{sample_assignment["id"]}',
            headers={'Content-Type': 'application/json', **auth_headers_faculty},
            json={'title': 'Updated Title'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['assignment']['title'] == 'Updated Title'
    
    def test_delete_assignment(self, client, auth_headers_faculty, sample_assignment, temp_data_dir):
        """Test deleting an assignment."""
        from services.storage_service import storage
        storage.create('assignments', sample_assignment)
        
        response = client.delete(f'/api/assignments/{sample_assignment["id"]}',
            headers=auth_headers_faculty)
        
        assert response.status_code == 200
    
    def test_submit_assignment(self, client, auth_headers_student, sample_assignment, temp_data_dir):
        """Test submitting an assignment file."""
        from services.storage_service import storage
        storage.create('assignments', sample_assignment)
        
        # Create a test file
        file_content = b'Test assignment submission content'
        data = {
            'file': (io.BytesIO(file_content), 'submission.pdf')
        }
        
        response = client.post(f'/api/assignments/{sample_assignment["id"]}/submit',
            headers=auth_headers_student,
            data=data,
            content_type='multipart/form-data')
        
        assert response.status_code == 201
        result = response.get_json()
        assert 'submission' in result


class TestGrading:
    """Test grading functionality."""
    
    def test_grade_submission(self, client, auth_headers_faculty, sample_assignment, temp_data_dir):
        """Test grading a submission."""
        from services.storage_service import storage
        
        storage.create('assignments', sample_assignment)
        
        submission = {
            'id': 'sub-001',
            'assignment_id': sample_assignment['id'],
            'student_id': 'test-student-001',
            'file_path': '/tmp/test.pdf',
            'file_name': 'test.pdf'
        }
        storage.create('submissions', submission)
        
        response = client.post('/api/assignments/submissions/sub-001/grade',
            headers={'Content-Type': 'application/json', **auth_headers_faculty},
            json={'marks': 85, 'feedback': 'Good work!'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['submission']['marks'] == 85
