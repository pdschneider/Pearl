# Managers/sound_manager.py
import os
import requests
import logging
import threading
import platform
import numpy as np
import wave
import sounddevice as sd
import soundfile as sf
from io import BytesIO
from Utils.load_settings import load_data_path
from Utils.toast import show_toast

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os_name = platform.platform()

if os_name.startswith("Linux"):
    import pulsectl


# Unified Speech
def play_tts(globals, text=None):
    """Plays TTS with the correct voice and source."""

    # Returns if thread count exceeds 6
    active_threads = threading.active_count()
    logging.info(f"Total Active Threads: {active_threads}")
    if active_threads > 6:
        logging.warning(f"Active threads: {active_threads} - sending messages too fast")
        show_toast(globals, message=f"Active threads: {active_threads} - Sending messages too fast!", _type="error")
        return

    # Returns early if TTS is not enabled
    if not globals.tts_enabled:
        return

    # Plays via either Default or Kokoro
    if globals.kokoro_active and globals.tts_source == "Kokoro":
        kokoro_speak(globals, text=text)
    elif globals.tts_source == "Default":
        default_speak(globals, text=text)


# Kokoro
def kokoro_speak(globals, text=None):
    """Communicates with the Kokoro endpoint for tts"""
    try:
        # Defined to play in a separate thread
        def _play_in_thread():
            """Queries Kokoro API and plays TTS in a thread."""

            # Return early if event was cancelled
            if globals.cancel_event and globals.cancel_event.is_set():
                logging.debug(f"TTS cancelled before generation.")
                return

            try:
                response = requests.post(
            "http://localhost:8880/v1/audio/speech", json={
                "model": "kokoro",
                "input": text or globals.assistant_message,
                "voice": globals.kokoro_active_voice,
                "response_format": "wav"})

                # Log API error 500 (removed folder)
                if response.status_code == 500:
                    logging.error(f"TTS API error: {response.status_code}")
                    logging.error(f"Error Details: {response.text}")
                    return

                # Exit early on error
                if response.status_code != 200:
                    logging.error(f"TTS API error: {response.status_code}")
                    return

                # Play TTS if status code is 200
                logging.debug(f"status code: {response.status_code}. Playing TTS.")
                audio_data = BytesIO(response.content)
                data, samplerate = sf.read(audio_data, dtype='float32')

                # Set speakers to play from
                selected_sink = globals.default_sink
                if os_name.startswith("Windows"):
                    device_arg = None
                else:
                    if selected_sink != "Default":
                        os.environ['PULSE_SINK'] = selected_sink
                    else:
                        # Fall back to system default
                        os.environ.pop('PULSE_SINK', None)
                    device_arg = 'pulse'

                # Second Check: Return early if event was cancelled
                if globals.cancel_event and globals.cancel_event.is_set():
                    logging.debug(f"TTS cancelled before playback.")
                    return

                # Set flag and play audio, then stop and reset flag
                with globals.speaking_lock:
                    globals.is_speaking = True
                try:
                    sd.play(data, samplerate, device=device_arg)
                    if globals.os_name.startswith("Windows"):
                        sd.wait()
                except sd.PortAudioError as e:
                    logging.error(f"Playback error: {e}")

                # IMPORTANT: Currently does not wait for audio to finish playing to reset flag

                with globals.speaking_lock:
                    globals.is_speaking = False

            except Exception as e:
                logging.error(f"Playback error: {e}")
                globals.is_speaking = False

        # Start the playback thread
        threading.Thread(target=_play_in_thread, daemon=True).start()
    except Exception as e:
        logging.error(f"TTS error: {e}")
        with globals.speaking_lock:
            globals.is_speaking = False


