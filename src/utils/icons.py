# src/utils/icons.py
from customtkinter import CTkImage
from PIL import Image
import logging
from src.utils.load import load_data_path
from PySide6.QtGui import QIcon


def load_icons(globs):
    """Loads icons."""
    try:
        globs.send_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/send.png")),
            dark_image=Image.open(load_data_path("config", "assets/send.png")),
            size=(40, 40))

        globs.stop_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/stop-3.png")),
            dark_image=Image.open(load_data_path("config", "assets/stop-3.png")),
            size=(40, 40))

        globs.attach_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/add-1.png")),
            dark_image=Image.open(load_data_path("config", "assets/add-1.png")),
            size=(40, 40))

        globs.sound_high_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/sound_high.png")),
            dark_image=Image.open(load_data_path("config", "assets/sound_high.png")),
            size=(40, 40))

        globs.speaker_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/speaker.png")),
            dark_image=Image.open(load_data_path("config", "assets/speaker.png")),
            size=(40, 40))

        globs.phone_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/phone.png")),
            dark_image=Image.open(load_data_path("config", "assets/phone.png")),
            size=(40, 40))

        globs.chat_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/chat.png")),
            dark_image=Image.open(load_data_path("config", "assets/chat.png")),
            size=(40, 40))

        globs.theme_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/theme.png")),
            dark_image=Image.open(load_data_path("config", "assets/theme.png")),
            size=(40, 40))

        globs.delete_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/cancel.png")),
            dark_image=Image.open(load_data_path("config", "assets/cancel.png")),
            size=(40, 40))

        globs.notification_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/notification-1.png")),
            dark_image=Image.open(load_data_path("config", "assets/notification-1.png")),
            size=(40, 40))

        globs.en_language_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/en-language.png")),
            dark_image=Image.open(load_data_path("config", "assets/en-language.png")),
            size=(40, 40))

        globs.operations_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/operations.png")),
            dark_image=Image.open(load_data_path("config", "assets/operations.png")),
            size=(40, 40))

        globs.title_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/tag.png")),
            dark_image=Image.open(load_data_path("config", "assets/tag.png")),
            size=(40, 40))

        globs.preferences_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/preferences.png")),
            dark_image=Image.open(load_data_path("config", "assets/preferences.png")),
            size=(40, 40))

        globs.note_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/note.png")),
            dark_image=Image.open(load_data_path("config", "assets/note.png")),
            size=(40, 40))

        globs.chats_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/chats.png")),
            dark_image=Image.open(load_data_path("config", "assets/chats.png")),
            size=(40, 40))

        globs.config_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/settings-2.png")),
            dark_image=Image.open(load_data_path("config", "assets/settings-2.png")),
            size=(40, 40))

        globs.ollama_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/ollama.png")),
            dark_image=Image.open(load_data_path("config", "assets/ollama.png")),
            size=(40, 40))

        globs.docker_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/docker.png")),
            dark_image=Image.open(load_data_path("config", "assets/docker.png")),
            size=(40, 40))

        globs.kokoro_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/fastapi.png")),
            dark_image=Image.open(load_data_path("config", "assets/fastapi.png")),
            size=(40, 40))

        globs.pearl_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/Pearl.png")),
            dark_image=Image.open(load_data_path("config", "assets/Pearl.png")),
            size=(40, 40))

        globs.hamburger_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/hamburger.png")),
            dark_image=Image.open(load_data_path("config", "assets/hamburger.png")),
            size=(35, 35))

        globs.settings_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/settings.png")),
            dark_image=Image.open(load_data_path("config", "assets/settings.png")),
            size=(35, 35))

        globs.bug_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/bug-2.png")),
            dark_image=Image.open(load_data_path("config", "assets/bug-2.png")),
            size=(35, 35))

        globs.new_chat_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/pencil.png")),
            dark_image=Image.open(load_data_path("config", "assets/pencil.png")),
            size=(35, 35))

        globs.hamburger_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/hamburger.png")),
            dark_image=Image.open(load_data_path("config", "assets/hamburger.png")),
            size=(35, 35))

        globs.new_chat_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/pencil.png")),
            dark_image=Image.open(load_data_path("config", "assets/pencil.png")),
            size=(35, 35))
        
        globs.windows_icon = CTkImage(
            light_image=Image.open(load_data_path("config", "assets/window-size.png")),
            dark_image=Image.open(load_data_path("config", "assets/window-size.png")),
            size=(40, 40))

    except Exception as e:
        logging.critical(f"Failed to load icons due to: {e}")


def load_qt_icons(globs):
    """Loads QT icons."""
    try:
        if globs.os_name.startswith("Linux"):
            globs.github_icon = QIcon(load_data_path("config", "assets/github.svg"))
            globs.github_light_icon = QIcon(load_data_path("config", "assets/github-light.svg"))
            globs.codeberg_icon = QIcon(load_data_path("config", "assets/codeberg.svg"))
        else:
            globs.github_icon = QIcon(load_data_path("config", "assets/github.png"))
            globs.github_light_icon = QIcon(load_data_path("config", "assets/github-light.png"))
            globs.codeberg_icon = QIcon(load_data_path("config", "assets/codeberg.png"))

        globs.mail_icon = QIcon(load_data_path("config", "assets/mail.png"))

    except Exception as e:
        logging.error(f"Failed to load icons due to: {e}")
