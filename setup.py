#!/usr/bin/env python3
"""
Setup script for Speaker Persona App
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible!")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    if os.path.exists("venv"):
        print("✅ Virtual environment already exists!")
        return True
    
    return run_command("python -m venv venv", "Creating virtual environment")

def activate_virtual_environment():
    """Get activation command for virtual environment"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def install_dependencies():
    """Install Python dependencies"""
    # Determine the correct pip path
    if platform.system() == "Windows":
        pip_path = "venv\\Scripts\\pip"
    else:
        pip_path = "venv/bin/pip"
    
    return run_command(f"{pip_path} install -r backend/requirements.txt", "Installing dependencies")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_path = "backend/.env"
    if os.path.exists(env_path):
        print("✅ .env file already exists!")
        return True
    
    print("📝 Creating .env file...")
    env_content = """# Speaker Persona App Configuration
SECRET_KEY=your_secret_key_here_change_this_in_production
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=noreply@vibeathon.com

# Database Configuration
DATABASE_URL=sqlite:///vibeathon.db

# Application Configuration
DEBUG=True
HOST=0.0.0.0
PORT=5000
"""
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("⚠️  Please update the email configuration in backend/.env")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def main():
    """Main setup function"""
    print("🎯 Speaker Persona App Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate the virtual environment:")
    print(f"   {activate_virtual_environment()}")
    print("2. Initialize the database:")
    print("   python backend/init_db.py")
    print("3. Run the application:")
    print("   python run.py")
    print("\n📧 Don't forget to configure email settings in backend/.env")
    print("🔐 Change the SECRET_KEY in production!")

if __name__ == "__main__":
    main()
