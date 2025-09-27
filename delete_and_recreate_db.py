#!/usr/bin/env python3
"""
Delete existing database and create a fresh one
"""

import os
import sys
import shutil
from datetime import datetime

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

def delete_and_recreate_database():
    """Delete existing database and create a fresh one"""
    print("🗑️  Deleting existing database and creating fresh one...")
    print("=" * 60)
    
    # Get the backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    instance_dir = os.path.join(backend_dir, 'instance')
    db_path = os.path.join(instance_dir, 'vibeathon.db')
    
    # Delete existing database if it exists
    if os.path.exists(db_path):
        # Create backup first
        backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(db_path, backup_path)
        print(f"✅ Database backed up to: {backup_path}")
        
        # Delete the database
        os.remove(db_path)
        print("🗑️  Existing database deleted")
    else:
        print("ℹ️  No existing database found")
    
    # Delete the entire instance directory to be sure
    if os.path.exists(instance_dir):
        shutil.rmtree(instance_dir)
        print("🗑️  Instance directory cleaned")
    
    # Create fresh database
    print("🔄 Creating fresh database...")
    
    try:
        from app import create_app
        from extensions import db
        from models import User, EmailTemplate
        from email_service import create_default_templates
        from werkzeug.security import generate_password_hash
        
        app = create_app()
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Create default email templates
            print("📧 Creating default email templates...")
            create_default_templates()
            print("✅ Default email templates created!")
            
            # Create default manager user
            print("👨‍💼 Creating default manager user...")
            manager = User(
                full_name="Event Manager",
                email="manager@vibeathon.com",
                password=generate_password_hash("manager123"),
                mobile="+1234567890",
                role="manager"
            )
            db.session.add(manager)
            db.session.commit()
            print("✅ Default manager user created!")
            
            # Create sample speaker user
            print("👤 Creating sample speaker user...")
            speaker = User(
                full_name="John Doe",
                email="speaker@vibeathon.com",
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
            
            print("\n🎉 Fresh database created successfully!")
            print("\n📋 Default Login Credentials:")
            print("   Manager:")
            print("     Email: manager@vibeathon.com")
            print("     Password: manager123")
            print("   Speaker:")
            print("     Email: speaker@vibeathon.com")
            print("     Password: speaker123")
            print("\n🚀 You can now run the application with: python run.py")
            
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    delete_and_recreate_database()
