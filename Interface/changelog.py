# Interface/changelog.py
import customtkinter as ctk
import Utils.fonts as fonts

def create_changelog_tab(globals, changelog_tab):
    """
    Creates the tab to display setup instructions for new users.

            Parameters:
                    globals: Global variables
                    setup_tab: The main frame of the setup window
    """
    ctk.CTkLabel(changelog_tab, 
                text="Changelog",
                font=fonts.title_font,
                anchor="center").pack(fill="x", pady=20, padx=10)

    changelog_frame = ctk.CTkScrollableFrame(changelog_tab)
    changelog_frame.pack(fill="both", expand=True, padx=10, pady=0)

    # Main Changelog Sections

    # v0.1.9
    ctk.CTkLabel(changelog_frame,
                 text="v0.1.9",
                 font=fonts.heading_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)
    
    ctk.CTkLabel(changelog_frame,
                 justify="left",
                 anchor="center",
                 wraplength=400,
                 text="- Functional chat history introduced\n" \
                        "- Added audio output selection (Linux Only)\n" \
                        "- Minor bug fixes and improvements").pack(fill="both", expand=True, padx=10, pady=10)

    # v0.1.8
    ctk.CTkLabel(changelog_frame,
                 text="v0.1.8",
                 font=fonts.heading_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)
    
    ctk.CTkLabel(changelog_frame,
                 justify="left",
                 anchor="center",
                 wraplength=400,
                 text="- Ships as AppImage for Linux users\n" \
                        "- Added progress bar for slow startup scenarios\n" \
                        "- Added program icon\n" \
                        "- Added sidebar for later chat history implementation\n" \
                        "- Added changelog page\n" \
                        "- Moved startup logic to new script\n" \
                        "- Added context detection logging\n" \
                        "- Minor bug fixes and improvements").pack(fill="both", expand=True, padx=10, pady=10)

    # v0.1.7
    ctk.CTkLabel(changelog_frame,
                 text="v0.1.7",
                 font=fonts.heading_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)
    
    ctk.CTkLabel(changelog_frame,
                 justify="left",
                 anchor="center",
                 wraplength=400,
                 text="- Total overhaul of main chat UI\n" \
                        "- Total overhaul of setup page\n" \
                        "- Added about page\n" \
                        "- Minor bug fixes and improvements\n" \
                        "- Brought closer to PEP8 compliance\n\n" \
                        "- Downgraded: Lost markdown text").pack(fill="both", expand=True, padx=10, pady=10)

    # v0.1.6
    ctk.CTkLabel(changelog_frame,
                 text="v0.1.6",
                 font=fonts.heading_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)
    
    ctk.CTkLabel(changelog_frame,
                 justify="left",
                 anchor="center",
                 wraplength=400,
                 text="- Major UI overhaul\n" \
                        "- Converted entire GUI to Custom Tkinter\n" \
                        "- Added 3 new themes\n" \
                        "- Improved folder path detection on Windows systems\n" \
                        "- Improved logging").pack(fill="both", expand=True, padx=10, pady=10)

    # v0.1.5
    ctk.CTkLabel(changelog_frame,
                 text="v0.1.5",
                 font=fonts.heading_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)
    
    ctk.CTkLabel(changelog_frame,
                 justify="left",
                 anchor="center",
                 wraplength=400,
                 text="- Added threading for more responsive UI during chats\n" \
                        "- Added initial greeting\n" \
                        "- Added model and hardware checks for later implementation\n" \
                        "- Optional save chats toggle").pack(fill="both", expand=True, padx=10, pady=10)

    # v0.1.4
    ctk.CTkLabel(changelog_frame,
                 text="v0.1.4",
                 font=fonts.heading_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)
    
    ctk.CTkLabel(changelog_frame,
                 justify="left",
                 anchor="center",
                 wraplength=400,
                 text="- Added universal cross-platform default TTS\n" \
                        "- UI improvements\n" \
                        "- Queries and logs CPU/RAM/GPU data for logging & error handling\n" \
                        "- General error handling improvements").pack(fill="both", expand=True, padx=10, pady=10)

    # v0.1.3
    ctk.CTkLabel(changelog_frame,
                 text="v0.1.3",
                 font=fonts.heading_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)
    
    ctk.CTkLabel(changelog_frame,
                 justify="left",
                 anchor="center",
                 wraplength=400,
                 text="- Updated fonts for Windows users\n" \
                        "- Removed unused query_ollama function\n" \
                        "- Added support for markdown italics, bold, and strikethrough\n" \
                        "- Improved TTS by removing italics, bold, and strikethrough markdown from speech").pack(fill="both", expand=True, padx=10, pady=10)

    # v0.1.2
    ctk.CTkLabel(changelog_frame,
                 text="v0.1.2",
                 font=fonts.heading_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)
    
    ctk.CTkLabel(changelog_frame,
                 justify="left",
                 anchor="center",
                 wraplength=400,
                 text="- Skips initial Ollama API requests when Ollama is not found.\n" \
                        "- Added TTS (requires Kokoro)\n" \
                        "- Suppressed requests debug log messages\n" \
                        "- Added dynamic settings updates").pack(fill="both", expand=True, padx=10, pady=10)

    # v0.1.1
    ctk.CTkLabel(changelog_frame,
                 text="v0.1.1",
                 font=fonts.heading_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)
    
    ctk.CTkLabel(changelog_frame,
                 justify="left",
                 anchor="center",
                 wraplength=400,
                 text="- Added requirements.txt\n" \
                        "- Added rotating log files\n" \
                        "- Improved error handling\n" \
                        "- Added setup instructions for users without Ollama installed").pack(fill="both", expand=True, padx=10, pady=10)

    # v0.1.0
    ctk.CTkLabel(changelog_frame,
                 text="v0.1.0",
                 font=fonts.heading_font,
                 anchor="center").pack(fill="x", pady=20, padx=10)
    
    ctk.CTkLabel(changelog_frame,
                 justify="left",
                 anchor="center",
                 wraplength=400,
                 text="- Created wireframe\n" \
                        "- Added Cosmic Sky theme\n" \
                        "- Added Pastel Green theme\n" \
                        "- Ollama functions for model fetching, unloading, and chat\n" \
                        "- Budget script for later implementation\n" \
                        "- TTS script for later implementation\n" \
                        "- Hardware checking script for later implementation\n" \
                        "- Chat page, models page, and settings page\n" \
                        "- Context script for later implementation\n" \
                        "- Added models list treeview\n" \
                        "- Added load and unload buttons to models treeview\n" \
                        "- Added logging\n" \
                        "- Added docstrings to most functions\n" \
                        "- Added logging level setting\n" \
                        "- Corrected file paths for Windows or Linux\n" \
                        "- Added load/unload models buttons\n" \
                        "- Added button for selecting active model\n" \
                        "- Added persistent chat history\n" \
                        "- Added changelog").pack(fill="both", expand=True, padx=10, pady=10)

    # Buttons Frame
    buttons_frame = ctk.CTkFrame(changelog_tab, fg_color="transparent")
    buttons_frame.pack(fill="x", padx=10, pady=10)

    ctk.CTkButton(buttons_frame, 
                text="Back", 
                command= lambda: continue_to_chat()).pack(padx=5, pady=5)

    def continue_to_chat():
        """Forgets setup and settings pages to return the user to a clean chat page"""
        globals.settings_overlay.pack_forget()
        globals.changelog.pack_forget()
        globals.chat_page.pack(fill="both", expand=True, padx=10, pady=0)

