from flask_login import UserMixin
from extensions import db
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'speaker' or 'manager'
    password = db.Column(db.String(128), nullable=False)
    # Additional fields for speaker registration
    track = db.Column(db.String(50))
    tshirt_size = db.Column(db.String(10))
    food_choice = db.Column(db.String(10))
    blood_group = db.Column(db.String(10))
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_number = db.Column(db.String(20))
    linkedin_url = db.Column(db.String(200))
    sap_community_url = db.Column(db.String(200))
    # Co-speaker fields
    speaker2_name = db.Column(db.String(100))
    speaker2_email = db.Column(db.String(120))
    speaker2_tshirt_size = db.Column(db.String(10))
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = db.relationship('Session', backref='speaker', lazy=True, foreign_keys='Session.speaker_id')
    certificates = db.relationship('Certificate', backref='speaker', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    track = db.Column(db.String(50))
    status = db.Column(db.String(20), default='submitted')
    speaker_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    speaker2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    timeslot = db.Column(db.String(50))
    location = db.Column(db.String(100))
    session_type = db.Column(db.String(50))  # Master Class, Demo Pod, Talk
    confirmation_status = db.Column(db.String(20), default='pending')  # pending, confirmed, declined
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documents = db.relationship('Document', backref='session', lazy=True)
    feedback = db.relationship('Feedback', backref='session', lazy=True)
    change_requests = db.relationship('ChangeRequest', backref='session', lazy=True)

class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    timeslot = db.Column(db.String(50))
    track = db.Column(db.String(50))
    location = db.Column(db.String(100))
    type = db.Column(db.String(50))
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    drive_link = db.Column(db.String(200))
    document_type = db.Column(db.String(50))  # presentation, demo, promotional
    filename = db.Column(db.String(200))
    file_size = db.Column(db.Integer)
    deadline = db.Column(db.DateTime)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    attendee_name = db.Column(db.String(100))
    attendee_email = db.Column(db.String(120))
    rating = db.Column(db.Integer)  # 1-5 scale
    comments = db.Column(db.Text)
    responses = db.Column(db.Text)  # JSON for custom questions
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speaker_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=True)
    image_path = db.Column(db.String(200))
    certificate_type = db.Column(db.String(50))  # speaker, participation
    downloaded = db.Column(db.Boolean, default=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChangeRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    request_type = db.Column(db.String(50))  # title, abstract, speaker
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    processed_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(200))
    message = db.Column(db.Text)
    notification_type = db.Column(db.String(50))  # email, session_update, reminder
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EmailTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_name = db.Column(db.String(100))
    subject = db.Column(db.String(200))
    body = db.Column(db.Text)
    template_type = db.Column(db.String(50))  # confirmation, rejection, reminder
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    qr_type = db.Column(db.String(50))  # checkin, tshirt
    qr_data = db.Column(db.String(200))
    image_path = db.Column(db.String(200))
    is_used = db.Column(db.Boolean, default=False)
    used_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
