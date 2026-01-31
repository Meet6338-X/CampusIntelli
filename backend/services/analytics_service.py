"""
Analytics Service - Data Aggregation for Charts and Reports
"""

from datetime import datetime, timedelta
from collections import defaultdict
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.storage_service import storage


class AnalyticsService:
    """Service for generating analytics and aggregate data."""
    
    @staticmethod
    def get_grade_distribution(course_id=None):
        """
        Get grade distribution (A+, A, B, C, D, F counts).
        Returns data suitable for bar/pie charts.
        """
        grades = storage.get_all('grades')
        
        if course_id:
            grades = [g for g in grades if g.get('course_id') == course_id]
        
        distribution = defaultdict(int)
        grade_order = ['A+', 'A', 'B', 'C', 'D', 'F']
        
        for g in grades:
            letter = g.get('grade_letter', 'N/A')
            distribution[letter] += 1
        
        # Ensure all grades are present
        result = {grade: distribution.get(grade, 0) for grade in grade_order}
        
        return {
            'labels': list(result.keys()),
            'data': list(result.values()),
            'total_students': len(grades)
        }
    
    @staticmethod
    def get_attendance_trends(course_id=None, days=30):
        """
        Get attendance trends over time.
        Returns data suitable for line charts.
        """
        records = storage.get_all('attendance')
        
        if course_id:
            records = [r for r in records if r.get('course_id') == course_id]
        
        # Filter by date range
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        records = [r for r in records if r.get('date', '') >= cutoff[:10]]
        
        # Group by date
        by_date = defaultdict(lambda: {'present': 0, 'total': 0})
        
        for r in records:
            date = r.get('date', '')[:10]
            by_date[date]['total'] += 1
            if r.get('present', False):
                by_date[date]['present'] += 1
        
        # Sort by date
        sorted_dates = sorted(by_date.keys())
        
        attendance_rates = []
        for date in sorted_dates:
            total = by_date[date]['total']
            present = by_date[date]['present']
            rate = (present / total * 100) if total > 0 else 0
            attendance_rates.append(round(rate, 1))
        
        return {
            'labels': sorted_dates,
            'data': attendance_rates,
            'period_days': days
        }
    
    @staticmethod
    def get_class_performance(course_id):
        """
        Get class performance metrics for a course.
        """
        grades = storage.get_by_field('grades', 'course_id', course_id)
        
        if not grades:
            return {
                'average': 0,
                'highest': 0,
                'lowest': 0,
                'passing_rate': 0,
                'total_students': 0
            }
        
        # Calculate percentages
        percentages = []
        for g in grades:
            max_marks = g.get('max_marks', 100)
            marks = g.get('marks', 0)
            if max_marks > 0:
                percentages.append((marks / max_marks) * 100)
        
        if not percentages:
            return {
                'average': 0,
                'highest': 0,
                'lowest': 0,
                'passing_rate': 0,
                'total_students': 0
            }
        
        avg = sum(percentages) / len(percentages)
        passing = len([p for p in percentages if p >= 50])
        
        return {
            'average': round(avg, 1),
            'highest': round(max(percentages), 1),
            'lowest': round(min(percentages), 1),
            'passing_rate': round((passing / len(percentages)) * 100, 1),
            'total_students': len(grades)
        }
    
    @staticmethod
    def get_student_performance(student_id):
        """
        Get performance metrics for a specific student.
        """
        grades = storage.get_by_field('grades', 'student_id', student_id)
        attendance = storage.get_by_field('attendance', 'student_id', student_id)
        
        # Calculate GPA equivalent
        grade_points = {'A+': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6, 'F': 0}
        total_points = 0
        total_credits = 0
        
        course_grades = []
        for g in grades:
            letter = g.get('grade_letter', 'F')
            points = grade_points.get(letter, 0)
            total_points += points
            total_credits += 1
            
            course = storage.get_by_id('courses', g.get('course_id', ''))
            course_grades.append({
                'course_name': course.get('name', 'Unknown') if course else 'Unknown',
                'grade': letter,
                'marks': g.get('marks', 0),
                'max_marks': g.get('max_marks', 100)
            })
        
        cgpa = (total_points / total_credits) if total_credits > 0 else 0
        
        # Attendance rate
        present_count = len([a for a in attendance if a.get('present', False)])
        total_attendance = len(attendance)
        attendance_rate = (present_count / total_attendance * 100) if total_attendance > 0 else 0
        
        return {
            'cgpa': round(cgpa, 2),
            'attendance_rate': round(attendance_rate, 1),
            'courses_completed': total_credits,
            'course_grades': course_grades
        }
    
    @staticmethod
    def get_dashboard_stats(user_id, role):
        """
        Get dashboard statistics for the user.
        """
        stats = {}
        
        if role == 'student':
            # Student stats
            grades = storage.get_by_field('grades', 'student_id', user_id)
            attendance = storage.get_by_field('attendance', 'student_id', user_id)
            assignments = storage.get_all('assignments')
            submissions = storage.get_by_field('submissions', 'student_id', user_id)
            
            submitted_ids = {s['assignment_id'] for s in submissions}
            pending = len([a for a in assignments if a['id'] not in submitted_ids])
            
            present = len([a for a in attendance if a.get('present', False)])
            total = len(attendance)
            
            stats = {
                'courses_enrolled': len(set(g.get('course_id') for g in grades)) or len(storage.get_all('courses')),
                'pending_assignments': pending,
                'attendance_rate': round((present/total*100) if total > 0 else 0, 1),
                'upcoming_exams': 0  # Placeholder
            }
        
        elif role == 'faculty':
            # Faculty stats
            courses = storage.get_by_field('courses', 'instructor_id', user_id)
            assignments = storage.get_all('assignments')
            faculty_assignments = [a for a in assignments if a.get('created_by') == user_id]
            submissions = storage.get_all('submissions')
            
            # Ungraded submissions
            ungraded = len([s for s in submissions if s.get('marks') is None])
            
            stats = {
                'courses_teaching': len(courses),
                'total_assignments': len(faculty_assignments),
                'pending_grading': ungraded,
                'total_students': len(set(s.get('student_id') for s in submissions))
            }
        
        else:  # admin
            stats = {
                'total_users': len(storage.get_all('users')),
                'total_courses': len(storage.get_all('courses')),
                'total_assignments': len(storage.get_all('assignments')),
                'active_bookings': len([b for b in storage.get_all('bookings') if b.get('status') == 'confirmed'])
            }
        
        return stats


# Singleton instance
analytics = AnalyticsService()
