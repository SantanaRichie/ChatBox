#!/usr/bin/env python
"""
Build script to create a standalone ChatBox executable using PyInstaller.
Run this to generate the ChatBox.exe file.
"""

import os
import shutil
import subprocess
import sys

def build_app():
    """Build the ChatBox application"""
    
    print("=" * 60)
    print("ChatBox - Building Executable")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("ERROR: PyInstaller not installed. Install with: pip install pyinstaller")
        sys.exit(1)
    
    # Clean up old builds
    print("\n[1/4] Cleaning old builds...")
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('ChatBox.spec'):
        os.remove('ChatBox.spec')
    print("✓ Cleaned")
    
    # Build the executable
    print("\n[2/4] Building executable...")
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=ChatBox',
        '--icon=chatbox.ico',
        '--add-data', 'configs:configs',
        '--hidden-import=customtkinter',
        '--hidden-import=yaml',
        'scripts/login.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ Executable built")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        sys.exit(1)
    
    # Copy required files
    print("\n[3/4] Copying required files...")
    
    # Copy configs folder to dist if needed
    if os.path.exists('configs'):
        dist_configs = os.path.join('dist', 'configs')
        if os.path.exists(dist_configs):
            shutil.rmtree(dist_configs)
        shutil.copytree('configs', dist_configs)
    
    print("✓ Files copied")
    
    # Final message
    print("\n[4/4] Build complete!")
    print("=" * 60)
    print("✓ ChatBox.exe created in 'dist/' folder")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Copy the 'dist/ChatBox/' folder to your desired location")
    print("2. Create a shortcut to 'ChatBox.exe' on your desktop")
    print("3. Run ChatBox.exe to launch the application")
    print("\nTo distribute:")
    print("- Zip the 'dist/ChatBox/' folder as 'ChatBox.zip'")
    print("- Share with others - they just extract and run ChatBox.exe")
    

if __name__ == '__main__':
    build_app()
