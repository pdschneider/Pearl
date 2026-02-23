# Changelog

All notable changes to **Pearl** will be located in this file.

## [0.2.0] - 2026-02-22

### Added
- Pearl is now compiled to C, greatly improving speed and performance
- CHANGELOG.md file added to better document changes
- Added startup check to sanitize context detection rules when values are missing or nonconforming

### Changed
- Moved Kokoro test to settings page GUI build to speed up launch
- Improved readability of the in-app changelog page
- Brought much closer to PEP8 compliance
- Updated Dependencies
- Updated README

### Deprecated
- Removed old spec files used for pyinstaller builds

## [0.1.12] - 2026-02-01

### Added 
- Added startup checks which analyze and sanitize corrupted values and files
- Draws window in the center of the screen when opening the program for the first time
- Added bug report icon to top bar that opens default email application
- Added delete all chats button in settings
- Added factory reset option upon GUI failure
- Added paperclip icon underneath user messages to indicate a file attachment
- Added icons to settings pages

### Changed
- Improved logic for opening the logs folder on Windows
- Normalized buttons across operating systems with updated icons
- Moved loading logic to new load_settings.py script
- General stability & UI improvements
- Updated dependencies

## [0.1.11] - 2025-12-30

### Added
- Dynamic prompt switching with context model enabled
- Added model name underneath assistant messages
- Added time groups to chat history view
- Added start/end times to assistant messages
- Added view logs button to advanced tab
- Added github button to about tab
- Remembers window placement for more consistent user experience

### Changed
- File attachment paths are logged for each message
- Minor bug fixes and improvements

## [0.1.10] - 2025-12-28

### Added
- Supports attachments for filetypes: .txt, .csv, .json, .py, .pyw, .log, .ini, .cfg, .xml, .sh, .bat, .ps1, .md, .tsv, .toml, .yaml, .html, .css, .spec
- Added experimental underlying context model choice
- Copy button added to messages
- New chat button added to the top bar
- Internal logging for each chat message's token count
- Added tooltips

### Changed
- Separated default settings from development settings for a more consistent default user experience
- Minor bug fixes and improvements

## [0.1.9] - 2025-12-19

### Added
- Functional chat history introduced
- Added audio output selection (Linux Only)

### Changed
- Minor bug fixes and improvements

## [0.1.8] - 2025-12-08

### Added
- Ships as AppImage for Linux users
- Added progress bar for slow startup scenarios
- Added program icon
- Added sidebar for later chat history implementation
- Added changelog page
- Moved startup logic to new script
- Added context detection logging

### Changed
- Minor bug fixes and improvements

## [0.1.7] - 2025-12-07

### Added
- Added about page

### Changed
- Total overhaul of main chat UI
- Total overhaul of setup page
- Minor bug fixes and improvements
- Brought closer to PEP8 compliance

### Deprecated
- Lost markdown text (not supported by Custom Tkinter)

## [0.1.6] - 2025-12-05

### Added
- Converted entire GUI to Custom Tkinter
- Added 3 new themes

### Changed
- Major UI overhaul
- Improved folder path detection on Windows systems
- Minor bug fixes and improvements

## [0.1.5] - 2025-12-02

### Added
- Added threading for more responsive UI during chats
- Added initial greeting
- Added model and hardware checks for later implementation
- Optional save chats toggle

## [0.1.4] - 2025-11-30

### Added
- Added universal cross-platform default TTS
- Queries CPU/RAM/GPU data for logging & error handling

### Changed
- UI improvements
- General error handling improvements

## [0.1.3] - 2025-11-29

### Added
- Added support for markdown italics, bold, and strike-through
- Improved TTS by removing italics, bold, and strike-through markdown from speech

### Changed
- Updated fonts for Windows users
- Removed unused query_ollama function, reducing code size

## [0.1.2] - 2025-11-28

### Added
- Added TTS with dozens of voices (requires Kokoro)
- Added dynamic settings updates

### Changed
- Skips initial Ollama API requests when Ollama is not found, speeding up initial load for systems without Ollama

### Fixed
- Suppressed extra requests debug messages, reducing log spam

## [0.1.1] - 2025-11-27

### Added
- Added requirements.txt with dependencies for easier builds
- Added rotating log files
- Added setup instructions for users without Ollama installed
- Added Windows 11 Support

### Changed
- Improved error handling

## [0.1.0] - 2025-11-25

### Added
- AI chat window
- Cosmic Sky & Pastel Green themes
- View models list & differ between loaded/not loaded to memory
- Load, unload, select specific models
- Persistent chat history per session
