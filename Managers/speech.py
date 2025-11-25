# Managers/tts.py
import json, os, pygame, requests, logging
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from io import BytesIO
from config import Globals

globals = Globals()

def initialize_tts():
    """loads possible Kokoro models"""
    try:
        with open(globals.resource_path(os.path.join(globals.data_dir, 'tts.json'))) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"ERROR: Failed to load tts.json ({e}), returning empty dict")
        return {}

def speak_text(text, voice):
    """Communicates with the Kokoro endpoint for tts"""
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        response = requests.post("http://localhost:8880/v1/audio/speech", json={
            "model": "kokoro",
            "input": text,
            "voice": voice,
            "response_format": "wav"
        })
        if response.status_code == 200:
            audio_data = BytesIO(response.content)
            sound = pygame.mixer.Sound(audio_data)
            sound.play()
        else:
            logging.error(f"TTS API error: {response.status_code}")
    except Exception as e:
        logging.error(f"TTS error: {e}")