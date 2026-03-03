# Utils/refresher.py
from Connections.ollama import ollama_version_test, ollama_test
from Connections.docker import docker_check, docker_version_check
from Managers.sound_manager import kokoro_test
import logging


def refresh_gui(globals):
    """Refreshes GUI when dependencies are active or inactive."""
    # Test Ollama
    ollama_version_test(globals)
    if globals.ollama_version:
        ollama_test(globals)

    # Test docker & Kokoro
    docker_version_check(globals)
    if globals.docker_version:
        docker_check(globals)
        if globals.docker_active:
            kokoro_test(globals)

    logging.debug(
        f"Health Check: Ollama: {globals.ollama_active} | Docker: {globals.docker_active} | Kokoro: {globals.kokoro_active}")

    # Configure UI widgets for Ollama
    if globals.ollama_active:
        globals.entry_box.configure(state="normal")
        globals.send_button.configure(state="normal")
        globals.ollama_interactive_download_button.configure(state="disabled")
        globals.ollama_web_download_button.configure(state="disabled")
    else:
        globals.entry_box.configure(state="disabled")
        globals.send_button.configure(state="disabled")
        if globals.os_name.startswith("Linux"):
            globals.ollama_interactive_download_button.configure(state="normal")
        globals.ollama_web_download_button.configure(state="normal")

    # Configure UI widgets for Docker
    if globals.docker_active:
        if globals.os_name.startswith("Linux"):
            globals.docker_interactive_download_button.configure(state="disabled")
        globals.docker_web_download_button.configure(state="disabled")
    else:
        if globals.os_name.startswith("Linux"):
            globals.docker_interactive_download_button.configure(state="normal")
        globals.docker_web_download_button.configure(state="normal")

    # Configure UI widgets for Kokoro
    if globals.kokoro_active:
        if globals.os_name.startswith("Linux"):
            globals.kokoro_interactive_download_button.configure(state="disabled")
        globals.kokoro_web_download_button.configure(state="disabled")
        if globals.tts_source_var.get() == "Kokoro" and globals.os_name.startswith("Linux"):
            globals.speakers_frame.tkraise()
        if "Kokoro" not in globals.source_options:
            globals.source_options.append("Kokoro")
    else:
        if globals.os_name.startswith("Linux"):
            globals.kokoro_interactive_download_button.configure(state="normal")
        globals.kokoro_web_download_button.configure(state="normal")
        globals.tts_source_var.set("Default")
        if globals.os_name.startswith("Linux"):
            globals.speakers_frame.lower()
        if "Kokoro" in globals.source_options:
            globals.source_options.remove("Kokoro")
