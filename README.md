# ChatBox

A lightweight peer-to-peer desktop chat application built with Python and CustomTkinter. Chat directly with friends over the internet without relying on third-party messaging services.

## Overview

ChatBox enables direct, decentralized communication between users by establishing peer-to-peer TCP connections. All chat history is stored locally in SQLite databases, giving you complete ownership of your data. The application features a modern dark/light mode UI and intuitive connection management.

## Features

- **Peer-to-Peer Messaging**: Direct TCP socket connections between users
- **Local Data Storage**: All messages stored in local SQLite databases
- **Connection Management**: Save and manage multiple peer connections
- **Dark/Light Mode**: Toggle between appearance modes in the UI
- **User Authentication**: Local credential-based login system
- **Modern UI**: Built with CustomTkinter for a professional desktop experience
- **Cross-Platform**: Runs on Windows, macOS, and Linux
- **Standalone Executable**: Downloadable .exe for Windows (no Python installation required)

## How It Works

### Architecture

- **Frontend**: CustomTkinter 5.2.1 for the desktop UI
- **Networking**: Python `socket` module for TCP peer-to-peer communication
- **Storage**: SQLite for local message history and connection data
- **Authentication**: YAML-based credential storage with MD5 hashing
- **Threading**: Background threads for non-blocking network operations

### Core Components

1. **chat_ui.py** - Main application window with messaging interface
2. **chatNet_utils.py** - User authentication and credential management
3. **manage_connections.py** - P2P network layer with ConnectionManager class
4. **db.py** - SQLite database initialization and schema
5. **login.py** - Login dialog and credential verification

## File Structure

```
ChatBox/
├── configs/
│   ├── cred.yml              # User credentials (MD5 hashed)
│   ├── c.json                # Application configuration
│   ├── log.yml               # Logging configuration
│   ├── chat.db               # Chat message history (SQLite)
│   └── connections.db        # Saved peer connections (SQLite)
├── scripts/
│   ├── chat_ui.py            # Main chat interface (395 lines)
│   ├── chatNet_utils.py      # Authentication utilities (60 lines)
│   ├── manage_connections.py # P2P networking layer (182 lines)
│   ├── db.py                 # Database management (25 lines)
│   └── login.py              # Login dialog
├── build_app.py              # PyInstaller build automation
├── setup.py                  # Python package configuration
├── requirements.txt          # Python dependencies
├── run_chatbox.bat           # Windows launcher script
├── INSTALL.md                # Installation guide
├── DISTRIBUTION.md           # Distribution & release guide
├── Pipfile                   # Pipenv configuration
└── README.md                 # This file
```

## Getting Started

### Option 1: Download Pre-Built Executable (Easiest)

