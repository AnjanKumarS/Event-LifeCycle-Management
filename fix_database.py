#!/usr/bin/env python3
"""
Quick fix script for database schema issues
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

def quick_fix():
    """Quick fix for the database schema issue"""
    print("🔧 Quick Database Fix for Speaker Persona App")
    print("=" * 50)
    
    # Option 1: Reset database (recommended for development)
    print("📋 This will reset your database and create fresh data.")
    print("⚠️  All existing data will be lost!")
    
    response = input("Do you want to reset the database? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        try:
            from reset_db import reset_database
            reset_database()
            print("\n🎉 Database fixed successfully!")
            print("🚀 You can now run: python run.py")
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n💡 Alternative: Delete the database file manually and run:")
            print("   python backend/init_db.py")
    else:
        print("\n💡 Alternative solutions:")
        print("1. Run: python backend/migrate_db.py")
        print("2. Delete backend/instance/vibeathon.db and run: python backend/init_db.py")
        print("3. Run: python backend/reset_db.py")

if __name__ == "__main__":
    quick_fix()
