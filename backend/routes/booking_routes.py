"""
Booking Routes
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.storage_service import storage
from models.booking import Room, Booking
from routes.auth_routes import token_required, role_required

booking_bp = Blueprint('bookings', __name__)


@booking_bp.route('/rooms', methods=['GET'])
@token_required
def get_rooms(user):
    rooms = storage.get_all('rooms')
    return jsonify({'rooms': rooms}), 200


@booking_bp.route('/rooms/available', methods=['GET'])
@token_required
def get_available_rooms(user):
    date = request.args.get('date')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    if not all([date, start_time, end_time]):
        return jsonify({'error': 'date, start_time, end_time required'}), 400
    
    rooms = storage.get_all('rooms')
    bookings = storage.get_by_field('bookings', 'date', date)
    
    booked_ids = set()
    for b in bookings:
        if b.get('status') == 'cancelled':
            continue
        b_start, b_end = b.get('start_time', ''), b.get('end_time', '')
        if not (end_time <= b_start or start_time >= b_end):
            booked_ids.add(b.get('room_id'))
    
    available = [r for r in rooms if r['id'] not in booked_ids and r.get('is_available', True)]
    return jsonify({'rooms': available}), 200


@booking_bp.route('/', methods=['GET'])
@token_required
def get_bookings(user):
    if user['role'] == 'admin':
        bookings = storage.get_all('bookings')
    else:
        bookings = storage.get_by_field('bookings', 'user_id', user['id'])
    
    rooms = {r['id']: r for r in storage.get_all('rooms')}
    for b in bookings:
        room = rooms.get(b.get('room_id'), {})
        b['room_name'] = room.get('name', '')
    
    return jsonify({'bookings': bookings}), 200


@booking_bp.route('/', methods=['POST'])
@token_required
def create_booking(user):
    data = request.get_json()
    room_id = data.get('room_id')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    
    if not all([room_id, date, start_time, end_time]):
        return jsonify({'error': 'Missing fields'}), 400
    
    booking = Booking(
        room_id=room_id,
        user_id=user['id'],
        date=date,
        start_time=start_time,
        end_time=end_time,
        purpose=data.get('purpose', ''),
        status='confirmed'
    )
    saved = storage.create('bookings', booking.to_dict())
    return jsonify({'booking': saved, 'message': 'Booked!'}), 201


@booking_bp.route('/<booking_id>', methods=['DELETE'])
@token_required
def cancel_booking(user, booking_id):
    booking = storage.get_by_id('bookings', booking_id)
    if not booking:
        return jsonify({'error': 'Not found'}), 404
    
    if booking.get('user_id') != user['id'] and user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    storage.update('bookings', booking_id, {'status': 'cancelled'})
    return jsonify({'message': 'Cancelled'}), 200
