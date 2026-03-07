# Utils/refresher.py
from Connections.ollama import ollama_version_test, ollama_test
from Connections.docker import docker_check, docker_version_check
from Connections.kokoro import kokoro_test
import logging
import threading


def refresh_gui(globals):
    """Refreshes GUI when dependencies are active or inactive."""
    def _refresh_in_thread(globals):
        """Does health check & GUI refresh in a thread to speed up app."""
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
            globals.ollama_interactive_download_button.configure(state="disabled")
            globals.ollama_web_download_button.configure(state="disabled")
        else:
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
            if "Kokoro" not in globals.source_options:
                globals.source_options.append("Kokoro")
        else:
            if globals.os_name.startswith("Linux"):
                globals.kokoro_interactive_download_button.configure(state="normal")
            globals.kokoro_web_download_button.configure(state="normal")
            globals.tts_source_var.set("Default")
            if "Kokoro" in globals.source_options:
                globals.source_options.remove("Kokoro")

    # Refresh in thread
    threading.Thread(target=lambda: _refresh_in_thread(globals), daemon=True).start()
