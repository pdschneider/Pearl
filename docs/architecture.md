
# 🏗️ Pearl Architecture

This document provides a high-level overview of Pearl's codebase and design decisions. It is intended for developers who want to understand how the application is structured.

## Overview

Pearl is a fully local, privacy-focused AI chat desktop application built with Python. It features a graphical user interface using **Custom Tkinter** with certain elements built with **PySide6**, integrates with local LLMs via Ollama, supports multiple text-to-speech engines, and file uploads.

The application is designed to be:
- **Fully offline-first** — no user data leaves the local machine by default after setup
- **Cross-platform** — Windows and Linux (with Android support considered for the future)
- **Easy to build and distribute** — using Nuitka (Linux) and PyInstaller + Inno Setup (Windows)
- **Modular** — to allow future extensibility (new models, TTS backends, prompt styles, etc.)

## Core Components

### 1. GUI Layer (Custom Tkinter + PySide6)
- Main window and primary interface
- Chat view, sidebar (chat history), input area
- Settings page with multiple sub-pages, plus onboarding page
- Message boxes and file selection boxes built with PySide6

### 2. Backend / Core Logic
- Chat management and conversation history
- Prompt switching and context handling
- File attachment logic
- Setup scripts for onboarding (installs for Ollama, Docker + Kokoro)

### 3. AI Integration
- Ollama client wrapper + kokoro TTS wrapper
- Model discovery, download, and metadata handling
- Response streaming and processing

### 4. TTS (Text-to-Speech)
- Multiple TTS backends (pyttsx3 + Kokoro)
- Future STT support (Vosk, etc.)

### 5. Data & Persistence
- `defaults/` directory for configuration and assets
- Chat history storage
- User preferences and personalization data

## Folder Structure

```Bash
Pearl/
├── pearl.py                  # Main entry point - launches the GUI
├── config.py                 # Configuration and settings handling
├── version.py                # Version information
├── defaults/                 # Default prompts, assets, icons, and configuration files
├── Interface/                # All GUI-related code
│   ├── Components/           # Reusable  UI components
│   ├── Settings/             # Settings pages
│   └── Setup/                # Initial setup wizard and onboarding screen
├── Managers/                 # Core business logic managers
├── Connections/              # Integration with network-related code (ollama, kokoro, github, docker)
├── Utils/                    # Utility functions, helpers, and shared tools
├── data/                     # Development mode data storage
├── packaging/                # Build configurations, spec files, AppImage resources, Inno Setup scripts
├── docs/                     # Documentation files (ARCHITECTURE.md, USAGE.md, etc.)
├── CHANGELOG.md
├── LICENSE.txt
└── README.md
```

## Key Design Decisions

- **Separation of Concerns**: GUI code is kept separate from core logic where possible.
- **Privacy First**: All processing happens locally. No telemetry or cloud services are used by default.
- **Modularity**: TTS, LLM backend, and storage are designed to support multiple implementations.
- **Why PySide6**: Chosen for better styling, performance, and modern Qt features compared to the current Custom Tkinter implementation.
- **Build Strategy**: One-file executables for easy distribution while maintaining reasonable binary size.

## Data Flow (Simplified)

1. User types message or uploads file
2. Prompt builder combines message + conversation history + file contents + prompt
3. Request sent to Ollama backend
4. Response is processed, displayed, and optionally spoken via TTS
5. Conversation is saved to local storage (optional)

## Extensibility Points

- Adding new LLM backends (beyond Ollama)
- Adding new TTS/STT engines
- Creating additional prompt templates or "roles"
- Remembering elements of past chats
- Supporting new file types for attachments

## Future Considerations

- Improved testing
- Performance optimizations for large context windows

---

## Folder Structure (deb - inside packaging/)

``` bash
deb/
├── DEBIAN
├── etc
│   └── pearl
└── usr
    ├── bin
    ├── lib
    │   └── pearl
    └── share
        ├── applications
        ├── doc
        │   └── pearl
        ├── icons
        │   └── hicolor
        │       ├── 128x128
        │       │   └── apps
        │       ├── 256x256
        │       │   └── apps
        │       └── scalable
        ├── pearl
        ├── man
        │   └── man1
        ├── metainfo
        └── pixmaps

```

---

## Important Variables

### Flags
- globals.ollama_active: Tells whether Ollama is currently installed and active
- globals.docker_active: Tells whether Docker is currently installed and active
- globals.kokoro_active: Tells whether Kokoro is currently installed and active

---

**Maintained by**: Phillip Schneider

If you notice outdated information, please open a GitHub issue.
