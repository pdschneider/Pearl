# Changelog

All notable changes to **Pearl** will be located in this file.

## [0.3.4] - 2026-00-00

Pearl now ships as a .deb for Linux! For the first time, Linux users can benefit from full desktop integration just like on Windows: pinning Pearl to the dock, seeing the app in the start menu, and a proper uninstall button. This update also adds support for 31 new file types including .docx.

### Added
- Pearl is now packaged as a .deb file on Linux in addition to AppImage!
- Supports the following file types: .eml, .zig, .nim, .erl, .ex, .exs, .sol, .vue, .svelte, .tf, .tfvars, .f, .f90, .asm, .s, .cmake, .gradle, .m, .mm, .vimrc, .inputrc, .npmrc, .nvmrc, .yarnrc, .eslintrc, .prettierrc, .babelrc, .pylintrc, .flake8, .gemrc, .docx

### Changed
- Doubled maximum character length for file uploads
- Rewrote chat logic to work with PySide6 when the new GUI framework is ready

### Fixed
- Fixed bug preventing chats from being deleted
- Added missing copyright to Windows setup file metadata
- Fixed broken Beta update channel

## [0.3.3] - 2026-04-21

This update enhances context detection by adding 12 new prompts and improving back-end logic. Maximum context length is also now used by default, enabling much longer chats before Pearl begins to forget older parts of the conversation. Pearl now also supports 39 new file types, supports thinking models, and includes an optional beta release channel!

### Added
- Added 12 new prompts
- Pearl now uses maximum context length by default, enabling much longer conversations
- Added token count checks with warnings if conversation exceeds maximum length
- Thinking models are now supported
- Added new documentation for listing supported file types
- Added beta release channel
- Pearl now supports the following file types as attachments: .repo, .htm, .java, .xhtml, .scss, .sass, .less, .vbs, .asp, .ipynb, .editorconfig, .htaccess, .dockerignore, .bashrc, .bash_aliases, .bash_history, .lynxrc, .bash_logout, .gitconfig, .python_history, .profile, .taskrc, .selected_editor, .steampid, .sweeprc, .sweeptimes, .update-timestamp, .wget-hsts, .windows-serial, .xinputrc, .xsession-errors, .zshrc, .lesshst, .desktop, .pid, .directory, .adm, .admx, .adml

### Changed
- Added restart prompt when saving settings which require app restart to apply
- Added startup hash check for prompts file
- Pearl now closes much faster when exiting the app
- Improved context detection logic
- Various UI improvements

### Fixed
- Fixed major bug preventing system prompt from changing via context detection
- File attachments which exceed maximum tokens for the active model are now rejected

## [0.3.2] - 2026-04-13

This update features an officially recognized certificate for Windows users, increasing compatibility with Windows Defender. It also features simple installer scripts for Docker and Kokoro so Windows users can benefit from enhanced TTS without the hassle of complex setup, along with various bug fixes and documentation additions.

### Added
- Added documentation: Architecture, Build Instructions, Roadmap, Usage
- Improved context detection via adding more keywords
- Added Debian folder structure for future .deb builds
- Added default model download script for Windows users when no model is available but Ollama is running
- Pearl on Windows is now signed with an officially recognized code signing certificate
- Added simple Docker and Kokoro installation for Windows users

### Changed
- Reorganized project structure
- Updated Dependencies
- Updated ReadMe

### Fixed
- Fixed crash when trying to report a bug
- Fixed various crashes resulting from QT-based message boxes
- General stability & UI improvements

### Security
- Patched moderate level cryptography vulnerability which allowed buffer overflow attacks in certain scenarios

## [0.3.1] - 2026-03-29

This update features a hotfix for Windows users who had trouble getting past Windows Defender false positives, along with general back-end and organizational improvements to speed up build time.

### Added
- Added metadata to Windows build
- Added .gitignore file + helper script for faster builds

### Changed
- Reorganized scripts for clarity: icons.py, version.py, vars.py
- Improved RAM check when loading models
- Updated Dependencies

### Fixed
- Fixed critical error where the model selector crashed the UI on startup for some users
- Fixed build issue where pdfplumber's dependency chain was breaking requirements.txt
- Pearl is now built with Pyinstaller again on Windows, sacrificing speed but improving compatibility with Windows Defender

