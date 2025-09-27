#!/usr/bin/env python3
"""
Database initialization script for Speaker Persona App
Creates database tables and initial data
"""

import os
import sys
from werkzeug.security import generate_password_hash

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models import User, EmailTemplate
from email_service import create_default_templates

def init_database():
    """Initialize the database with tables and default data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create default email templates
        print("Creating default email templates...")
        create_default_templates()
        print("✅ Default email templates created!")
        
        # Create default manager user if it doesn't exist
        manager_email = "manager@vibeathon.com"
        existing_manager = User.query.filter_by(email=manager_email).first()
        
        if not existing_manager:
            print("Creating default manager user...")
            manager = User(
                full_name="Event Manager",
                email=manager_email,
                password=generate_password_hash("manager123"),
                mobile="+1234567890",
                role="manager"
            )
            db.session.add(manager)
            db.session.commit()
            print("✅ Default manager user created!")
            print(f"   Email: {manager_email}")
            print(f"   Password: manager123")
        else:
            print("✅ Manager user already exists!")
        
        # Create sample speaker user for testing
        speaker_email = "speaker@vibeathon.com"
        existing_speaker = User.query.filter_by(email=speaker_email).first()
        
        if not existing_speaker:
            print("Creating sample speaker user...")
            speaker = User(
                full_name="John Doe",
                email=speaker_email,
                password=generate_password_hash("speaker123"),
                mobile="+1234567891",
                role="speaker",
                track="Technical",
                tshirt_size="L",
                food_choice="Veg",
                blood_group="O+",
                emergency_contact_name="Jane Doe",
                emergency_contact_number="+1234567892",
                linkedin_url="https://linkedin.com/in/johndoe",
                sap_community_url="https://community.sap.com/johndoe"
            )
            db.session.add(speaker)
            db.session.commit()
            print("✅ Sample speaker user created!")
            print(f"   Email: {speaker_email}")
            print(f"   Password: speaker123")
        else:
            print("✅ Sample speaker user already exists!")
        
        print("\n🎉 Database initialization completed successfully!")
        print("\n📋 Default Login Credentials:")
        print("   Manager:")
        print(f"     Email: {manager_email}")
        print("     Password: manager123")
        print("   Speaker:")
        print(f"     Email: {speaker_email}")
        print("     Password: speaker123")
        print("\n🚀 You can now run the application with: python app.py")

if __name__ == "__main__":
    init_database()