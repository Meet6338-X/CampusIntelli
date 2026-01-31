"""
Calendar and Events Routes - Admin ERP Management
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.storage_service import storage
from models.calendar import Event, AcademicCalendar, TimetableSlot
from routes.auth_routes import token_required, role_required

calendar_bp = Blueprint('calendar', __name__)


# ==========================================
# EVENTS MANAGEMENT (Admin can edit past events)
# ==========================================

@calendar_bp.route('/events', methods=['GET'])
@token_required
def get_events(user):
    """Get all events with optional filters."""
    event_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    include_past = request.args.get('include_past', 'true').lower() == 'true'
    
    events = storage.get_all('events')
    
    # Filter by type
    if event_type:
        events = [e for e in events if e.get('event_type') == event_type]
    
    # Filter by date range
    if start_date:
        events = [e for e in events if e.get('start_date', '') >= start_date]
    if end_date:
        events = [e for e in events if e.get('start_date', '') <= end_date]
    
    # Filter past events for non-admin
    if not include_past and user['role'] != 'admin':
        today = datetime.now().strftime('%Y-%m-%d')
        events = [e for e in events if e.get('end_date', e.get('start_date', '')) >= today]
    
    # Enrich with organizer name
    users = storage.get_all('users')
    user_map = {u['id']: u.get('name', 'Unknown') for u in users}
    for event in events:
        event['organizer_name'] = user_map.get(event.get('organizer_id'), 'Unknown')
    
    # Sort by date
    events.sort(key=lambda x: x.get('start_date', ''), reverse=True)
    
    return jsonify({'events': events, 'total': len(events)}), 200


@calendar_bp.route('/events/<event_id>', methods=['GET'])
@token_required
def get_event(user, event_id):
    """Get single event."""
    event = storage.get_by_id('events', event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({'event': event}), 200


@calendar_bp.route('/events', methods=['POST'])
@token_required
@role_required('admin', 'faculty')
def create_event(user):
    """Create a new event."""
    data = request.get_json()
    
    if not data.get('title') or not data.get('start_date'):
        return jsonify({'error': 'Title and start_date are required'}), 400
    
    event = Event(
        title=data.get('title'),
        description=data.get('description', ''),
        event_type=data.get('event_type', 'general'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        location=data.get('location', ''),
        organizer_id=data.get('organizer_id', user['id']),
        department=data.get('department', user.get('department', '')),
        is_public=data.get('is_public', True),
        is_holiday=data.get('is_holiday', False),
        created_by=user['id']
    )
    
    saved = storage.create('events', event.to_dict())
    return jsonify({'event': saved, 'message': 'Event created successfully'}), 201


@calendar_bp.route('/events/<event_id>', methods=['PUT'])
@token_required
@role_required('admin', 'faculty')
def update_event(user, event_id):
    """Update event - Admin can edit ANY event including past ones."""
    event = storage.get_by_id('events', event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    # Only admin can edit others' events or past events
    is_past = event.get('end_date', event.get('start_date', '')) < datetime.now().strftime('%Y-%m-%d')
    is_owner = event.get('created_by') == user['id'] or event.get('organizer_id') == user['id']
    
    if user['role'] != 'admin' and (is_past or not is_owner):
        return jsonify({'error': 'Not authorized to edit this event'}), 403
    
    data = request.get_json()
    
    # Update all fields
    updatable = ['title', 'description', 'event_type', 'start_date', 'end_date',
                 'start_time', 'end_time', 'location', 'organizer_id', 'department',
                 'is_public', 'is_holiday']
    
    for field in updatable:
        if field in data:
            event[field] = data[field]
    
    event['updated_at'] = datetime.now().isoformat()
    event['updated_by'] = user['id']
    
    updated = storage.update('events', event_id, event)
    return jsonify({'event': updated, 'message': 'Event updated successfully'}), 200


@calendar_bp.route('/events/<event_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_event(user, event_id):
    """Delete event - Admin only."""
    event = storage.get_by_id('events', event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    storage.delete('events', event_id)
    return jsonify({'message': 'Event deleted successfully'}), 200


# ==========================================
# ACADEMIC CALENDAR MANAGEMENT
# ==========================================

@calendar_bp.route('/academic', methods=['GET'])
@token_required
def get_academic_calendar(user):
    """Get academic calendar items."""
    academic_year = request.args.get('academic_year')
    semester = request.args.get('semester')
    item_type = request.args.get('type')
    
    items = storage.get_all('academic_calendar')
    
    if academic_year:
        items = [i for i in items if i.get('academic_year') == academic_year]
    if semester:
        items = [i for i in items if i.get('semester') == semester]
    if item_type:
        items = [i for i in items if i.get('item_type') == item_type]
    
    # Sort by date
    items.sort(key=lambda x: x.get('start_date', ''))
    
    return jsonify({'calendar': items, 'total': len(items)}), 200


@calendar_bp.route('/academic', methods=['POST'])
@token_required
@role_required('admin')
def create_academic_item(user):
    """Create academic calendar item - Admin only."""
    data = request.get_json()
    
    required = ['academic_year', 'title', 'start_date', 'item_type']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    item = AcademicCalendar(
        academic_year=data.get('academic_year'),
        semester=data.get('semester', ''),
        item_type=data.get('item_type'),
        title=data.get('title'),
        description=data.get('description', ''),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        created_by=user['id']
    )
    
    saved = storage.create('academic_calendar', item.to_dict())
    return jsonify({'item': saved, 'message': 'Academic calendar item created'}), 201


@calendar_bp.route('/academic/<item_id>', methods=['PUT'])
@token_required
@role_required('admin')
def update_academic_item(user, item_id):
    """Update academic calendar item - Admin only."""
    item = storage.get_by_id('academic_calendar', item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    data = request.get_json()
    
    updatable = ['academic_year', 'semester', 'item_type', 'title',
                 'description', 'start_date', 'end_date', 'is_active']
    
    for field in updatable:
        if field in data:
            item[field] = data[field]
    
    updated = storage.update('academic_calendar', item_id, item)
    return jsonify({'item': updated, 'message': 'Academic calendar updated'}), 200


@calendar_bp.route('/academic/<item_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_academic_item(user, item_id):
    """Delete academic calendar item - Admin only."""
    if not storage.get_by_id('academic_calendar', item_id):
        return jsonify({'error': 'Item not found'}), 404
    
    storage.delete('academic_calendar', item_id)
    return jsonify({'message': 'Academic calendar item deleted'}), 200


# ==========================================
# TIMETABLE MANAGEMENT (Full CRUD)
# ==========================================

@calendar_bp.route('/timetable', methods=['GET'])
@token_required
def get_timetable(user):
    """Get timetable with filters."""
    course_id = request.args.get('course_id')
    day = request.args.get('day', type=int)
    semester = request.args.get('semester')
    section = request.args.get('section')
    
    slots = storage.get_all('timetable_slots')
    
    if course_id:
        slots = [s for s in slots if s.get('course_id') == course_id]
    if day is not None:
        slots = [s for s in slots if s.get('day_of_week') == day]
    if semester:
        slots = [s for s in slots if s.get('semester') == semester]
    if section:
        slots = [s for s in slots if s.get('section') == section]
    
    # Enrich with course and instructor info
    courses = storage.get_all('courses')
    users = storage.get_all('users')
    course_map = {c['id']: c for c in courses}
    user_map = {u['id']: u for u in users}
    
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for slot in slots:
        course = course_map.get(slot.get('course_id'), {})
        slot['course_name'] = course.get('name', 'Unknown')
        slot['course_code'] = course.get('code', '')
        slot['day_name'] = day_names[slot.get('day_of_week', 0)]
        
        instructor = user_map.get(slot.get('instructor_id'), {})
        slot['instructor_name'] = instructor.get('name', 'TBA')
    
    # Sort by day and time
    slots.sort(key=lambda x: (x.get('day_of_week', 0), x.get('start_time', '')))
    
    return jsonify({'timetable': slots, 'total': len(slots)}), 200


@calendar_bp.route('/timetable', methods=['POST'])
@token_required
@role_required('admin', 'faculty')
def create_timetable_slot(user):
    """Create a timetable slot."""
    data = request.get_json()
    
    required = ['course_id', 'day_of_week', 'start_time', 'end_time']
    for field in required:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Verify course exists
    course = storage.get_by_id('courses', data['course_id'])
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    # Check for time conflicts
    existing = storage.get_all('timetable_slots')
    for slot in existing:
        if (slot.get('day_of_week') == data['day_of_week'] and
            slot.get('room') == data.get('room') and
            slot.get('is_active', True)):
            # Check time overlap
            if not (data['end_time'] <= slot.get('start_time', '') or 
                    data['start_time'] >= slot.get('end_time', '')):
                return jsonify({'error': f'Time conflict with {slot.get("course_id")} in room {slot.get("room")}'}), 400
    
    slot = TimetableSlot(
        course_id=data['course_id'],
        day_of_week=int(data['day_of_week']),
        start_time=data['start_time'],
        end_time=data['end_time'],
        room=data.get('room', ''),
        instructor_id=data.get('instructor_id', course.get('instructor_id', '')),
        slot_type=data.get('slot_type', 'lecture'),
        section=data.get('section', ''),
        semester=data.get('semester', '')
    )
    
    saved = storage.create('timetable_slots', slot.to_dict())
    return jsonify({'slot': saved, 'message': 'Timetable slot created'}), 201


@calendar_bp.route('/timetable/<slot_id>', methods=['PUT'])
@token_required
@role_required('admin', 'faculty')
def update_timetable_slot(user, slot_id):
    """Update timetable slot."""
    slot = storage.get_by_id('timetable_slots', slot_id)
    if not slot:
        return jsonify({'error': 'Slot not found'}), 404
    
    # Only admin or course instructor can update
    course = storage.get_by_id('courses', slot.get('course_id', ''))
    if user['role'] != 'admin' and (not course or course.get('instructor_id') != user['id']):
        return jsonify({'error': 'Not authorized'}), 403
    
    data = request.get_json()
    
    updatable = ['day_of_week', 'start_time', 'end_time', 'room',
                 'instructor_id', 'slot_type', 'section', 'semester', 'is_active']
    
    for field in updatable:
        if field in data:
            slot[field] = data[field]
    
    updated = storage.update('timetable_slots', slot_id, slot)
    return jsonify({'slot': updated, 'message': 'Timetable slot updated'}), 200


@calendar_bp.route('/timetable/<slot_id>', methods=['DELETE'])
@token_required
@role_required('admin')
def delete_timetable_slot(user, slot_id):
    """Delete timetable slot - Admin only."""
    if not storage.get_by_id('timetable_slots', slot_id):
        return jsonify({'error': 'Slot not found'}), 404
    
    storage.delete('timetable_slots', slot_id)
    return jsonify({'message': 'Timetable slot deleted'}), 200


# ==========================================
# SUBJECT DATE MANAGEMENT
# ==========================================

@calendar_bp.route('/subjects', methods=['GET'])
@token_required
def get_subjects_schedule(user):
    """Get all subjects with their scheduled dates."""
    courses = storage.get_all('courses')
    timetable = storage.get_all('timetable_slots')
    assignments = storage.get_all('assignments')
    
    subjects = []
    for course in courses:
        course_slots = [s for s in timetable if s.get('course_id') == course['id']]
        course_assignments = [a for a in assignments if a.get('course_id') == course['id']]
        
        subjects.append({
            'id': course['id'],
            'code': course.get('code'),
            'name': course.get('name'),
            'department': course.get('department'),
            'schedule': course_slots,
            'assignments': [{
                'id': a['id'],
                'title': a.get('title'),
                'due_date': a.get('due_date')
            } for a in course_assignments],
            'class_count': len(course_slots)
        })
    
    return jsonify({'subjects': subjects}), 200


@calendar_bp.route('/subjects/<course_id>/dates', methods=['PUT'])
@token_required
@role_required('admin')
def update_subject_dates(user, course_id):
    """Bulk update subject dates (assignments, timetable) - Admin only."""
    course = storage.get_by_id('courses', course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    data = request.get_json()
    updated_items = {'assignments': 0, 'timetable': 0}
    
    # Update assignment due dates
    if 'assignments' in data:
        for assignment_update in data['assignments']:
            assignment = storage.get_by_id('assignments', assignment_update.get('id'))
            if assignment and assignment.get('course_id') == course_id:
                if 'due_date' in assignment_update:
                    assignment['due_date'] = assignment_update['due_date']
                    storage.update('assignments', assignment['id'], assignment)
                    updated_items['assignments'] += 1
    
    # Update timetable slots
    if 'timetable' in data:
        for slot_update in data['timetable']:
            slot = storage.get_by_id('timetable_slots', slot_update.get('id'))
            if slot and slot.get('course_id') == course_id:
                for field in ['day_of_week', 'start_time', 'end_time', 'room']:
                    if field in slot_update:
                        slot[field] = slot_update[field]
                storage.update('timetable_slots', slot['id'], slot)
                updated_items['timetable'] += 1
    
    return jsonify({
        'message': f'Updated {updated_items["assignments"]} assignments, {updated_items["timetable"]} timetable slots',
        'updated': updated_items
    }), 200
