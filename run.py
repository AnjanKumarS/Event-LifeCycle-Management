#!/usr/bin/env python3
"""
Run script for Speaker Persona App
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

def check_database_schema():
    """Check if database needs migration"""
    try:
        from app import create_app
        from extensions import db
        from models import User
        
        app = create_app()
        with app.app_context():
            # Try to query a user to check if new columns exist
            User.query.first()
            return True
    except Exception as e:
        if "no such column" in str(e):
            return False
        raise e

def main():
    """Main function"""
    # Check if database needs migration
    if not check_database_schema():
        print("🔄 Database schema needs updating...")
        print("📋 Choose an option:")
        print("1. Migrate existing database (recommended)")
        print("2. Reset database (deletes all data)")
        print("3. Exit")
        
        while True:
            choice = input("Enter your choice (1-3): ").strip()
            if choice == "1":
                print("🔄 Running database migration...")
                try:
                    from migrate_db import migrate_database
                    if migrate_database():
                        print("✅ Migration completed!")
                        break
                    else:
                        print("❌ Migration failed!")
                        sys.exit(1)
                except Exception as e:
                    print(f"❌ Migration error: {e}")
                    sys.exit(1)
            elif choice == "2":
                print("🔄 Resetting database...")
                try:
                    from reset_db import reset_database
                    reset_database()
                    break
                except Exception as e:
                    print(f"❌ Reset error: {e}")
                    sys.exit(1)
            elif choice == "3":
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    # Start the application
    from app import create_app
    
    app = create_app()
    
    # Get configuration from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print("🚀 Starting Speaker Persona App...")
    print(f"📍 Server running at: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print("📱 Open your browser and navigate to the URL above")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
