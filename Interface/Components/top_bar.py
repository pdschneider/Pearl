# Interface/Components/top_bar.py
import customtkinter as ctk
import CTkToolTip as ctktt
from tktooltip import ToolTip

def create_top_bar(globals):
    # Main top bar
    top_bar = ctk.CTkFrame(globals.root, height=55, corner_radius=0)
    globals.top_bar = top_bar
    top_bar.pack(side="top", fill="x")
    top_bar.pack_propagate(False)

    # Hamburger button (left)
    hamburger = ctk.CTkButton(
        top_bar,
        text="☰",
        width=45,
        height=45,
        command=lambda: print("Chat history coming soon!"))
    hamburger.pack(side="left", padx=10, pady=5)
    ToolTip(hamburger, msg="Chat History Coming Soon!", delay=0.3, follow=True, fg="white", bg="gray20", padx=10, pady=5)

    # Title / App name (center)
    title = ctk.CTkLabel(
        top_bar,
        text="Pearl at your service!",
        font=ctk.CTkFont(size=20, weight="bold"))
    title.pack(side="left", expand=True)

    # Settings gear (right)
    settings = ctk.CTkButton(
        top_bar,
        text="⚙",
        width=45,
        height=45,
        command=lambda: print("later"))
    settings.pack(side="right", padx=10, pady=5)
    settings.configure(command=lambda: (globals.main_frame.pack_forget() if globals.main_frame.winfo_ismapped() else globals.main_frame.pack(fill="both", expand=True, padx=10, pady=10), globals.settings_overlay.pack(fill="both", expand=True, padx=10, pady=10) if not globals.settings_overlay.winfo_ismapped() else globals.settings_overlay.pack_forget(), globals.settings_overlay.tkraise()))

    return top_bar
