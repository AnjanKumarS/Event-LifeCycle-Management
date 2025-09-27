import os
import qrcode
from io import BytesIO
import base64
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from models import Session, Document, Certificate, QRCode, ChangeRequest, Notification
from extensions import db

speaker = Blueprint('speaker', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx', 'doc', 'docx', 'zip'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_qr_code(user_id, qr_type):
    """Generate QR code for user"""
    qr_data = f"{qr_type}_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to file
    filename = f"{qr_type}_{user_id}.png"
    filepath = os.path.join(current_app.static_folder, 'qrcodes', filename)
    img.save(filepath)
    
    # Save to database
    qr_record = QRCode(
        user_id=user_id,
        qr_type=qr_type,
        qr_data=qr_data,
        image_path=f"qrcodes/{filename}"
    )
    db.session.add(qr_record)
    db.session.commit()
    
    return filepath, qr_data

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

@speaker.route('/qrcodes/generate', methods=['POST'])
@login_required
def generate_qr_codes():
    if current_user.role != 'speaker':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        # Generate check-in QR code
        checkin_path, checkin_data = generate_qr_code(current_user.id, 'checkin')
        
        # Generate t-shirt QR code
        tshirt_path, tshirt_data = generate_qr_code(current_user.id, 'tshirt')
        
        return jsonify({
            'success': True,
            'message': 'QR codes generated successfully',
            'qr_codes': {
                'checkin': {
                    'path': f"static/qrcodes/checkin_{current_user.id}.png",
                    'data': checkin_data
                },
                'tshirt': {
                    'path': f"static/qrcodes/tshirt_{current_user.id}.png",
                    'data': tshirt_data
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error generating QR codes: {str(e)}'}), 500

@speaker.route('/qrcodes/<qr_type>')
@login_required
def get_qr_code(qr_type):
    if current_user.role != 'speaker':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    if qr_type not in ['checkin', 'tshirt']:
        return jsonify({'success': False, 'message': 'Invalid QR code type'}), 400
    
    # Check if QR code exists in database
    qr_record = QRCode.query.filter_by(user_id=current_user.id, qr_type=qr_type).first()
    
    if not qr_record:
        # Generate new QR code
        try:
            filepath, qr_data = generate_qr_code(current_user.id, qr_type)
            return send_file(filepath, mimetype='image/png')
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error generating QR code: {str(e)}'}), 500
    
    # Return existing QR code
    filepath = os.path.join(current_app.static_folder, qr_record.image_path)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='image/png')
    else:
        # Regenerate if file doesn't exist
        try:
            filepath, qr_data = generate_qr_code(current_user.id, qr_type)
            return send_file(filepath, mimetype='image/png')
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error generating QR code: {str(e)}'}), 500

@speaker.route('/sessions/<int:session_id>/confirm', methods=['POST'])
@login_required
def confirm_session(session_id):
    if current_user.role != 'speaker':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    session = Session.query.get_or_404(session_id)
    if session.speaker_id != current_user.id:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    data = request.get_json()
    confirmation_status = data.get('status', 'confirmed')
    
    if confirmation_status not in ['confirmed', 'declined']:
        return jsonify({'success': False, 'message': 'Invalid confirmation status'}), 400
    
    session.confirmation_status = confirmation_status
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Session {confirmation_status} successfully',
        'session': {
            'id': session.id,
            'confirmation_status': session.confirmation_status
        }
    })

@speaker.route('/change-requests', methods=['POST'])
@login_required
def submit_change_request():
    if current_user.role != 'speaker':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    data = request.get_json()
    session_id = data.get('session_id')
    request_type = data.get('request_type')
    new_value = data.get('new_value')
    
    if not all([session_id, request_type, new_value]):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    session = Session.query.get_or_404(session_id)
    if session.speaker_id != current_user.id:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Get old value based on request type
    old_value = getattr(session, request_type, '')
    
    # Create change request
    change_request = ChangeRequest(
        session_id=session_id,
        request_type=request_type,
        old_value=old_value,
        new_value=new_value
    )
    
    db.session.add(change_request)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Change request submitted successfully',
        'change_request': {
            'id': change_request.id,
            'request_type': change_request.request_type,
            'status': change_request.status
        }
    })