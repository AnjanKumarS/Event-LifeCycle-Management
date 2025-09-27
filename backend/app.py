from flask import Flask, render_template, request, jsonify
from config import Config
from extensions import db, login_manager, mail, format_date
from email_service import init_mail, create_default_templates
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Create upload directories
    os.makedirs(os.path.join(app.instance_path, 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'qrcodes'), exist_ok=True)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
    
    # Register Jinja2 filters
    app.jinja_env.filters['date'] = format_date

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    init_mail(app)

    with app.app_context():
        # Import models
        from models import User, Session, Agenda, Document, Feedback, Certificate, ChangeRequest, Notification, EmailTemplate, QRCode

        # Register blueprints
        from auth import auth
        from speaker import speaker
        from manager import manager

        app.register_blueprint(auth, url_prefix='/auth')
        app.register_blueprint(speaker, url_prefix='/speaker')
        app.register_blueprint(manager, url_prefix='/manager')

        # Main routes
        @app.route('/')
        def index():
            return render_template('index.html')

        # API Routes for frontend
        @app.route('/api/register', methods=['POST'])
        def api_register():
            from auth import register
            return register()

        @app.route('/api/login', methods=['POST'])
        def api_login():
            from auth import login
            return login()

        @login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))

        # Create all database tables
        db.create_all()
        
        # Create default email templates
        create_default_templates()

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
