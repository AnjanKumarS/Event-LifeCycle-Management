#!/usr/bin/env python3
"""
Database reset script for Speaker Persona App
Deletes existing database and creates a fresh one
"""

import os
import sys
import shutil
from datetime import datetime

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models import User, EmailTemplate
from email_service import create_default_templates
from werkzeug.security import generate_password_hash

def reset_database():
    """Reset the database by deleting and recreating it"""
    app = create_app()
    
    with app.app_context():
        # Get database path
        db_path = os.path.join(app.instance_path, 'vibeathon.db')
        
        # Create backup if database exists
        if os.path.exists(db_path):
            backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(db_path, backup_path)
            print(f"✅ Existing database backed up to: {backup_path}")
            
            # Delete existing database
            os.remove(db_path)
            print("🗑️  Existing database deleted")
        
        # Create instance directory if it doesn't exist
        os.makedirs(app.instance_path, exist_ok=True)
        
        # Create all tables
        print("🔄 Creating fresh database...")
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
        
        print("\n🎉 Database reset completed successfully!")
        print("\n📋 Default Login Credentials:")
        print("   Manager:")
        print("     Email: manager@vibeathon.com")
        print("     Password: manager123")
        print("   Speaker:")
        print("     Email: speaker@vibeathon.com")
        print("     Password: speaker123")
        print("\n🚀 You can now run the application with: python app.py")

def main():
    """Main reset function"""
    print("🔄 Speaker Persona App - Database Reset")
    print("=" * 40)
    
    # Confirm with user
    response = input("⚠️  This will delete all existing data. Continue? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Operation cancelled.")
        return
    
    reset_database()

if __name__ == "__main__":
    main()
