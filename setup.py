#!/usr/bin/env python3
"""
AnyKrowd Onboarding QR Code Generator - Setup Script
Version: 1.0.0
Author: AnyKrowd Development Team

This script sets up the environment and validates the installation.
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import List, Tuple

def check_python_version() -> bool:
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_requirements() -> Tuple[bool, List[str]]:
    """Check if all required packages are installed"""
    requirements = [
        'mysql-connector-python',
        'qrcode',
        'Pillow',
        'reportlab',
        'python-dotenv'
    ]
    
    missing = []
    for package in requirements:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    return len(missing) == 0, missing

def create_directories() -> None:
    """Create necessary directories"""
    directories = ['output', 'temp']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directory created: {directory}/")

def check_env_file() -> bool:
    """Check if .env file exists"""
    if Path('.env').exists():
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("   Please copy .env.example to .env and configure your database settings")
        return False

def install_requirements() -> bool:
    """Install missing requirements"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def main():
    """Main setup function"""
    print("=== AnyKrowd Onboarding QR Generator Setup ===\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\n--- Checking Requirements ---")
    all_installed, missing = check_requirements()
    
    if not all_installed:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Installing missing packages...")
        if not install_requirements():
            sys.exit(1)
    
    print("\n--- Setting up Directories ---")
    create_directories()
    
    print("\n--- Checking Configuration ---")
    env_exists = check_env_file()
    
    print("\n--- Setup Summary ---")
    print("✅ Python version check passed")
    print("✅ All requirements installed")
    print("✅ Directories created")
    
    if env_exists:
        print("✅ Configuration file ready")
        print("\n🎉 Setup complete! You can now run: python main.py")
    else:
        print("⚠️  Please configure .env file before running the application")
        print("\n📝 Next steps:")
        print("   1. Copy .env.example to .env")
        print("   2. Configure your database credentials in .env")
        print("   3. Run: python main.py")

if __name__ == "__main__":
    main()
