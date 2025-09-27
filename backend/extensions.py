from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()

def format_date(value):
    """Format a date using a human-readable format"""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            try:
                value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return value
    
    if isinstance(value, datetime):
        return value.strftime("%B %d, %Y")
    return value