# Default TTS
def default_speak(globals, text=None):
    """Plays TTS from the computers default TTS source."""
    def _play_in_thread():
        """Plays default TTS in a thread."""

        # Return early if event was cancelled
        if globals.cancel_event and globals.cancel_event.is_set():
            logging.debug(f"TTS cancelled before generation.")
            return

        try:
            # Create path for temporary sound file
            temp_path = os.path.normpath(load_data_path("cache", "temp_tts.wav"))

            # Debug print full voices list
            # logging.debug(f"{get_default_tts_voices(globals)}\n")

            # Set voice
            if globals.default_active_voice:
                globals.engine.setProperty('voice', globals.default_active_voice)

            # Flag is_speaking as true
            with globals.speaking_lock:
                globals.is_speaking = True

            # Save audio to file
            globals.engine.save_to_file(text or globals.assistant_message, temp_path)
            globals.engine.runAndWait()

            # Return if file does not exist
            if not os.path.exists(temp_path):
                logging.warning(f"Default TTS audio file does not exist - can't play.")
                with globals.speaking_lock:
                    globals.is_speaking = False
                globals.engine.stop()
                return

            # Return if sound file is too small
            if os.path.getsize(temp_path) < 10000:
                logging.warning(f"TTS file smaller than 10KB - not large enough to contain audio.")
                with globals.speaking_lock:
                    globals.is_speaking = False
                globals.engine.stop()
                os.remove(temp_path)
                return

            # Debug for audio file data
            if os_name.startswith("Linux"):
                get_audio_info(globals, temp_path)
        except Exception as e:
            logging.error(f"Could not generate audio file due to: {e}")
            globals.engine.stop()
            with globals.speaking_lock:
                globals.is_speaking = False

        try:
            # Load audio file into memory
            with open(temp_path, "rb") as f:
                audio = f.read()

            # Set speakers to play from
            selected_sink = globals.default_sink
            if os_name.startswith("Windows"):
                device_arg = None
            else:
                if selected_sink != "Default":
                    os.environ['PULSE_SINK'] = selected_sink
                else:
                    # Fall back to system default
                    os.environ.pop('PULSE_SINK', None)
                device_arg = 'pulse'

            # Second Check: Return early if event was cancelled
            if globals.cancel_event and globals.cancel_event.is_set():
                logging.debug(f"TTS cancelled before playback.")
                return

            # Set flag
            with globals.speaking_lock:
                globals.is_speaking = True

            # Play audio from file in memory
            audio_data = BytesIO(audio)
            data, samplerate = sf.read(audio_data, dtype='float32')
            try:
                sd.play(data, samplerate, device=device_arg)
                if globals.os_name.startswith("Windows"):
                    sd.wait()
            except sd.PortAudioError as e:
                logging.error(f"Playback error: {e}")
            
            # IMPORTANT: Currently does not wait for audio to finish playing to reset flag

            # Clean up the audio file
            if os.path.exists(temp_path):
                os.remove(temp_path)

            # Stop TTS queue and set flag
            globals.engine.stop()
            with globals.speaking_lock:
                globals.is_speaking = False

        except Exception as e:
            logging.error(f"Could not read : {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            with globals.speaking_lock:
                globals.is_speaking = False
    
    try:
        threading.Thread(target=_play_in_thread, daemon=True).start()
    except Exception as e:
        logging.error(f"Could not play default TTS due to: {e}")
        globals.is_speaking = False


def get_audio_info(globals, path):
    """Logs detailed info about audio being played."""
    logging.debug(f"Playing Voice: {globals.engine.getProperty('voice')}")

    # WAV check
    try:
        with wave.open(path, 'rb') as wf:
            logging.debug(f"Channels: {wf.getnchannels()}")
            logging.debug(f"Sample width: {wf.getsampwidth()}")
            logging.debug(f"Frame rate: {wf.getframerate()}")
            logging.debug(f"Frames: {wf.getnframes()}  → Duration: {wf.getnframes() / wf.getframerate():.2f} sec")

        with wave.open(path, 'rb') as wf:
            raw_data = wf.readframes(wf.getnframes())
        audio_array = np.frombuffer(raw_data, dtype=np.int16)
        logging.debug(f"Max amplitude: {np.max(np.abs(audio_array))}")
        logging.debug(f"Mean amplitude: {np.mean(np.abs(audio_array))}")
    except wave.Error as e:
        logging.debug(f"WAV read error: {e}")
    except Exception as e:
        logging.debug(f"Could not find audio file info due to: {e}")


def get_default_tts_voices(globals):
    """Returns a list of default tts voices."""
    voice_dict = {}
    try:
        # Get voice list
        voices = globals.engine.getProperty('voices')

        # Creates dictionary linking readable names to IDs
        logging.debug("Available voices:")
        for voice in voices:
            if str(voice.languages[0]).startswith("en"):
                voice_dict[str(voice.name)] = str(voice.id)
    except Exception as e:
        logging.error(f"Could not return available default voices due to: {e}")

    # Return complete dictionary
    return voice_dict


# Query for speaker outputs (Linux only)
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
