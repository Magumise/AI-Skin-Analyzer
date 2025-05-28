import os
import shutil
from pathlib import Path

def create_upload_directory():
    # Create upload directory
    upload_dir = Path('pythonanywhere_upload')
    if upload_dir.exists():
        shutil.rmtree(upload_dir)
    upload_dir.mkdir()
    
    # Directories to copy
    dirs_to_copy = [
        'backend',
        'skin_analyzer',
        'media',
        'staticfiles'
    ]
    
    # Files to copy
    files_to_copy = [
        'manage.py',
        'requirements.txt'
    ]
    
    print("🚀 Preparing files for PythonAnywhere upload...")
    
    # Copy directories
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            print(f"📁 Copying directory: {dir_name}")
            shutil.copytree(dir_name, upload_dir / dir_name)
        else:
            print(f"⚠️ Warning: Directory {dir_name} not found")
    
    # Copy files
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            print(f"📄 Copying file: {file_name}")
            shutil.copy2(file_name, upload_dir / file_name)
        else:
            print(f"⚠️ Warning: File {file_name} not found")
    
    # Create a zip file
    print("📦 Creating zip file...")
    shutil.make_archive('pythonanywhere_upload', 'zip', upload_dir)
    
    print("\n✅ Upload preparation complete!")
    print("\nNext steps:")
    print("1. Go to PythonAnywhere.com and sign up/login")
    print("2. Go to the 'Files' tab")
    print("3. Create a new directory called 'ai-skin-analyzer'")
    print("4. Upload the 'pythonanywhere_upload.zip' file")
    print("5. Extract the zip file in your PythonAnywhere directory")
    print("\nWould you like to proceed with these steps?")

if __name__ == "__main__":
    create_upload_directory() 