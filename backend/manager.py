from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Session, User, Agenda, Document, Certificate, EmailTemplate, QRCode, ChangeRequest, Notification
from extensions import db
from email_service import send_session_notification, send_reminder_email
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
        
        # Send email notification to speaker
        if action == 'approved':
            send_session_notification(session.id, 'session_confirmation')
        elif action == 'rejected':
            send_session_notification(session.id, 'session_rejection')
        
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

@manager.route('/change-requests', methods=['GET'])
@login_required
def get_change_requests():
    if current_user.role != 'manager':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    requests = ChangeRequest.query.filter_by(status='pending').all()
    
    return jsonify({
        'success': True,
        'change_requests': [{
            'id': req.id,
            'session_id': req.session_id,
            'session_title': req.session.title,
            'request_type': req.request_type,
            'old_value': req.old_value,
            'new_value': req.new_value,
            'requested_at': req.requested_at.isoformat(),
            'speaker_name': req.session.speaker.full_name
        } for req in requests]
    })

@manager.route('/change-requests/<int:request_id>/<action>', methods=['POST'])
@login_required
def handle_change_request(request_id, action):
    if current_user.role != 'manager':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    if action not in ['approve', 'reject']:
        return jsonify({'success': False, 'message': 'Invalid action'}), 400
    
    change_request = ChangeRequest.query.get_or_404(request_id)
    session = Session.query.get(change_request.session_id)
    
    if action == 'approve':
        # Apply the change
        if change_request.request_type == 'title':
            session.title = change_request.new_value
        elif change_request.request_type == 'abstract':
            session.abstract = change_request.new_value
        elif change_request.request_type == 'category':
            session.category = change_request.new_value
        
        change_request.status = 'approved'
        change_request.processed_at = datetime.utcnow()
        change_request.processed_by = current_user.id
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Change request approved and applied',
            'change_request': {
                'id': change_request.id,
                'status': change_request.status
            }
        })
    else:
        change_request.status = 'rejected'
        change_request.processed_at = datetime.utcnow()
        change_request.processed_by = current_user.id
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Change request rejected',
            'change_request': {
                'id': change_request.id,
                'status': change_request.status
            }
        })

@manager.route('/agenda/publish', methods=['POST'])
@login_required
def publish_agenda():
    if current_user.role != 'manager':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Mark agenda as published
    agenda_items = Agenda.query.all()
    for item in agenda_items:
        item.is_published = True
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Agenda published successfully'
    })

@manager.route('/certificates/generate', methods=['POST'])
@login_required
def generate_certificates():
    if current_user.role != 'manager':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Get all approved sessions
    approved_sessions = Session.query.filter_by(status='approved').all()
    
    certificates_created = 0
    for session in approved_sessions:
        # Check if certificate already exists
        existing_cert = Certificate.query.filter_by(
            speaker_id=session.speaker_id,
            session_id=session.id
        ).first()
        
        if not existing_cert:
            certificate = Certificate(
                speaker_id=session.speaker_id,
                session_id=session.id,
                certificate_type='speaker',
                image_path=f"certificates/speaker_{session.speaker_id}_{session.id}.png"
            )
            db.session.add(certificate)
            certificates_created += 1
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'{certificates_created} certificates generated successfully'
    })

@manager.route('/reminders/send', methods=['POST'])
@login_required
def send_reminders():
    if current_user.role != 'manager':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    data = request.get_json()
    reminder_type = data.get('type')
    user_ids = data.get('user_ids', [])
    
    if not user_ids:
        # Send to all speakers
        speakers = User.query.filter_by(role='speaker').all()
        user_ids = [speaker.id for speaker in speakers]
    
    sent_count = 0
    for user_id in user_ids:
        user = User.query.get(user_id)
        if user:
            reminder_details = data.get('details', 'Please check your dashboard for updates.')
            if send_reminder_email(user_id, reminder_type, reminder_details):
                sent_count += 1
    
    return jsonify({
        'success': True,
        'message': f'Reminders sent to {sent_count} users'
    })