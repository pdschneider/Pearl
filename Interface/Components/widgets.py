# Interface/Components/widgets.py
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from CTkToolTip import CTkToolTip
import Utils.fonts as fonts
from Utils.load_settings import load_data_path

class ButtonWidgets(ctk.CTkFrame):
    """A riny reusable row for buttons underneath message bubbles."""
    def __init__(self, globals, parent, label, copy_callback, model=None, attachment=False):
        super().__init__(parent, 
                         fg_color=None, 
                         bg_color=globals.theme_dict["CTkScrollableFrame"]["bg_color"],
                         border_color=globals.theme_dict["CTkScrollableFrame"]["bg_color"],
                         border_width=0,
                         corner_radius=0,
                         height=32,
                         width=40)
        
        self.label = label
        self.copy_callback = copy_callback
        self.is_shown = False
        self.copying = False
        self.model = model or "Unknown"
        self.attachment = attachment or None

        # Get Icons
        self.copy_icon = CTkImage(
        light_image=Image.open(load_data_path("config", "assets/copy.png")),
        dark_image=Image.open(load_data_path("config", "assets/copy.png")),
        size=(10, 10))

        self.check_icon = CTkImage(
        light_image=Image.open(load_data_path("config", "assets/check-1.png")),
        dark_image=Image.open(load_data_path("config", "assets/check-1.png")),
        size=(10, 10))

        self.attach_icon = CTkImage(
        light_image=Image.open(load_data_path("config", "assets/attach-2.png")),
        dark_image=Image.open(load_data_path("config", "assets/attach-2.png")),
        size=(10, 10))

        # Copy button
        self.copy_button = ctk.CTkButton(self,
                                         image=self.copy_icon,
                                         text=None,
                                         width=26,
                                         height=26,
                                         bg_color="transparent",
                                         corner_radius=8,
                                         font=fonts.widget_font,
                                         command=self._on_copy)
        
        # Attachment icon for messages with attachments
        self.attach_icon_widget = ctk.CTkButton(self, 
                                                image=self.attach_icon, 
                                                text=None,
                                                width=26,
                                                height=26,
                                                bg_color="transparent",
                                                corner_radius=8)
        CTkToolTip(self.attach_icon_widget, message="File Attached", delay=0.6, follow=True, padx=10, pady=5)

        # Model label
        self.model_label = ctk.CTkLabel(self, text=model, font=fonts.model_font)

    def _on_copy(self):
        """Copies the text from a message bubble."""
        if self.copying == True:
            return
        self.copy_callback(self.label)

        # Visual feedback
        original_image = self.copy_icon
        self.copying = True
        self.copy_button.configure(image=self.check_icon)

        def reset_button():
            self.copy_button.configure(image=original_image)
            self.copying = False

        self.after(1500, reset_button)

    def show_buttons(self):
        """Shows the widget buttons."""
        if not self.is_shown:
            self.copy_button.grid(row=0, column=0, padx=2, pady=2)
            if self.attachment:
                self.attach_icon_widget.grid(row=0, column=1, padx=2, pady=2)
            self.model_label.grid(row=0, column=2, padx=2, pady=2)
            self.is_shown = True
            self.after(600, lambda: self.copy_button.grid_forget())
            self.after(600, lambda: self.attach_icon_widget.grid_forget())
            self.after(600, lambda: self.model_label.grid_forget())
            self.is_shown = False

    def hide_buttons(self):
        """Hides the widget buttons."""
        if self.is_shown:
            self.after(600, lambda: self.copy_button.grid_forget())
            self.after(600, lambda: self.attach_icon_widget.grid_forget())
            self.after(600, lambda: self.model_label.grid_forget())
            self.is_shown = False