## [0.3.0] - 2026-03-17

Pearl now has networking capabilities! You can now utilize multiple devices for context detection, title generation, & chats so long as they are compatible with Ollama. Context detection logic and speed have also greatly improved and pdf files are now supported. Pearl is now also fully integrated into the desktop environment for Windows users!

### Added
- Networking: users can now utilize multiple devices for chats, title generation, & context detection
- Pearl is now fully integrated into the desktop environment for Windows users
- Context detection toggle now available in settings
- Pearl now generates chat titles
- Chat title generation toggle available in settings
- Added optional wizard to about settings
- Added bug report button in about settings
- .pdf files are now supported in file attachments

### Changed
- Greatly improved context detection logic and keywords
- Context detection now runs in a separate thread, improving chat speed
- Converted all convertable message boxes to PySide6
- Updated About page
- Updated Dependencies
- Updated ReadME

### Fixed
- Added dependency check and installer script for Linux systems missing libxb-cursor0
- Fixed major bug where Linux systems without Kokoro installed would crash
- Toasts now correctly display when selecting models
- General stability improvements

## [0.2.5] - 2026-03-13

This update adds new buttons to assistant messages, giving more control over TTS output and helpful information, along with an improved updater and partial re-write in the much more modern GUI framework PySide6. This is the beginning of a slow transition to the new framework.

### Added
- Added button underneath assistant messages to stop ongoing TTS
- Added stats button under assistant messages which shows token count
- appimage.xml better integrates AppImage into Linux desktop environments
- Windows build is now signed with a self-signed certificate

### Changed
- Updater now brings you directly to the correct download, not the generic new release page
- Switched updater from outdated tkinter framework to modern PySide6
- Updater now shows latest release notes so users can see what's new before downloading
- Updated file attachment box to PySide6, greatly improving UX, especially for Linux users
- Updated Dependencies

### Fixed
- Selecting a conversation from the sidebar now switches to the chat page
- Creating a new chat now correctly scrolls to the top of the chat frame
- Pearl now checks thread count and aborts excessive actions to increase stability
- Fixed bug stopping models from being unloaded via the model settings tab
- Pearl now correctly shuts down logging and both roots on exit
- General stability improvements

## [0.2.4] - 2026-03-07

This update focuses on overall speed, bug fixes, and stability improvements relating to file attachments and context detection (among others) as well as expanding accepted filetypes for attachments and improving default TTS behavior.

### Added
- Pearl is now pre-compiled to C on Windows (in addition to Linux), greatly improving speed for all users
- Roughly tripled the number of accepted filetypes for attachments: .rst, .adoc, .tex, .org, .conf, .js, .sql, .go, .rs, .php, .cpp, .c, .h, .cs, .kt, .swift, .dart, .ts, .tsx, .jsx, .rb, .pl, .lua, .scala, .hs, .jl, .yml, .env, .r, .text, .asc, .properties, .m3u, ,.lst, .list, .gitignore, .gitattributes
- Greatly improved default TTS functionality:
    - Now works with speaker selection on Linux
    - Audio stops playing when program shuts down
    - Follows same pattern as Kokoro where entering a new message cuts off previous TTS
- Added icon for Windows users

### Changed
- Switched theme and context checks to more effective hashing method, ensuring proper values
- Improved code organization for certain features
- Made Kokoro voice options easier to read
- Updated build instructions in ReadME
- Updated Dependencies

### Fixed
- Fixed bug where pressing enter too many times in a row would disable sending messages
- Improved chat behavior logic for enter press
- Impoved stability for context detection and file attachments
- Window now draws widgets before displaying, reducing UI errors
- New chat button now maps to the chat page as users would expect
- Eliminated unnecessary chat history rebuilds, improving speed
- Sidebar now populates chat history on startup, reducing loading time on first click
- General UI and stability improvements

## [0.2.3] - 2026-03-03

This update focuses on improving Pearl in all the ways user feedback suggests. I've added an interactive install for both Docker and Kokoro for Linux users, making Kokoro TTS simple to get working. I also added uninstall buttons for both Docker and Kokoro and a factory reset button for deleting all Pearl-related data. In addition, Pearl features greater stability, responsiveness, general bug fixes, and improved logging.

