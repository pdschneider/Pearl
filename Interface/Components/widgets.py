# Interface/Components/widgets.py
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from CTkToolTip import CTkToolTip
import Utils.fonts as fonts
import sounddevice as sd
import logging
from Utils.load_settings import load_data_path
from Managers.sound_manager import kokoro_speak, default_speak


class ButtonWidgets(ctk.CTkFrame):
    """A riny reusable row for buttons underneath message bubbles."""
    def __init__(self,
                 globals,
                 parent,
                 label,
                 copy_callback,
                 model=None,
                 attachment=False,
                 prompt=None,
                 tokens=None,
                 role=None,
                 text=None,
                 message_index=None):
        super().__init__(parent,
                         fg_color=None,
                         bg_color=globals.theme_dict["CTkScrollableFrame"]["fg_color"],
                         border_color=globals.theme_dict["CTkScrollableFrame"]["fg_color"],
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
        self.prompt = prompt or "Unknown"
        self.tokens = tokens or 0
        self.globals = globals
        self.role = role or None
        self.text = text or ""
        self.message_index = message_index or 0

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
        
        self.sound_high_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/sound_high.png")),
            dark_image=Image.open(load_data_path("config", "assets/sound_high.png")),
            size=(10, 10))
        
        self.sound_low_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/sound_low.png")),
            dark_image=Image.open(load_data_path("config", "assets/sound_low.png")),
            size=(10, 10))
        
        self.no_sound_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/no-sound.png")),
            dark_image=Image.open(load_data_path("config", "assets/no-sound.png")),
            size=(10, 10))
        
        self.stats_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/column-chart.png")),
            dark_image=Image.open(load_data_path("config", "assets/column-chart.png")),
            size=(10, 10))

        # Copy Button
        self.copy_button = ctk.CTkButton(self,
                                         image=self.copy_icon,
                                         text=None,
                                         width=26,
                                         height=26,
                                         bg_color="transparent",
                                         corner_radius=8,
                                         font=fonts.widget_font,
                                         command=self._on_copy)
        
        CTkToolTip(self.copy_button,
                   message="Copy",
                   delay=0.6,
                   follow=True,
                   padx=10,
                   pady=5)

        # Attachment Icon
        self.attach_icon_widget = ctk.CTkButton(self,
                                                image=self.attach_icon,
                                                text=None,
                                                width=26,
                                                height=26,
                                                bg_color="transparent",
                                                corner_radius=8)

        CTkToolTip(self.attach_icon_widget,
                   message="File Attached",
                   delay=0.6,
                   follow=True,
                   padx=10,
                   pady=5)
        
        # Sound Button
        self.sound_button = ctk.CTkButton(self,
                                          image=self.sound_high_icon,
                                          text=None,
                                          width=26,
                                          height=26,
                                          bg_color="transparent",
                                          corner_radius=8,
                                          font=fonts.widget_font,
                                          command=self._stop_sound)
        
        CTkToolTip(self.sound_button,
                   message="Stop Sound",
                   delay=0.6,
                   follow=True,
                   padx=10,
                   pady=5)
        
        # Stats Icon
        self.stats_widget = ctk.CTkButton(self,
                                          image=self.stats_icon,
                                          text=None,
                                          width=26,
                                          height=26,
                                          bg_color="transparent",
                                          corner_radius=8,
                                          font=fonts.widget_font,
                                          command=lambda: self._update_stats())

        self.stats_tooltip = CTkToolTip(self.stats_widget,
                   message="Click for Stats...",
                   delay=0.6,
                   follow=True,
                   padx=10,
                   pady=5)

        # Model Label
        self.model_label = ctk.CTkLabel(self,
                                        text=model,
                                        font=fonts.model_font)

    def _on_copy(self):
        """Copies the text from a message bubble."""
        if self.copying:
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

    def _stop_sound(self):
        """Stops sound if playing."""
        logging.debug(f"Stop sound button clicked. Is speaking? {self.globals.is_speaking}")
        try:
            sd.stop()
            with self.globals.speaking_lock:
                self.globals.is_speaking = False
            logging.debug(f"Sound stopped from stop button widget.")
            if False:
                if self.globals.kokoro_active and self.globals.tts_enabled == True and self.globals.tts_source == "Kokoro":
                    kokoro_speak(self.globals)
                elif self.globals.tts_enabled == True and self.globals.tts_source == "Default":
                    default_speak(self.globals, text=self.text)

        except Exception as e:
            logging.error(f"Could not play or stop TTS due to: {e}")

    def _update_stats(self):
        """Pull stats from conversation history and update tooltip"""
        try:
            if self.tokens > 0:
                self.stats_tooltip.configure(message=f"{self.tokens} tokens")
            else:
                self.stats_tooltip.configure(message="No token data yet.")
  
        except Exception as e:
            logging.error(f"Could not update stats tooltip: {e}")

    def show_buttons(self):
        """Shows the widget buttons."""
        if not self.is_shown:
            self.copy_button.grid(row=0, column=0, padx=2, pady=2)
            if self.attachment:
                self.attach_icon_widget.grid(row=0, column=1, padx=2, pady=2)
            if self.role == "assistant":
                self.sound_button.grid(row=0, column=1, padx=2, pady=2)
                self.stats_widget.grid(row=0, column=2, padx=2, pady=2)
            self.model_label.grid(row=0, column=3, padx=2, pady=2)
            self.is_shown = True

    def hide_buttons(self):
        """Hides the widget buttons."""
        if self.is_shown:
            self.copy_button.grid_remove()
            self.attach_icon_widget.grid_remove()
            self.sound_button.grid_remove()
            self.stats_widget.grid_remove()
            self.model_label.grid_remove()
            self.is_shown = False
