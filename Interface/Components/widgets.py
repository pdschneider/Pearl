# Interface/Components/widgets.py
import customtkinter as ctk
import Utils.fonts as fonts

class ButtonWidgets(ctk.CTkFrame):
    """A riny reusable row for buttons underneath message bubbles."""
    def __init__(self, globals, parent, label, copy_callback):
        super().__init__(parent, 
                         fg_color=None, 
                         bg_color=globals.theme_dict["CTkScrollableFrame"]["bg_color"],
                         border_color=globals.theme_dict["CTkScrollableFrame"]["bg_color"],
                         border_width=0,
                         corner_radius=0,
                         height=30,
                         width=40)
        
        self.label = label
        self.copy_callback = copy_callback
        self.is_shown = False
        self.copying = False

        # Copy button
        self.copy_button = ctk.CTkButton(self,
                                         text="📋",
                                         width=25,
                                         height=26,
                                         bg_color="transparent",
                                         corner_radius=8,
                                         font=fonts.widget_font,
                                         command=self._on_copy)
        self.copy_button.pack(anchor="w", pady=2)
        self.copy_button.pack_forget()

    def _on_copy(self):
        """Copies the text from a message bubble."""
        if self.copying == True:
            return
        self.copy_callback(self.label)

        # Visual feedback
        original_text = self.copy_button.cget("text")
        self.copying = True
        self.copy_button.configure(text="✓")

        def reset_button():
            self.copy_button.configure(text=original_text)
            self.copying = False

        self.after(1500, reset_button)

    def show_buttons(self):
        """Shows the widget buttons."""
        if not self.is_shown:
            self.copy_button.pack(anchor="w", pady=2)
            self.is_shown = True
            self.after(600, lambda: self.copy_button.pack_forget())
            self.is_shown = False

    def hide_buttons(self):
        """Hides the widget buttons."""
        if self.is_shown:
            self.after(600, lambda: self.copy_button.pack_forget())
            self.is_shown = False

