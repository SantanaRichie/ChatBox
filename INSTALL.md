# ChatBox - Installation Guide

## Quick Start (Windows)

### Option 1: Download Pre-Built Executable (Easiest)
1. Download `ChatBox.zip` from releases
2. Extract the folder anywhere on your computer
3. Double-click `ChatBox.exe` to launch
4. No Python installation required!

### Option 2: Install from Source (Requires Python)

#### Prerequisites
- Python 3.9 or higher
- pip (comes with Python)

#### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/SantanaRichie/ChatBox.git
   cd ChatBox
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set up user credentials in `configs/cred.yml`:
   ```yaml
   user:
       <hashed_username>: <hashed_password>
   ```

4. Run ChatBox:
   ```bash
   python scripts/login.py
   ```

### Option 3: Build Your Own Executable

1. Install build dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python build_app.py
   ```

3. Find `ChatBox.exe` in the `dist/ChatBox/` folder

4. (Optional) Create a shortcut on your desktop for easy access

## System Requirements

### Minimum
- Windows 7 or later (or Linux/Mac with Python)
- 100 MB disk space
- 512 MB RAM
- Network connection for peer-to-peer chat

### Recommended
- Windows 10 or later
- 1 GB disk space
- 2 GB RAM
- Ethernet or WiFi connection

## Troubleshooting

### "Python not found"
- Download Python from https://www.python.org
- During installation, check "Add Python to PATH"
- Restart your computer

### Port 5000 already in use
- ChatBox uses port 5000 by default
- Edit `scripts/chat_ui.py` line `42` and change the port number
- Or stop the program using that port

### Can't connect to peers
- Ensure both computers are on the same network (or accessible via internet)
- Check firewalls - may need to allow ChatBox through
- Verify you have the correct peer's host/IP address

### Permission denied errors
- Run the command prompt as Administrator
- Or install to a different folder with write permissions

## First Use

1. **Login**: Create user credentials in `configs/cred.yml` first
2. **Start Server**: ChatBox automatically starts listening on port 5000
3. **Add Connections**: Use the "Connect to Peer" panel to add peer information
4. **Send Message**: Select a peer and type your message

## Uninstallation

### Executable Version
- Simply delete the `ChatBox/` folder
- No registry changes or leftover files

### Python Version
```bash
pip uninstall ChatBox
```

## Getting Help

- Check the README.md for features and architecture
- Review `scripts/` for source code
- Open an issue on GitHub for bugs

## Next Steps

See [DISTRIBUTION.md](DISTRIBUTION.md) if you want to share your own build of ChatBox with others.
