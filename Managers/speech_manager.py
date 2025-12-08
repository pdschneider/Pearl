# Managers/tts.py
import os, pygame, requests, logging, socket, pyttsx3
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from io import BytesIO

# Default TTS
def default_speak(text: str):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# Kokoro
def kokoro_test():
    """Tests Kokoro to set flag for active/inactive."""
    try:
        socket.create_connection(("localhost", 8880), timeout=1).close()
        logging.info(f"Kokokro found!")
        return True
    except Exception as e:
        logging.error(f"Kokoro not installed. TTS features will be unavailable.")
        return False

def fetch_tts_models(globals):
    """loads possible Kokoro models"""
    if globals.kokoro_active:
        try:
                logging.debug(f"Attempting to load Kokoro voice list...")
                voices = requests.get("http://localhost:8880/v1/audio/voices")
                if voices.status_code == 200:
                    logging.info(f"Kokoro voices fetch succeeded. Returning voices dictionary.")
                    return voices.json()["voices"]
                else:
                    logging.error(f"Kokoro voices fetch failed. Status code: {voices.status_code}. Returning empty dictionary.")
                    return {}
        except Exception as e:
            logging.error(f"Failed to load voices due to {e}. Returning empty dictionary.")
            return {}

def kokoro_speak(text, voice):
    """Communicates with the Kokoro endpoint for tts"""
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        response = requests.post("http://localhost:8880/v1/audio/speech", json={
            "model": "kokoro",
            "input": text,
            "voice": voice,
            "response_format": "wav"})
        if response.status_code == 200:
            logging.debug(f"status code: {response.status_code}. Playing TTS.")
            audio_data = BytesIO(response.content)
            sound = pygame.mixer.Sound(audio_data)
            sound.play()
        else:
            logging.error(f"TTS API error: {response.status_code}")
    except Exception as e:
        logging.error(f"TTS error: {e}")
