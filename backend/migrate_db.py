#!/usr/bin/env python3
"""
Database migration script for Speaker Persona App
Handles database schema updates and data migration
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db

def backup_database():
    """Create a backup of the existing database"""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'vibeathon.db')
    if os.path.exists(db_path):
        backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"✅ Database backed up to: {backup_path}")
        return backup_path
    return None

def check_column_exists(cursor, table_name, column_name):
    """Check if a column exists in a table"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    return column_name in columns

def migrate_database():
    """Migrate the existing database to the new schema"""
    app = create_app()
    
    with app.app_context():
        db_path = os.path.join(app.instance_path, 'vibeathon.db')
        
        if not os.path.exists(db_path):
            print("📝 No existing database found. Creating new database...")
            db.create_all()
            print("✅ New database created successfully!")
            return True
        
        print("🔄 Migrating existing database...")
        
        # Create backup
        backup_path = backup_database()
        
        try:
            # Connect to the database directly
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check and add missing columns to user table
            if not check_column_exists(cursor, 'user', 'created_at'):
                print("➕ Adding created_at column to user table...")
                cursor.execute("ALTER TABLE user ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            
            if not check_column_exists(cursor, 'user', 'updated_at'):
                print("➕ Adding updated_at column to user table...")
                cursor.execute("ALTER TABLE user ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            
            # Update existing users with current timestamp
            cursor.execute("UPDATE user SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
            cursor.execute("UPDATE user SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL")
            
            # Check and add missing columns to session table
            if not check_column_exists(cursor, 'session', 'location'):
                print("➕ Adding location column to session table...")
                cursor.execute("ALTER TABLE session ADD COLUMN location VARCHAR(100)")
            
            if not check_column_exists(cursor, 'session', 'session_type'):
                print("➕ Adding session_type column to session table...")
                cursor.execute("ALTER TABLE session ADD COLUMN session_type VARCHAR(50)")
            
            if not check_column_exists(cursor, 'session', 'confirmation_status'):
                print("➕ Adding confirmation_status column to session table...")
                cursor.execute("ALTER TABLE session ADD COLUMN confirmation_status VARCHAR(20) DEFAULT 'pending'")
            
            if not check_column_exists(cursor, 'session', 'created_at'):
                print("➕ Adding created_at column to session table...")
                cursor.execute("ALTER TABLE session ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            
            if not check_column_exists(cursor, 'session', 'updated_at'):
                print("➕ Adding updated_at column to session table...")
                cursor.execute("ALTER TABLE session ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            
            # Update existing sessions
            cursor.execute("UPDATE session SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
            cursor.execute("UPDATE session SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL")
            
            # Check and add missing columns to agenda table
            if not check_column_exists(cursor, 'agenda', 'is_published'):
                print("➕ Adding is_published column to agenda table...")
                cursor.execute("ALTER TABLE agenda ADD COLUMN is_published BOOLEAN DEFAULT 0")
            
            if not check_column_exists(cursor, 'agenda', 'created_at'):
                print("➕ Adding created_at column to agenda table...")
                cursor.execute("ALTER TABLE agenda ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            
            # Check and add missing columns to document table
            if not check_column_exists(cursor, 'document', 'document_type'):
                print("➕ Adding document_type column to document table...")
                cursor.execute("ALTER TABLE document ADD COLUMN document_type VARCHAR(50)")
            
            if not check_column_exists(cursor, 'document', 'filename'):
                print("➕ Adding filename column to document table...")
                cursor.execute("ALTER TABLE document ADD COLUMN filename VARCHAR(200)")
            
            if not check_column_exists(cursor, 'document', 'file_size'):
                print("➕ Adding file_size column to document table...")
                cursor.execute("ALTER TABLE document ADD COLUMN file_size INTEGER")
            
            if not check_column_exists(cursor, 'document', 'deadline'):
                print("➕ Adding deadline column to document table...")
                cursor.execute("ALTER TABLE document ADD COLUMN deadline DATETIME")
            
            if not check_column_exists(cursor, 'document', 'uploaded_at'):
                print("➕ Adding uploaded_at column to document table...")
                cursor.execute("ALTER TABLE document ADD COLUMN uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            
            if not check_column_exists(cursor, 'document', 'is_approved'):
                print("➕ Adding is_approved column to document table...")
                cursor.execute("ALTER TABLE document ADD COLUMN is_approved BOOLEAN DEFAULT 0")
            
            # Check and add missing columns to feedback table
            if not check_column_exists(cursor, 'feedback', 'attendee_name'):
                print("➕ Adding attendee_name column to feedback table...")
                cursor.execute("ALTER TABLE feedback ADD COLUMN attendee_name VARCHAR(100)")
            
            if not check_column_exists(cursor, 'feedback', 'attendee_email'):
                print("➕ Adding attendee_email column to feedback table...")
                cursor.execute("ALTER TABLE feedback ADD COLUMN attendee_email VARCHAR(120)")
            
            if not check_column_exists(cursor, 'feedback', 'rating'):
                print("➕ Adding rating column to feedback table...")
                cursor.execute("ALTER TABLE feedback ADD COLUMN rating INTEGER")
            
            if not check_column_exists(cursor, 'feedback', 'comments'):
                print("➕ Adding comments column to feedback table...")
                cursor.execute("ALTER TABLE feedback ADD COLUMN comments TEXT")
            
            if not check_column_exists(cursor, 'feedback', 'submitted_at'):
                print("➕ Adding submitted_at column to feedback table...")
                cursor.execute("ALTER TABLE feedback ADD COLUMN submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            
            # Check and add missing columns to certificate table
            if not check_column_exists(cursor, 'certificate', 'session_id'):
                print("➕ Adding session_id column to certificate table...")
                cursor.execute("ALTER TABLE certificate ADD COLUMN session_id INTEGER")
            
            if not check_column_exists(cursor, 'certificate', 'certificate_type'):
                print("➕ Adding certificate_type column to certificate table...")
                cursor.execute("ALTER TABLE certificate ADD COLUMN certificate_type VARCHAR(50)")
            
            if not check_column_exists(cursor, 'certificate', 'generated_at'):
                print("➕ Adding generated_at column to certificate table...")
                cursor.execute("ALTER TABLE certificate ADD COLUMN generated_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            
            # Create new tables that might not exist
            print("🔄 Creating new tables...")
            
            # Create change_request table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS change_request (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    request_type VARCHAR(50) NOT NULL,
                    old_value TEXT,
                    new_value TEXT,
                    status VARCHAR(20) DEFAULT 'pending',
                    requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    processed_at DATETIME,
                    processed_by INTEGER,
                    FOREIGN KEY (session_id) REFERENCES session (id),
                    FOREIGN KEY (processed_by) REFERENCES user (id)
                )
            """)
            
            # Create notification table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notification (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title VARCHAR(200) NOT NULL,
                    message TEXT,
                    notification_type VARCHAR(50),
                    is_read BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            """)
            
            # Create email_template table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS email_template (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    template_name VARCHAR(100) NOT NULL,
                    subject VARCHAR(200) NOT NULL,
                    body TEXT NOT NULL,
                    template_type VARCHAR(50) NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create qr_code table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS qr_code (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    qr_type VARCHAR(50) NOT NULL,
                    qr_data VARCHAR(200) NOT NULL,
                    image_path VARCHAR(200),
                    is_used BOOLEAN DEFAULT 0,
                    used_at DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            """)
            
            conn.commit()
            conn.close()
            
            print("✅ Database migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            if backup_path:
                print(f"🔄 Restoring from backup: {backup_path}")
                import shutil
                shutil.copy2(backup_path, db_path)
            return False

def main():
    """Main migration function"""
    print("🔄 Speaker Persona App - Database Migration")
    print("=" * 50)
    
    if migrate_database():
        print("\n🎉 Migration completed successfully!")
        print("🚀 You can now run the application with: python app.py")
    else:
        print("\n❌ Migration failed!")
        print("💡 Try deleting the database file and running python init_db.py instead")
        sys.exit(1)

if __name__ == "__main__":
    main()
