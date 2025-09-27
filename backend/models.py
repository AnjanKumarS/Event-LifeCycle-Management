from flask_login import UserMixin
from extensions import db

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

class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    timeslot = db.Column(db.String(50))
    track = db.Column(db.String(50))
    location = db.Column(db.String(100))
    type = db.Column(db.String(50))

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    drive_link = db.Column(db.String(200))
    deadline = db.Column(db.String(50))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    responses = db.Column(db.Text)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speaker_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_path = db.Column(db.String(200))
    downloaded = db.Column(db.Boolean, default=False)
