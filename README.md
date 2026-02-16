# ChatBox

A desktop chat application that leverages personal cloud storage (Google Drive) to store chat logs, putting data back into the hands of the creators.

## Overview

ChatBox is a privacy-focused desktop chat client that stores all conversation data on your personal Google Drive rather than on third-party servers. This approach ensures that you maintain complete ownership and control over your chat history.

## How It Works

### Architecture
- **Frontend**: Built with PySimpleGUI for a clean, responsive desktop interface
- **Backend**: Python-based with SQLite for local data management
- **Cloud Storage**: Google Drive API for secure chat log synchronization
- **Authentication**: OAuth 2.0 with Google for secure Drive access

### Core Features

1. **Secure Authentication**
   - User credentials are stored locally in `configs/cred.yml` with MD5 hashing
   - Google OAuth 2.0 integration for Drive access
   - Token-based authentication with automatic refresh

2. **Chat Management**
   - Real-time chat interface with message history
   - SQLite database (`chat.db`) for local message storage
   - Automatic synchronization with Google Drive
   - Thread-based message updates every 5 seconds

3. **Data Synchronization**
   - Chat logs are uploaded to Google Drive as `chat.db` files
   - Automatic backup and restore functionality
   - Continuation support through `continued_chat.json` tracking
   - Local cache for offline access

### File Structure

```
ChatBox/
├── configs/
│   ├── cred.yml          # User credentials (hashed)
│   ├── chat.db           # Local SQLite database
│   ├── continued_chat.json # Drive file tracking
│   ├── credentials.json  # Google OAuth credentials
│   └── token.json        # OAuth access tokens
├── scripts/
│   ├── chat_ui.py        # Main chat interface
│   ├── chatNet_utils.py  # Drive integration utilities
│   ├── db.py            # Database management
│   └── login.py         # Authentication logic
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.x
- Google Account with Drive access
- Google Cloud Project with Drive API enabled

### Installation
1. Clone the repository
2. Install dependencies: `pip install PySimpleGUI google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`
3. Set up Google OAuth credentials in `configs/credentials.json`
4. Run the application: `python scripts/login.py`

### Usage
1. Launch the application and authenticate with your Google Account
2. Enter your ChatBox credentials (stored in `configs/cred.yml`)
3. Start chatting - messages are automatically saved to your Google Drive
4. Chat history persists across sessions through Drive synchronization

## Security & Privacy

- All chat data is stored on your personal Google Drive
- Local credentials are hashed using MD5
- OAuth 2.0 ensures secure Google API access
- No third-party servers store your chat history
- Full data ownership and portability

## Technical Details

- **Database**: SQLite with `chat_log` table (user, time, msg columns)
- **Sync Protocol**: Upload/replace cycle for Drive files
- **Threading**: Background thread for automatic chat refresh
- **Error Handling**: Graceful fallback for network issues 
