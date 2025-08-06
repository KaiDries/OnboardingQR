#!/usr/bin/env python3
"""
Deployment preparation script for AnyKrowd Onboarding QR Generator
Version: 1.0.0

This script prepares the application for production deployment.
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Set

def get_project_files() -> Set[str]:
    """Get list of files to include in deployment"""
    include_files = {
        # Core application files
        'main.py',
        'qr_generator.py', 
        'database.py',
        'config.py',
        'utils.py',
        'version.py',
        'logging_config.py',
        
        # Configuration files
        'requirements.txt',
        '.env.example',
        '.gitignore',
        
        # Documentation
        'README.md',
        
        # Setup and test files
        'setup.py',
        'test_application.py',
        
        # Required assets
        'TOPUPMANUAL.png'
    }
    
    return include_files

def get_exclude_patterns() -> Set[str]:
    """Get patterns to exclude from deployment"""
    exclude_patterns = {
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.env',
        'temp',
        'output',
        '*.pdf',
        'missing_users_import.csv',
        '.vscode',
        '.idea',
        'logs'
    }
    
    return exclude_patterns

def should_include_file(file_path: Path, include_files: Set[str], exclude_patterns: Set[str]) -> bool:
    """Determine if a file should be included in deployment"""
    file_name = file_path.name
    
    # Skip deployment directory entirely
    if 'deployment' in file_path.parts:
        return False
    
    # Check if explicitly included
    if file_name in include_files:
        return True
    
    # Check if matches exclude pattern
    for pattern in exclude_patterns:
        if pattern in str(file_path):
            return False
    
    # Include .github directory and markdown files
    if '.github' in str(file_path) or file_path.suffix == '.md':
        return True
    
    return False

def create_deployment_package():
    """Create deployment package"""
    print("=" * 60)
    print("AnyKrowd Onboarding QR Generator - Deployment Package")
    print("=" * 60)
    
    # Get version information
    try:
        from version import __version__
        version = __version__
    except ImportError:
        version = "1.0.0"
    
    # Create deployment directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    deployment_name = f"onboarding-qr-generator-v{version}-{timestamp}"
    deployment_dir = Path("deployment") / deployment_name
    deployment_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating deployment package: {deployment_name}")
    
    # Get file lists
    include_files = get_project_files()
    exclude_patterns = get_exclude_patterns()
    
    # Copy files
    copied_files = 0
    project_root = Path(".")
    
    for item in project_root.rglob("*"):
        if item.is_file() and should_include_file(item, include_files, exclude_patterns):
            # Create relative path structure
            relative_path = item.relative_to(project_root)
            target_path = deployment_dir / relative_path
            
            # Create parent directories
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(item, target_path)
            copied_files += 1
            print(f"✓ {relative_path}")
    
    print(f"\nCopied {copied_files} files to deployment directory")
    
    # Create deployment instructions
    instructions_path = deployment_dir / "DEPLOYMENT_INSTRUCTIONS.md"
    create_deployment_instructions(instructions_path, version)
    
    # Create ZIP archive
    zip_path = Path("deployment") / f"{deployment_name}.zip"
    create_zip_archive(deployment_dir, zip_path)
    
    print(f"\n✅ Deployment package created:")
    print(f"   Directory: {deployment_dir}")
    print(f"   Archive: {zip_path}")
    print(f"   Version: {version}")
    
    return deployment_dir, zip_path

def create_deployment_instructions(file_path: Path, version: str):
    """Create deployment instructions file"""
    instructions = f"""# AnyKrowd Onboarding QR Generator v{version}
## Deployment Instructions

### 1. Prerequisites
- Python 3.8 or higher
- Access to AWS RDS MySQL database
- Required Python packages (see requirements.txt)

### 2. Installation Steps

1. **Extract files to target directory**
   ```bash
   # Extract deployment package to desired location
   unzip onboarding-qr-generator-v{version}-*.zip
   cd onboarding-qr-generator-v{version}-*
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Test installation**
   ```bash
   python setup.py
   python test_application.py
   ```

5. **Run application**
   ```bash
   python main.py
   ```

### 3. Configuration

Edit the `.env` file with your specific settings:
- Database connection details
- Output directory preferences
- Logging configuration

### 4. Verification

Run the test suite to verify everything is working:
```bash
python test_application.py
```

### 5. Usage

Start the application:
```bash
python main.py
```

Follow the interactive prompts to generate QR codes.

### 6. Support

For technical support, contact the AnyKrowd Development Team.

---
**Version**: {version}
**Deployment Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Generated by**: AnyKrowd Deployment System
"""
    
    file_path.write_text(instructions, encoding='utf-8')
    print(f"✓ Created deployment instructions: {file_path.name}")

def create_zip_archive(source_dir: Path, zip_path: Path):
    """Create ZIP archive of deployment directory"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                arc_name = file_path.relative_to(source_dir.parent)
                zipf.write(file_path, arc_name)
    
    print(f"✓ Created ZIP archive: {zip_path.name}")

def main():
    """Main deployment function"""
    try:
        # Check if we're in the right directory
        if not Path("main.py").exists():
            print("❌ Error: Run this script from the project root directory")
            sys.exit(1)
        
        # Create deployment package
        deployment_dir, zip_path = create_deployment_package()
        
        print("\n" + "=" * 60)
        print("DEPLOYMENT READY")
        print("=" * 60)
        print("The deployment package is ready for distribution.")
        print(f"Share the ZIP file: {zip_path}")
        print("\nNext steps:")
        print("1. Test the deployment package in a clean environment")
        print("2. Update documentation if needed")
        print("3. Distribute to end users")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
