from flask import current_app
from flask_mail import Mail, Message
from models import EmailTemplate, User, Session
from extensions import db
import os

mail = Mail()

def init_mail(app):
    """Initialize Flask-Mail with the app"""
    mail.init_app(app)

def send_email(to, subject, body, template_type=None):
    """Send email to recipient"""
    try:
        msg = Message(
            subject=subject,
            recipients=[to],
            body=body,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send email to {to}: {str(e)}")
        return False

def send_template_email(to, template_type, **kwargs):
    """Send email using template"""
    template = EmailTemplate.query.filter_by(
        template_type=template_type, 
        is_active=True
    ).first()
    
    if not template:
        # Use default templates
        template = get_default_template(template_type)
    
    if template:
        subject = template.subject.format(**kwargs)
        body = template.body.format(**kwargs)
        return send_email(to, subject, body)
    
    return False

def get_default_template(template_type):
    """Get default email template"""
    default_templates = {
        'session_confirmation': EmailTemplate(
            template_name='Session Confirmation',
            subject='Your Session Has Been Approved - Vibeathon',
            body='''Dear {speaker_name},

Congratulations! Your session "{session_title}" has been approved for Vibeathon.

Session Details:
- Title: {session_title}
- Track: {track}
- Category: {category}
- Time Slot: {timeslot}

Please confirm your availability and upload your presentation materials.

Best regards,
Vibeathon Team''',
            template_type='session_confirmation'
        ),
        'session_rejection': EmailTemplate(
            template_name='Session Rejection',
            subject='Session Submission Update - Vibeathon',
            body='''Dear {speaker_name},

Thank you for your interest in Vibeathon. Unfortunately, we cannot accommodate your session "{session_title}" at this time.

We encourage you to participate as an attendee and look forward to seeing you at the event.

Best regards,
Vibeathon Team''',
            template_type='session_rejection'
        ),
        'reminder': EmailTemplate(
            template_name='Reminder',
            subject='Reminder: {reminder_type} - Vibeathon',
            body='''Dear {speaker_name},

This is a friendly reminder about your upcoming {reminder_type}.

{reminder_details}

Best regards,
Vibeathon Team''',
            template_type='reminder'
        ),
        'document_upload': EmailTemplate(
            template_name='Document Upload',
            subject='Document Upload Required - Vibeathon',
            body='''Dear {speaker_name},

Please upload your presentation materials for your session "{session_title}".

Deadline: {deadline}

You can upload your documents through the speaker dashboard.

Best regards,
Vibeathon Team''',
            template_type='document_upload'
        )
    }
    
    return default_templates.get(template_type)

def send_session_notification(session_id, notification_type):
    """Send notification for session status change"""
    session = Session.query.get(session_id)
    if not session:
        return False
    
    speaker = User.query.get(session.speaker_id)
    if not speaker:
        return False
    
    kwargs = {
        'speaker_name': speaker.full_name,
        'session_title': session.title,
        'track': session.track,
        'category': session.category,
        'timeslot': session.timeslot or 'TBD'
    }
    
    return send_template_email(speaker.email, notification_type, **kwargs)

def send_reminder_email(user_id, reminder_type, reminder_details):
    """Send reminder email to user"""
    user = User.query.get(user_id)
    if not user:
        return False
    
    kwargs = {
        'speaker_name': user.full_name,
        'reminder_type': reminder_type,
        'reminder_details': reminder_details
    }
    
    return send_template_email(user.email, 'reminder', **kwargs)

def create_default_templates():
    """Create default email templates in database"""
    templates = [
        EmailTemplate(
            template_name='Session Confirmation',
            subject='Your Session Has Been Approved - Vibeathon',
            body='''Dear {speaker_name},

Congratulations! Your session "{session_title}" has been approved for Vibeathon.

Session Details:
- Title: {session_title}
- Track: {track}
- Category: {category}
- Time Slot: {timeslot}

Please confirm your availability and upload your presentation materials.

Best regards,
Vibeathon Team''',
            template_type='session_confirmation'
        ),
        EmailTemplate(
            template_name='Session Rejection',
            subject='Session Submission Update - Vibeathon',
            body='''Dear {speaker_name},

Thank you for your interest in Vibeathon. Unfortunately, we cannot accommodate your session "{session_title}" at this time.

We encourage you to participate as an attendee and look forward to seeing you at the event.

Best regards,
Vibeathon Team''',
            template_type='session_rejection'
        ),
        EmailTemplate(
            template_name='Document Upload Reminder',
            subject='Document Upload Required - Vibeathon',
            body='''Dear {speaker_name},

Please upload your presentation materials for your session "{session_title}".

Deadline: {deadline}

You can upload your documents through the speaker dashboard.

Best regards,
Vibeathon Team''',
            template_type='document_upload'
        )
    ]
    
    for template in templates:
        existing = EmailTemplate.query.filter_by(template_type=template.template_type).first()
        if not existing:
            db.session.add(template)
    
    db.session.commit()
