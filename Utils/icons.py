# Utils/icons.py
from customtkinter import CTkImage
from PIL import Image
import logging
from Utils.load_settings import load_data_path

def load_icons(globals):
    """Loads icons."""
    try:
        globals.send_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/send.png")),
            dark_image=Image.open(load_data_path("config", "assets/send.png")),
            size=(35, 35))

        globals.stop_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/stop-3.png")),
            dark_image=Image.open(load_data_path("config", "assets/stop-3.png")),
            size=(35, 35))

        globals.attach_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/attach-2.png")),
            dark_image=Image.open(load_data_path("config", "assets/attach-2.png")),
            size=(35, 35))

        globals.sound_high_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/sound_high.png")),
            dark_image=Image.open(load_data_path("config", "assets/sound_high.png")),
            size=(40, 40))

        globals.speaker_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/speaker.png")),
            dark_image=Image.open(load_data_path("config", "assets/speaker.png")),
            size=(40, 40))

        globals.phone_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/phone.png")),
            dark_image=Image.open(load_data_path("config", "assets/phone.png")),
            size=(40, 40))

        globals.chat_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/chat.png")),
            dark_image=Image.open(load_data_path("config", "assets/chat.png")),
            size=(40, 40))

        globals.theme_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/theme.png")),
            dark_image=Image.open(load_data_path("config", "assets/theme.png")),
            size=(40, 40))

        globals.delete_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/cancel.png")),
            dark_image=Image.open(load_data_path("config", "assets/cancel.png")),
            size=(40, 40))

        globals.notification_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/notification-1.png")),
            dark_image=Image.open(load_data_path("config", "assets/notification-1.png")),
            size=(40, 40))

        globals.en_language_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/en-language.png")),
            dark_image=Image.open(load_data_path("config", "assets/en-language.png")),
            size=(40, 40))

        globals.operations_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/operations.png")),
            dark_image=Image.open(load_data_path("config", "assets/operations.png")),
            size=(40, 40))

        globals.title_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/tag.png")),
            dark_image=Image.open(load_data_path("config", "assets/tag.png")),
            size=(40, 40))

        globals.preferences_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/preferences.png")),
            dark_image=Image.open(load_data_path("config", "assets/preferences.png")),
            size=(40, 40))

        globals.note_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/note.png")),
            dark_image=Image.open(load_data_path("config", "assets/note.png")),
            size=(40, 40))

        globals.chats_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/chats.png")),
            dark_image=Image.open(load_data_path("config", "assets/chats.png")),
            size=(40, 40))

        globals.config_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/settings-2.png")),
            dark_image=Image.open(load_data_path("config", "assets/settings-2.png")),
            size=(40, 40))

        globals.ollama_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/ollama.png")),
            dark_image=Image.open(load_data_path("config", "assets/ollama.png")),
            size=(40, 40))

        globals.docker_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/docker.png")),
            dark_image=Image.open(load_data_path("config", "assets/docker.png")),
            size=(40, 40))

        globals.kokoro_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/fastapi.png")),
            dark_image=Image.open(load_data_path("config", "assets/fastapi.png")),
            size=(40, 40))

        globals.pearl_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/Pearl.png")),
            dark_image=Image.open(load_data_path("config", "assets/Pearl.png")),
            size=(40, 40))

        globals.hamburger_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/hamburger.png")),
            dark_image=Image.open(load_data_path("config", "assets/hamburger.png")),
            size=(35, 35))

        globals.settings_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/settings.png")),
            dark_image=Image.open(load_data_path("config", "assets/settings.png")),
            size=(35, 35))

        globals.bug_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/bug-2.png")),
            dark_image=Image.open(load_data_path("config", "assets/bug-2.png")),
            size=(35, 35))

        globals.new_chat_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/pencil.png")),
            dark_image=Image.open(load_data_path("config", "assets/pencil.png")),
            size=(35, 35))

        globals.hamburger_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/hamburger.png")),
            dark_image=Image.open(load_data_path("config", "assets/hamburger.png")),
            size=(35, 35))

        globals.new_chat_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/pencil.png")),
            dark_image=Image.open(load_data_path("config", "assets/pencil.png")),
            size=(35, 35))

    except Exception as e:
        logging.critical(f"Failed to load icons due to: {e}")
