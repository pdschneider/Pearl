# Managers/sound_manager.py
import os
import requests
import logging
import socket
import pyttsx3
import threading
import platform
import sounddevice as sd
import soundfile as sf
from io import BytesIO

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os_name = platform.platform()

if os_name.startswith("Linux"):
    import pulsectl


# Kokoro
def kokoro_test():
    """Tests Kokoro to set flag for active/inactive."""
    try:
        socket.create_connection(("localhost", 8880), timeout=1).close()
        logging.info(f"Kokokro found!")
        return True
    except Exception as e:
        logging.error(
            f"Kokoro not installed. TTS features will be unavailable.")
        return False


def fetch_tts_models(globals):
    """loads possible Kokoro models"""
    if globals.kokoro_active:
        try:
                logging.debug(f"Attempting to load Kokoro voice list...")
                voices = requests.get("http://localhost:8880/v1/audio/voices")
                if voices.status_code == 200:
                    return voices.json()["voices"]
                else:
                    logging.error(
                        f"Kokoro voices fetch failed. Status code: {voices.status_code}. Returning empty dictionary.")
                    return {}
        except Exception as e:
            logging.error(
                f"Failed to load voices due to {e}. Returning empty dictionary.")
            return {}


def kokoro_speak(globals):
    """Communicates with the Kokoro endpoint for tts"""
    try:
        # Defined to play in a separate thread
        def _play_in_thread():
            """Queries Kokoro API and plays TTS in a thread."""
            try:
                response = requests.post(
            "http://localhost:8880/v1/audio/speech", json={
                "model": "kokoro",
                "input": globals.assistant_message,
                "voice": globals.active_voice,
                "response_format": "wav"})
                if response.status_code != 200:
                    logging.error(f"TTS API error: {response.status_code}")
                    return  # Early exit on error
                logging.debug(f"status code: {response.status_code}. Playing TTS.")
                audio_data = BytesIO(response.content)
                data, samplerate = sf.read(audio_data, dtype='float32')

                selected_sink = globals.default_sink
                if selected_sink != "Default":
                    os.environ['PULSE_SINK'] = selected_sink
                else:
                    # Fall back to system default
                    os.environ.pop('PULSE_SINK', None)

                # Set flag and play audio
                globals.is_speaking = True
                sd.play(data, samplerate, device='pulse')
                globals.is_speaking = False
            except Exception as e:
                logging.error(f"Playback error: {e}")
                globals.is_speaking = False

        # Start the playback thread
        threading.Thread(target=_play_in_thread, daemon=True).start()
    except Exception as e:
        logging.error(f"TTS error: {e}")
        globals.is_speaking = False


# Default TTS
def default_speak(globals, text):
    """Plays TTS from the computers default TTS source."""
    def _play_in_thread():
        """Plays default TTS in a thread."""
        try:
            globals.is_speaking = True
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            globals.is_speaking = False
        except Exception as e:
            logging.error(f"Could not play TTS via default due to: {e}")
            globals.is_speaking = False
    
    try:
        threading.Thread(target=_play_in_thread, daemon=True).start()
    except Exception as e:
        logging.error(f"Could not play default TTS due to: {e}")


# Query for speaker outputs
def get_sink_menu():
    """
    Returns a list of dicts:
        {
            "label":   human readable name for the UI,
            "pulse_name": exact name Pulse/
            PipeWire uses (can be passed to sounddevice)
        }
    """
    menu = [{"label": "Default", "pulse_name": "Default"}]

    if os_name.startswith("Linux"):
        with pulsectl.Pulse('sink-menu') as pulse:
            for sink in pulse.sink_list():
                # Skip monitor loopbacks
                if "monitor" in (sink.description or "").lower():
                    continue

                label = sink.description or sink.name
                menu.append({"label": label, "pulse_name": sink.name})

        return menu
    else:
        return "Default"