1. Download `ChatBox.zip` from the [releases page](https://github.com/youruser/ChatBox/releases)
2. Extract the ZIP file
3. Double-click `ChatBox.exe` to launch
4. No additional software needed (Python is bundled)

### Option 2: Install from Source (Python 3.9+)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ChatBox
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python scripts/login.py
   ```

### Option 3: Build Your Own Executable

1. Follow Option 2 (install from source)
2. Build the executable:
   ```bash
   python build_app.py
   ```
3. Find the executable in `dist/ChatBox/ChatBox.exe`

## Usage

### First Time Setup

1. **Launch ChatBox** - Run the executable or `python scripts/login.py`
2. **Login** - Enter your username and password
   - Default credentials: username `test`, password `pwd`
   - Credentials are hashed and stored in `configs/cred.yml`
3. **Add a Connection** - Click "Connect" to set up a peer connection
4. **Enter Peer Details**:
   - Peer Username
   - Peer IP Address (their host IP)
   - Peer Port (listening port, default 5000)
5. **Start Chatting** - Select the peer from the dropdown and send messages

### Managing Connections

- **Save Connection**: After entering peer details, click "Save Connection" to store for future use
- **Load Saved Connection**: Select from the "Saved Connections" dropdown to auto-populate fields
- **Connect to Peer**: After configuring details, click "Connect to Peer" to establish the connection

### UI Features

- **Dark/Light Mode Toggle**: Click the mode button in the top-right corner
- **Chat Log**: Shows messages from the selected peer (peer-filtered view)
- **Connection Dropdown**: Quickly switch between saved peer connections
- **Collapsible Panel**: Hide the connection settings to maximize chat space

## Network Details

### Getting Your IP Address

**Windows:**
```powershell
ipconfig
```
Look for "IPv4 Address" (usually 192.168.x.x or 10.x.x.x)

**macOS/Linux:**
```bash
ifconfig
```
Look for "inet" address

### Port Configuration

- Default port: `5000`
- Ensure your firewall allows inbound connections on this port
- Both peers must know each other's IP address and port

### Message Format

Messages are transmitted as JSON objects over TCP:
```json
{
  "sender": "username",
  "message": "Hello!",
  "timestamp": "2024-01-15 14:30:45"
}
```

## Database Schema

### chat.db - Chat Log Table

```sql
CREATE TABLE chat_log (
  user TEXT,
  time TEXT,
  msg TEXT
);
```

### connections.db - Saved Connections Table

```sql
CREATE TABLE connections (
  id INTEGER PRIMARY KEY,
  user1 TEXT,
  user2 TEXT,
  user2_host TEXT,
  user2_port INTEGER,
  status TEXT,
  created_at TEXT,
  updated_at TEXT
);
```

## Security & Privacy

- **Local Storage**: All chat data stored on your computer, not on external servers
- **Credential Hashing**: Passwords hashed with MD5 before storing
- **Direct Connections**: Peer-to-peer communication, no intermediary servers
- **Full Control**: You control when data is accessed and shared
- **Data Portability**: Export all your chat history from SQLite databases

## Dependencies

- `customtkinter==5.2.1` - Modern GUI framework
- `pyyaml==6.0` - Configuration file handling
- `pyinstaller==6.1.0` - Build executable (development only)

See `requirements.txt` for complete dependency list.

## Troubleshooting

### Connection Issues

**Cannot connect to peer:**
- Verify peer's IP address and port are correct
- Check firewall settings allow inbound connections on the port
- Ensure both users have ChatBox running
- Try connecting from the peer's side first

**Messages not sending:**
- Check the connection status in the UI
- Verify the peer is still online
- Try clicking "Connect to Peer" again

### Application Won't Start

**Executable won't run:**
- Download a fresh copy from releases
- Check Windows antivirus isn't blocking the file
- Try running as Administrator

**Source code won't run:**
- Verify Python 3.9+ is installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`
- Check logs in `configs/log.yml`

### Database Issues

**Chat history missing:**
- Check `configs/chat.db` exists
- Verify disk space is available
- Try clearing the database (backup first, then delete `*.db` files)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Development

### Setting Up Development Environment

```bash
# Install Pipenv
pip install pipenv

# Install dependencies from Pipfile
pipenv install --dev

# Enter virtual environment
pipenv shell
```

### Building from Source

```bash
python build_app.py
```

The script will:
1. Clean old builds
2. Run PyInstaller
3. Copy configuration folder
4. Provide setup instructions

## License

This project is open source. See LICENSE file for details.

## Support

For issues, feature requests, or troubleshooting:
1. Check the [Troubleshooting](#troubleshooting) section above
2. Review existing [GitHub issues](https://github.com/youruser/ChatBox/issues)
3. Create a new issue with:
   - Your OS and Python version
   - Steps to reproduce the problem
   - Error messages from logs

## Roadmap

- [ ] Message encryption (end-to-end)
- [ ] File transfer support
- [ ] Group chat (multi-peer messaging)
- [ ] Message search and filtering
- [ ] User profile pictures
- [ ] Message reactions and emojis
- [ ] macOS and Linux installers
- [ ] Mobile app (iOS/Android)

## Credits

Built with:
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern GUI framework
- [PyInstaller](https://pyinstaller.org/) - Executable packaging
- [PyYAML](https://pyyaml.org/) - Configuration management

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Python Version**: 3.9+ 
