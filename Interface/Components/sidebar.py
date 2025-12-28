# Interface/Components/sidebar.py
import customtkinter as ctk
import logging
from Managers.chat_history import load_conversations, load_specific_conversation, start_new_conversation
import sounddevice as sd
from CTkToolTip import CTkToolTip

def create_sidebar(globals):
    """
    Creates the sidebar that slides in from the left.

    Parameters:
        globals: Global variables

    Returns:
        sidebar: The sidebar frame and its child widgets
    """
    sidebar_width = 250
    animation_step = 20
    animation_delay = 10

    # Create the sidebar frame
    sidebar = ctk.CTkFrame(globals.root, width=sidebar_width, corner_radius=0)
    globals.sidebar = sidebar
    globals.sidebar.configure(fg_color=globals.theme_dict["CTk"]["fg_color"])

    # Initially place off-screen
    sidebar.place(x=-sidebar_width, y=0, relheight=1)

    buttons_frame = ctk.CTkFrame(sidebar, width=sidebar_width, corner_radius=0)
    buttons_frame.pack(fill="x")
    buttons_frame.configure(fg_color=globals.theme_dict["CTk"]["fg_color"])

    # Add the hamburger button back so the sidebar can be closed
    sidebar_hamburger = ctk.CTkButton(
        buttons_frame,
        text="☰",
        width=45,
        height=45,
        command=lambda: toggle_sidebar())
    sidebar_hamburger.pack(side="left", padx=10, pady=5)
    CTkToolTip(sidebar_hamburger, message="Collapse Sidebar", delay=1.0, follow=True, padx=10, pady=5)

    # New Chat Button
    sidebar_new_chat = ctk.CTkButton(
        buttons_frame,
        text="✎",
        width=45,
        height=45,
        command=lambda: reset_to_new_chat())
    sidebar_new_chat.pack(side="left", padx=0, pady=5)
    CTkToolTip(sidebar_new_chat, message="New Chat", delay=1.0, follow=True, padx=10, pady=5)

    # Chat History
    title_label = ctk.CTkLabel(
        sidebar,
        text="Chat History",
        font=ctk.CTkFont(size=18, weight="bold"))
    title_label.pack(pady=5, padx=10)

    # Scrollable Frame for Chat History items
    history_frame = ctk.CTkScrollableFrame(sidebar)
    history_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def populate_history():
        """Clears and populates the history frame with chat entries."""
        for widget in history_frame.winfo_children():
            widget.destroy()

        conversations = load_conversations(globals)
        if not conversations:
            no_chats_label = ctk.CTkLabel(history_frame, text="No chats yet!")
            no_chats_label.pack(pady=20, padx=5)
            return

        for convo in conversations:
            metadata = convo["metadata"]
            conv_id = metadata["conversation_id"]
            title = metadata.get("title", "Untitled")
            date_str = metadata.get("created_at", "Unknown")[:10]

            # Create a frame for each chat entry
            entry_frame = ctk.CTkFrame(history_frame, corner_radius=6)
            entry_frame.pack(fill="x", pady=5)

            # Title label
            title_label = ctk.CTkLabel(entry_frame, text=title, anchor="w", justify="left")
            title_label.pack(side="left", expand=True, fill="x")

            # Make the whole frame clickable
            entry_frame.bind("<Button-1>", lambda e, cid=conv_id: load_and_display_chat(cid))
            title_label.bind("<Button-1>", lambda e, cid=conv_id: load_and_display_chat(cid))
    
    def reset_to_new_chat():
        """Resets to a new conversation and clears the chat frame."""
        sd.stop()
        start_new_conversation(globals)

        # Clear the current chat bubbles
        for widget in globals.ui_elements["chat_frame"].winfo_children():
            widget.destroy()
        globals.ui_elements["scroll_to_bottom"]()
        globals.root.update_idletasks()
        toggle_sidebar()
        logging.info(f"Started new chat from sidebar button.")

    def slide_in():
        """Slides the sidebar in after clicking the hamburger button."""
        current_x = sidebar.winfo_x()
        new_x = min(0, current_x + animation_step)
        sidebar.place_configure(x=new_x)
        if new_x < 0:
            sidebar.after(animation_delay, slide_in)
        else:
            globals.sidebar_open = True
            populate_history()

    def slide_out():
        """Slide the sidebar back out when done."""
        current_x = sidebar.winfo_x()
        new_x = max(-sidebar_width, current_x - animation_step)
        sidebar.place_configure(x=new_x)
        if new_x > -sidebar_width:
            sidebar.after(animation_delay, slide_out)
        else:
            globals.sidebar_open = False

    def toggle_sidebar():
        """Calls the sidebar to be slid in or out."""
        logging.debug(f"Sidebar toggle called.")
        sidebar.tkraise()  #  Bring to front
        logging.debug(f"Current sidebar x position: {sidebar.winfo_x()}")
        if globals.sidebar_open:
            logging.debug(f"Closing sidebar.")
            slide_out()
        else:
            logging.debug(f"Opening sidebar.")
            sidebar.place(x=-sidebar_width)
            slide_in()

    def load_and_display_chat(conv_id):
        """Loads the chat and rebuilds the main chat window."""
        sd.stop()
        load_specific_conversation(globals, conv_id)

        # Clear current chat bubbles
        for widget in globals.ui_elements["chat_frame"].winfo_children():
            widget.destroy()
        
        #Add new bubbles from loaded chat
        for msg in globals.chat_history:
            role = msg["role"]
            content = msg["content"]
            globals.ui_elements["add_bubble"](role, content)

        globals.ui_elements["scroll_to_bottom"]()
        globals.root.update_idletasks()

        # Close sidebar after selection
        toggle_sidebar()
        globals.chat_page.tkraise()
        logging.info(f"Displaying conversation: {conv_id}")

    # Override the hamburger button command in top_bar
    if hasattr(globals, 'hamburger'):
        logging.debug(f"Overriding hamburger command.")
        globals.hamburger.configure(command=toggle_sidebar)
    else:
        logging.error(f"No globals.hamburger found.")

    return sidebar
