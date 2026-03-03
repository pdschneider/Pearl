# Changelog

All notable changes to **Pearl** will be located in this file.

## [0.2.3] - 2026-03-03

### Added
- Added interactive install for Docker for Debian and Ubuntu users
- Added interactive install for Kokoro for Linux users
- Added uninstall buttons for Docker (Windows + Linux) and Kokoro (Linux Only)
- Added more granular checks for Linux-based OS's
- Pearl now hashes shell files at startup to ensure updated versions are used
- Logs Python version at startup
- Added language selection (English only for now)

### Changed
- Better widget refreshing to prevent locked up GUI on first setup
- Refined Kokoro voice list to reflect language choice
- Updated README
- Updated Dependencies

### Fixed
- General stability and UI improvements
- Better logging for chat window GUI errors
- Initial logging added for correct CPU temp polling on Windows

## [0.2.2] - 2026-02-28

### Added
- Optional update check, prompts to download most recent version from GitHub if enabled
- Prompts to download default model if not found (optional)
- Added Ollama Uninstall button in Advanced Settings

### Changed
- Defaults to llama3.2:latest if chosen model is not found
- TTS now plays fully in a separate thread, freeing the GUI during chats
- Improved markdown scrubbing from assistant responses
- Updated README

### Fixed
- Fixed major bug where each message was treated as a new conversation when save chats was toggled off
- Fixed broken default TTS on Linux
- Cleaned up logs 

## [0.2.1] - 2026-02-25

### Added
- Added interactive install for Ollama, greatly speeding up initial setup
- Added Docker check on startup, bypassing slow API calls to Kokoro and greatly speeding up application start
- Added disk space check to ensure storage requirements are met
- Added open chats & open config buttons in advanced settings

### Changed
- Improved startup logic for testing connection to Ollama, speeding up application start time
- Improved build instructions in the README
- Updated dependencies
- About page now wrapped in a scrollable frame for better readability

### Fixed
- Initial hardware check now correctly parses L3 cache on Windows and Linux
- GPU checks made more robust, no longer fill logs on failure
- CPU temp check skips on Windows, speeding up application start
- Settings images correctly display only when a feature is available
- Setup page buttons correctly disable when dependencies are already installed
- Fixed major error where essential files didn't copy to their correct location

## [0.2.0] - 2026-02-22

### Added
- Pearl is now compiled to C, greatly improving speed and performance (Linux Only)
- CHANGELOG.md file added to better document changes
- Added startup check to sanitize context detection rules when values are missing or nonconforming

### Changed
- Moved Kokoro test to settings page GUI build to speed up launch
- Improved readability of the in-app changelog page
- Brought much closer to PEP8 compliance
- Updated Dependencies
- Updated README

### Deprecated
- Removed old spec file used for building via Pyinstaller on Linux

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