### Added
- Added interactive install for Docker for Debian and Ubuntu users
- Added interactive install for Kokoro for Linux users
- Added uninstall buttons for Docker (Windows + Linux) and Kokoro (Linux Only)
- Added factory reset button for all Pearl data
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
- Initial debug logging added for CPU temp polling on Windows

## [0.2.2] - 2026-02-28

Pearl can now check for new updates on startup, making downloading the most recent version much easier. An uninstall button was also added for Ollama and overall responsiveness, stability, and speed have been improved.

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

Pearl now has an interactive install for Ollama making first time user setup much simpler. Speed and stability have also greatly improved.

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

VERSION 0.2 IS HERE! This time around, Pearl is pre-compiled to C on Linux systems, greatly improving speed and performance. Documentation has been improved by adding dedicated changelog and readme files and stability is greatly improved with startup checks to sanitize corrupted or nonconforming settings.

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

This update features the ability to delete chats, report bugs, and various UI and stability improvements!

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

Pearl now dynamically determines the context of the conversation and adjusts tone on the fly! Other minor updates include an improved sidebar, better logging per message, and handy buttons for github and logs.

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

Pearl now supports file attachments as well as a new chat button, tooltips, and improved stability!

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

Chat history is finally here along with an audio output selection on Linux!

### Added
- Functional chat history introduced
- Added audio output selection (Linux Only)

### Changed
- Minor bug fixes and improvements

## [0.1.8] - 2025-12-08

Pearl now ships as an AppImage for Linux users, improving compatibility across distros, plus a sidebar for an upcoming chat history feature, a changelog page, and general stability improvements.

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

This update finishes the GUI overhaul with a total redesign of the main chat page. However, markdown support is lost.

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

This version features a near-total overhaul of the interface to a more modern framework, plus three new themes.

### Added
- Converted entire GUI to Custom Tkinter
- Added 3 new themes

### Changed
- Major UI overhaul
- Improved folder path detection on Windows systems
- Minor bug fixes and improvements

## [0.1.5] - 2025-12-02

This version includes an optional save chats toggle for future implementation and a more responsive UI.

### Added
- Added threading for more responsive UI during chats
- Added initial greeting
- Added model and hardware checks for later implementation
- Optional save chats toggle

## [0.1.4] - 2025-11-30

This update adds built-in cross-platform TTS as well as hardware checks for better debugging.

### Added
- Added universal cross-platform default TTS
- Queries CPU/RAM/GPU data for logging & error handling

### Changed
- UI improvements
- General error handling improvements

## [0.1.3] - 2025-11-29

This version adds markdown support, improves TTS output, and updates fonts.

### Added
- Added support for markdown italics, bold, and strike-through
- Improved TTS by removing italics, bold, and strike-through markdown from speech

### Changed
- Updated fonts for Windows users
- Removed unused query_ollama function, reducing code size

## [0.1.2] - 2025-11-28

This update greatly improves Test to Speech by including Kokoro-FastAPI support and improves launch speed.

### Added
- Added TTS with dozens of voices (requires Kokoro)
- Added dynamic settings updates

### Changed
- Skips initial Ollama API requests when Ollama is not found, speeding up initial load for systems without Ollama

### Fixed
- Suppressed extra requests debug messages, reducing log spam

## [0.1.1] - 2025-11-27

This update adds Windows support and a handy onboarding page for new users, plus log files and a dependencies list for devs.

### Added
- Added requirements.txt with dependencies for easier builds
- Added rotating log files
- Added setup instructions for users without Ollama installed
- Added Windows 10/11 Support

### Changed
- Improved error handling

## [0.1.0] - 2025-11-25

Welcome to Pearl's initial release! To kick it off, we have a functional AI chat, two themes to choose from, a place to view, select, load, and unload downloaded models, and persistent chat history!

### Added
- AI chat window
- Cosmic Sky & Pastel Green themes
- View models list & differ between loaded/not loaded to memory
- Load, unload, select specific models
- Persistent chat history per session
