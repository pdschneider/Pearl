
# ⚪ Pearl Roadmap

This document outlines the vision, planned features, and development priorities for **Pearl**.

It is a living document and will be updated periodically. Some features may not be included in Pearl and other features not listed may be added.

## 🎯 Project Vision

Pearl is an AI chat app designed to be fully private and yours. The goal of this project is to make local AI useful and accessible.

## 📅 Current Status (April 2026)

- **Version**: 0.3.x (Stable release available)
- **Core Features**: Private AI chats, file uploads, networking capabilities and multiple TTS options
- **Platforms**: Linux (Ubuntu/Debian recommended) & Windows 10/11

## 🗺️ Planned Milestones

The roadmap for Pearl is vast with several planned features prior to the official 1.0 release. Each minor release follows a general theme and is always subject to change. 

## 0.3.x - Networking & Models

Updates in the 0.3.x series focus on networking capabilities and model management. The focus of this series of updates is to give users more control over the models they use, provide additional information about each for clarity, and enhance and simplify the entire experience.

### Major Improvements
- [ ] A dedicated **models** page with multiple selection screens
- [ ] Built in **download and removal** for models directly in the app
- [ ] Clear details view so users can see what each model offers
- [ ] Smart automatic model selection based on hardware
- [ ] Guided model downloading with recommendations

### Other Improvements
- [ ] Expand documentation with updated README, Build instructions, Roadmap, Architecture, and Usage
- [ ] Faster and more streamlined in-app Pearl updates
- [ ] Support individual chat deletion
- [ ] Improve sidebar loading speeds by limiting the loading of previous chats at once
- [x] Fully integrate Pearl into the Windows desktop environment
- [x] Switch outdated messageboxes to new GUI framework
- [x] Improve context detection with additional keywords

## 0.4.x - Personalization

This update cycle focuses on user control over the personalization of Pearl. Users will be able to select Pearl's interests, add a profile picture and more. Pearl will also introduce a memories feature, allowing her to remember details across different chats.

### Major Improvements
- [ ] Feature a Personalization page in settings
- [ ] Incorporate user-selected interests for Pearl
- [ ] Add general prompt settings to guide behavior (short/detailed, formal/informal, etc.)
- [ ] Add custom profile picture option to personalization
- [ ] Add advanced fine-tuning options
- [ ] Feature a memories system to retain important details across chats
- [ ] Add edit button underneath user messages
- [ ] Add Thumbs Up & Down Personalization Buttons under assistant messages + Pearl Points
- [ ] Add regenerate button to assistant messages

### Other Improvements
- [ ] Expand the list of available prompts
- [ ] Improve the speed and accuracy of context detection via fine-tuning LLM options
- [ ] Add checks for conversation token length
- [ ] Attach prompt to assistant messages

## 0.5.x - Image Support

The image support update cycle will focus on adding support for images as file attachments as well as add more accepted filetypes in general.

### Major Improvements
- [ ] Add basic support for image files
- [ ] Add dedicated vision model to summarize images and attach summaries to queries

### Other Improvements
- [ ] Add support for more image types
- [ ] Add support for .docx/.odf files

## 0.6.x - Speech to Text

This update cycle focuses on adding speech to text in order to talk to Pearl with voice.

- [ ] Add basic Speech to Text ability
- [ ] Add microphone selection
- [ ] Add Vosk STT
- [ ] Add dedicated call mode
- [ ] Waveform visual representation of audio while speaking

## 0.7.x - Knowledge Base

This update lets you point to folders allowing Pearl to intelligently access information without per-conversation file uploads.

- [ ] Add the ability to point to folders so Pearl can dynamically search from pre-selected files

## 0.8.x - Web Search

This update focuses on adding web search capabilities to Pearl for up-to-date information.

- [ ] Add compatibility with Brave Search

## 0.9.x - Commands

This update cycle features in conversation commands so Pearl can take actions mid-conversation. This feature could potentially integrate into calendar, to-do lists, budgets, and more.

- [ ] Add commands that allow Pearl to perform functions via input ("Hey Pearl, make me a to-do list!)

## 0.10.x - Polish / Pre-Major Release

This is the final update cycle before the official release of version 1.0.0. The focus here is on adding features which don't fit into any previous update cycle and refining code / fixing bugs prior to the first major release.

### Major Improvements
- [ ] Set specific times to send messages
- [ ] Search bar for chat history

### Other Improvements
- [ ] Add dynamic Pearl profile picture switching for different prompts
- [ ] Keyboard shortcuts
- [ ] Clean up any bugs prior to GUI rewrite

## 1.0.x - Rewrite in PySide

Versions in the 1.0.x series will feature a full GUI refresh in a much more modern GUI framework. The goal of updates in this cycle is to make Pearl look and feel like a professional app.

- [ ] Rewrite entire GUI in PySide, modernizing the app

## Technical Additions & General Improvements

Features:
- [ ] Add Spanish support
- [ ] Import/export chats
- [ ] Add new chat page
- [ ] Add support for more TTS
- [ ] Support .deb builds for Linux users

Setup Page:
- [ ] Improve install/uninstall scripts
- [ ] Turn setup page into wizard with check marks for dependencies and general settings toggles, multi-page

TTS:
- [ ] Add default TTS voice selection to Linux/Windows
- [ ] Add replay feature to sound button under assistant messages

Logging:
- [ ] Attach CPU temp to assistant messages (average + max) - Linux only
- [ ] Attach tokens per second to assistant messages
- [ ] Add estimated token count for user messages
- [ ] Logs total conversation tokens for checks (you've hit max context!)
- [ ] Attach total response time to assistant messages & info button
- [ ] Add checks to warn the user when CPU temp gets above 90C
- [ ] Auto stop generating text and warn user if temperature exceeds 110C

Settings:
- [x] Add Context Detection options to settings

Misc:
- [ ] Build loading window with PySide6
- [ ] Add tooltips to every sensible widget
- [ ] Make clicking settings retract sidebar
- [ ] Improve accessability features

Windows Specific:
- [ ] Add support for CPU temp polling on Windows
- [ ] Fix default tts silently failing after first message
- [ ] Add audio output selection for Windows
- [ ] Add Kokoro voice selection for Windows
- [ ] Add proper install / uninstall scripts for Docker/Kokoro on Windows

## 📝 Notes

- Priorities may shift based on user feedback and bug reports.
- Feature requests are welcome — please open a GitHub issue.
- This roadmap focuses primarily on **user-facing** improvements. Technical debt and refactoring happen continuously.

**Maintained by** Phillip Schneider
