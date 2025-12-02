# Managers/chat_history.py
import json, uuid, logging, os
from datetime import datetime
from config import get_data_path

conversation_history = []
conversation_id = str(uuid.uuid4())
is_new_conversation = True
created_at = datetime.now().isoformat()
chat_dir = os.path.normpath(get_data_path("local", "chats"))
try:
    os.makedirs(chat_dir, exist_ok=True)
except Exception as e:
    logging.error(f"Unable to create chats folder due to: {e}")

def add_message(role, content, combo=None, **kwargs):
    """Builds each message to save to chat file"""
    message = {"role": role, "content": content, "message_id": str(uuid.uuid4()), **kwargs}
    if combo:
        message["combo"] = combo
    try:
        conversation_history.append(message)
    except Exception as e:
        logging.error(f"Could not write message to chat file due to: {e}")

def save_conversation():
    """Saves conversation history each message"""
    if not conversation_history:
        return
    filename = os.path.join(chat_dir, f"chat_{conversation_id}.json")
    data = {
        "metadata": {
            "created_at": created_at,
            "title": f"Untitled Chat_{conversation_id}",
            "conversation_id": conversation_id
        },
        "history": conversation_history
    }
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Conversation saved/updated to {filename}")
    except Exception as e:
        logging.error(f"Failed to save conversation to {filename}: {e}")