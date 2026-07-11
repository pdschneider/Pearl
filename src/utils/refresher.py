# Utils/refresher.py
from src.connections.ollama import ollama_version_test, ollama_test
from src.connections.docker import docker_check, docker_version_check
from src.connections.kokoro import kokoro_test
import logging
import threading


def refresh_gui(globs):
    """Refreshes GUI when dependencies are active or inactive."""
    def _refresh_in_thread(globs):
        """Does health check & GUI refresh in a thread to speed up app."""
        # Test Ollama
        ollama_version_test(globs)
        if globs.ollama_version:
            ollama_test(globs)

        # Test docker & Kokoro
        docker_version_check(globs)
        if globs.docker_version:
            docker_check(globs)
            if globs.docker_active:
                kokoro_test(globs)

        logging.debug(
            f"Health Check: Ollama: {globs.ollama_active} | Docker: {globs.docker_active} | Kokoro: {globs.kokoro_active}")

        # Configure UI widgets for Ollama
        if globs.ollama_active:
            globs.ollama_interactive_download_button.configure(state="disabled")
            globs.ollama_web_download_button.configure(state="disabled")
        else:
            if globs.os_name.startswith("Linux"):
                globs.ollama_interactive_download_button.configure(state="normal")
            globs.ollama_web_download_button.configure(state="normal")

        # Configure UI widgets for Docker
        if globs.docker_active:
            if globs.os_name.startswith("Linux"):
                globs.docker_interactive_download_button.configure(state="disabled")
            globs.docker_web_download_button.configure(state="disabled")
        else:
            if globs.os_name.startswith("Linux"):
                globs.docker_interactive_download_button.configure(state="normal")
            globs.docker_web_download_button.configure(state="normal")

        # Configure UI widgets for Kokoro
        if globs.kokoro_active:
            if globs.os_name.startswith("Linux"):
                globs.kokoro_interactive_download_button.configure(state="disabled")
            globs.kokoro_web_download_button.configure(state="disabled")
            if "Kokoro" not in globs.source_options:
                globs.source_options.append("Kokoro")
        else:
            if globs.os_name.startswith("Linux"):
                globs.kokoro_interactive_download_button.configure(state="normal")
            globs.kokoro_web_download_button.configure(state="normal")
            globs.tts_source_var.set("Default")
            if "Kokoro" in globs.source_options:
                globs.source_options.remove("Kokoro")

    # Refresh in thread
    threading.Thread(target=lambda: _refresh_in_thread(globs), daemon=True).start()
