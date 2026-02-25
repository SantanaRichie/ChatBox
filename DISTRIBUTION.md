# ChatBox - Distribution Guide

This guide explains how to package and distribute ChatBox as a downloadable application.

## Building the Executable

### Prerequisites
- Python 3.9+
- PyInstaller installed (`pip install pyinstaller`)

### Build Steps

```bash
# Install dependencies
pip install -r requirements.txt

# Run the build script
python build_app.py
```

The executable will be created in `dist/ChatBox/ChatBox.exe`

## Package for Distribution

### Method 1: ZIP Archive (Recommended)

```bash
# After building
cd dist
Compress-Archive -Path ChatBox -DestinationPath ChatBox.zip
```

This creates `ChatBox.zip` containing:
```
ChatBox/
├── ChatBox.exe        (Main executable)
├── configs/           (Configuration files)
│   ├── cred.yml      (User credentials template)
│   ├── chat.db       (Chat database)
│   └── connections.db (Connections database)
└── [other libraries]
```

### Method 2: Installer (NSIS)

For a professional installer experience, use NSIS:

1. Install NSIS from https://nsis.sourceforge.io
2. Create `installer.nsi`:

```nsis
!include "MUI2.nsh"

Name "ChatBox"
OutFile "ChatBox-Installer.exe"
InstallDir "$PROGRAMFILES\ChatBox"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "dist\ChatBox\*.*"
  CreateShortcut "$SMPROGRAMS\ChatBox.lnk" "$INSTDIR\ChatBox.exe"
  CreateShortcut "$DESKTOP\ChatBox.lnk" "$INSTDIR\ChatBox.exe"
SectionEnd
```

3. Compile with NSIS to generate installer

## Distribution Options

### Option 1: GitHub Releases
1. Build the executable
2. Create a release on GitHub
3. Upload `ChatBox.zip` as a release asset
4. Users download and extract

### Option 2: Website Download
1. Host `ChatBox.zip` on your website
2. Users download directly from your site

### Option 3: Cloud Storage
1. Upload to Google Drive, Dropbox, or OneDrive
2. Share the public download link

## Pre-Distribution Checklist

- [ ] Update version number in `setup.py`
- [ ] Update `README.md` with latest features
- [ ] Test executable on clean Windows machine
- [ ] Verify all configs are included
- [ ] Create changelog for this release
- [ ] Test peer-to-peer connections work
- [ ] Document any new features or changes

## System Requirements for Users

- **Windows**: 7 or later
- **Disk Space**: 150 MB minimum
- **RAM**: 512 MB minimum
- **Network**: Connection required for chat

## Post-Distribution

### Gather Feedback
- Ask users to report bugs on GitHub
- Track which versions are being used
- Monitor common issues

### Updates
When releasing updates:
1. Increment version in `setup.py`
2. Rebuild executable
3. Create new release with changelog
4. Notify users of new version
5. Keep older versions available

## Security Notes for Distributors

⚠️ **Important**: Before distributing:

1. **Sign the executable** (Windows Code Signing Certificate)
   - Prevents "Unknown publisher" warnings
   - Builds user trust

2. **Virus scan** the executable
   - Use VirusTotal.com to scan before release
   - Assure users it's safe

3. **Document data storage**
   - Explain where configs are saved
   - Explain what data is stored

4. **Privacy statement**
   - Clarify that chat is peer-to-peer
   - No data sent to external servers

## Size Optimization

Current build size: ~150 MB

To reduce size:
```python
# In build_app.py, add:
'--upx-dir=<UPX_PATH>',  # Use UPX compression
'--exclude-module=tcl',  # Remove unused modules
```

## Troubleshooting Distribution Issues

**"File too large"**
- Compress further with ZIP
- Some platforms have upload limits

**"Unknown publisher" warning on Windows**
- Normal for unsigned apps
- User needs to click "Run anyway"
- [See Code Signing Guide](https://docs.microsoft.com/en-us/windows/desktop/seccrypto/cryptography-essentials)

**User can't extract ZIP**
- Recommend 7-Zip or WinRAR
- Or provide pre-extracted in installer

**Port conflicts**
- Document default port 5000 in README
- Explain how to change it

## Release Template

Use this for each release:

```markdown
# ChatBox v1.0.0

## What's New
- Feature 1
- Feature 2
- Bug fixes

## Download
- [ChatBox.zip](link) - Standalone (no installation needed)
- [ChatBox-Installer.exe](link) - Windows installer

## System Requirements
- Windows 7 or later
- 150 MB disk space
- Network connection

## Installation
See [INSTALL.md](INSTALL.md)

## Known Issues
- Issue 1
- Issue 2

## Upgrade Notes
If upgrading from v0.9.0:
- No breaking changes
- Existing connections preserved
```

## Legal Considerations

- Include LICENSE file in distribution
- Add THIRD_PARTY_LICENSES for dependencies
- Consider privacy policy if collecting any data
- Follow platform-specific guidelines (Windows Store, etc.)

Good luck distributing ChatBox! 🚀
