# Interface/Components/sidebar.py
import customtkinter as ctk
import logging

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

    # Initially place off-screen
    sidebar.place(x=-sidebar_width, y=0, relheight=1)

    # Add the hamburger button back so the sidebar can be closed
    sidebar_hamburger = ctk.CTkButton(
        sidebar,
        text="☰",
        width=45,
        height=45,
        command=lambda: toggle_sidebar())
    sidebar_hamburger.pack(padx=10, pady=5)

    # Chat History
    title_label = ctk.CTkLabel(
        sidebar,
        text="Chat History",
        font=ctk.CTkFont(size=18, weight="bold"))
    title_label.pack(pady=20, padx=10)

    # Placeholder for Chat History items
    history_frame = ctk.CTkScrollableFrame(sidebar)
    history_frame.pack(fill="both", expand=True, padx=10, pady=10)

    coming_soon_label = ctk.CTkLabel(
        history_frame,
        text="Coming soon!")
    coming_soon_label.pack(pady=20, padx=5)

    def slide_in():
        """Slides the sidebar in after clicking the hamburger button."""
        current_x = sidebar.winfo_x()
        new_x = min(0, current_x + animation_step)
        sidebar.place_configure(x=new_x)
        if new_x < 0:
            sidebar.after(animation_delay, slide_in)
        else:
            globals.sidebar_open = True

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

    # Override the hamburger button command in top_bar
    if hasattr(globals, 'hamburger'):
        logging.debug(f"Overriding hamburger command.")
        globals.hamburger.configure(command=toggle_sidebar)
    else:
        logging.error(f"No globals.hamburger found.")

    return sidebar
