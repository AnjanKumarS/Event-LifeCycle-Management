from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Session, User, Agenda
from app import db
from datetime import datetime, timedelta

manager = Blueprint('manager', __name__)

def generate_timeslots():
    """Generate time slots for the event day."""
    slots = []
    start = datetime.strptime("09:00", "%H:%M")
    end = datetime.strptime("17:00", "%H:%M")
    current = start
    
    while current <= end:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=45)  # 45-minute slots
    
    return slots

@manager.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'manager':
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    
    # Get all session submissions
    submissions = Session.query.all()
    
    # Get all speakers
    speakers = User.query.filter_by(role='speaker').all()
    
    # Generate time slots for agenda builder
    timeslots = generate_timeslots()
    
    return render_template('manager/dashboard.html',
                         submissions=submissions,
                         speakers=speakers,
                         timeslots=timeslots)

@manager.route('/submissions/<int:id>/<action>', methods=['POST'])
@login_required
def handle_submission(id, action):
    if current_user.role != 'manager':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    session = Session.query.get_or_404(id)
    if action not in ['approve', 'reject', 'hold', 'view']:
        return jsonify({'success': False, 'message': 'Invalid action'}), 400
    
    if action != 'view':
        session.status = action
        db.session.commit()
    
        # TODO: Send email notification to speaker
        
        return jsonify({
            'success': True,
            'message': f'Session {action}ed successfully',
            'session': {
                'id': session.id,
                'status': session.status
            }
        })
    else:
        speaker = User.query.get(session.speaker_id)
        speaker2 = User.query.get(session.speaker2_id) if session.speaker2_id else None
        
        return jsonify({
            'success': True,
            'session': {
                'id': session.id,
                'title': session.title,
                'abstract': session.abstract,
                'track': session.track,
                'category': session.category,
                'status': session.status,
                'timeslot': session.timeslot,
                'speaker': {
                    'name': speaker.full_name,
                    'email': speaker.email,
                    'mobile': speaker.mobile,
                    'track': speaker.track
                },
                'speaker2': {
                    'name': speaker2.full_name,
                    'email': speaker2.email
                } if speaker2 else None
            }
        })

@manager.route('/submissions/filter', methods=['POST'])
@login_required
def filter_submissions():
    if current_user.role != 'manager':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    data = request.get_json()
    query = Session.query
    
    if data.get('track'):
        query = query.filter_by(track=data['track'])
    if data.get('status'):
        query = query.filter_by(status=data['status'])
    if data.get('search'):
        search = f"%{data['search']}%"
        query = query.filter(
            (Session.title.ilike(search)) |
            (Session.abstract.ilike(search))
        )
    
    sessions = query.all()
    return jsonify({
        'success': True,
        'submissions': [{
            'id': s.id,
            'title': s.title,
            'abstract': s.abstract,
            'track': s.track,
            'status': s.status,
            'speaker': {
                'name': User.query.get(s.speaker_id).full_name,
                'email': User.query.get(s.speaker_id).email
            }
        } for s in sessions]
    })

@manager.route('/agenda/update', methods=['POST'])
@login_required
def update_agenda():
    if current_user.role != 'manager':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    data = request.get_json()
    session_id = data.get('session_id')
    timeslot = data.get('timeslot')
    
    if not session_id or not timeslot:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    session = Session.query.get_or_404(session_id)
    session.timeslot = timeslot
    
    # Update or create agenda entry
    agenda = Agenda.query.filter_by(session_id=session_id).first()
    if not agenda:
        agenda = Agenda(session_id=session_id)
    
    agenda.timeslot = timeslot
    agenda.track = session.track
    db.session.add(agenda)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Session scheduled successfully',
        'session': {
            'id': session.id,
            'title': session.title,
            'timeslot': session.timeslot,
            'track': session.track
        }
    })