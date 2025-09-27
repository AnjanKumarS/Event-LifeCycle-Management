from flask import Flask, render_template
from config import Config
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # Import models
        from models import User, Session, Agenda, Document, Feedback, Certificate

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

        @login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))

        # Create all database tables
        db.create_all()

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
