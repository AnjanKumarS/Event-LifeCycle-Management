import os
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from models import Session, Document, Certificate
from app import db

speaker = Blueprint('speaker', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx', 'doc', 'docx', 'zip'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@speaker.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'speaker':
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    
    # Get speaker's sessions
    sessions = Session.query.filter_by(speaker_id=current_user.id).all()
    
    # Get speaker's certificates
    certificates = Certificate.query.filter_by(speaker_id=current_user.id).all()
    
    return render_template('speaker/dashboard.html', sessions=sessions, certificates=certificates)

@speaker.route('/sessions/new', methods=['POST'])
@login_required
def new_session():
    if current_user.role != 'speaker':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    data = request.get_json()
    session = Session(
        title=data['title'],
        abstract=data['abstract'],
        category=data['category'],
        track=data['track'],
        speaker_id=current_user.id,
        speaker2_id=data.get('speaker2_id'),
        status='pending'
    )
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Session submitted successfully!',
        'session': {
            'id': session.id,
            'title': session.title,
            'status': session.status
        }
    })

@speaker.route('/sessions/<int:session_id>/details')
@login_required
def session_details(session_id):
    session = Session.query.get_or_404(session_id)
    
    if session.speaker_id != current_user.id:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    return jsonify({
        'success': True,
        'session': {
            'id': session.id,
            'title': session.title,
            'abstract': session.abstract,
            'category': session.category,
            'track': session.track,
            'status': session.status,
            'timeslot': session.timeslot
        }
    })

@speaker.route('/sessions/<int:session_id>', methods=['PUT'])
@login_required
def update_session(session_id):
    session = Session.query.get_or_404(session_id)
    
    if session.speaker_id != current_user.id:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    if session.status != 'pending':
        return jsonify({'success': False, 'message': 'Cannot edit approved or rejected sessions'}), 400
    
    data = request.get_json()
    session.title = data.get('title', session.title)
    session.abstract = data.get('abstract', session.abstract)
    session.category = data.get('category', session.category)
    session.track = data.get('track', session.track)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Session updated successfully',
        'session': {
            'id': session.id,
            'title': session.title,
            'status': session.status
        }
    })

@speaker.route('/documents/upload', methods=['POST'])
@login_required
def upload_document():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'}), 400
    
    file = request.files['file']
    session_id = request.form.get('sessionId')
    doc_type = request.form.get('type')
    
    if not file or not file.filename:
        return jsonify({'success': False, 'message': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'File type not allowed'}), 400
    
    session = Session.query.get_or_404(session_id)
    if session.speaker_id != current_user.id:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{session_id}_{doc_type}_{timestamp}_{filename}"
    
    # Save file
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    
    # Create document record
    document = Document(
        session_id=session_id,
        drive_link=file_path
    )
    db.session.add(document)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'File uploaded successfully',
        'document': {
            'id': document.id,
            'filename': filename,
            'uploadedAt': document.created_at.isoformat(),
            'url': url_for('static', filename=f'uploads/{unique_filename}'),
            'sessionId': session_id
        }
    })

@speaker.route('/documents/<int:document_id>', methods=['DELETE'])
@login_required
def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    session = Session.query.get(document.session_id)
    
    if session.speaker_id != current_user.id:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Delete file from filesystem
    try:
        os.remove(document.drive_link)
    except OSError:
        pass
    
    # Delete record from database
    db.session.delete(document)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Document deleted successfully'
    })