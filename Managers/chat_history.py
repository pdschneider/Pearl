# Managers/chat_history.py
import json, uuid, logging, os
from datetime import datetime
from config import load_data_path

chat_dir = os.path.normpath(load_data_path("local", "chats"))
try:
    os.makedirs(chat_dir, exist_ok=True)
except Exception as e:
    logging.error(f"Unable to create chats folder due to: {e}")

def start_new_conversation(globals):
    """Reverts variables for a new conversation."""
    globals.conversation_history = []
    globals.chat_history = globals.conversation_history
    globals.conversation_id = str(uuid.uuid4())
    globals.is_new_conversation = True
    globals.created_at = datetime.now().isoformat()
    logging.debug(f"Started new conversation with ID: {globals.conversation_id}")

def add_message(globals, role, content, model=None, tokens=0, **kwargs):
    """Builds each message to save to chat file"""
    message = {"role": role, "content": content, "message_id": str(uuid.uuid4()), **kwargs}
    if message["role"] == "assistant":
        globals.current_response_id = message["message_id"]
        logging.debug(f"Current message ID: {globals.current_response_id}")
    if globals.message_start_time:
        message["start_time"] = globals.message_start_time
    if globals.message_end_time:
        message["end_time"] = globals.message_end_time
    if globals.attachment_path:
        message["attachment"] = globals.attachment_path
    if model:
        message["model"] = model
    if globals.active_prompt and role == "assistant":
        message["prompt"] = globals.active_prompt
    if tokens and tokens != 0:
        message["tokens"] = tokens
    try:
        globals.conversation_history.append(message)
    except Exception as e:
        logging.error(f"Could not write message to chat file due to: {e}")
    
    globals.message_start_time = None
    globals.message_end_time = None

def save_conversation(globals):
    """Saves conversation history each message"""
    if not globals.conversation_history:
        logging.debug("No history to save; skipping.")
        return
    
    if globals.conversation_id is None:
        globals.conversation_id = str(uuid.uuid4())

    filename = os.path.join(chat_dir, f"chat_{globals.conversation_id}.json")
    data = {
        "metadata": {
            "created_at": globals.created_at,
            "title": f"Untitled Chat_{globals.conversation_id}",
            "conversation_id": globals.conversation_id},
        "history": globals.conversation_history}
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Conversation saved/updated to {filename}")
        globals.is_new_conversation = False
    except Exception as e:
        logging.error(f"Failed to save conversation to {filename}: {e}")

def load_conversations(globals):
    """Loads all saved conversations from the chat dir, sorted by created_at descending."""
    conversations = []
    if not os.path.isdir(load_data_path("local", "chats")):
        os.mkdir(load_data_path("local", "chats"))
    chat_dir = os.path.normpath(load_data_path("local", "chats"))
    for filename in os.listdir(chat_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(chat_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    metadata = data.get("metadata", {})
                    history = data.get("history", [])
                    # Generate a better title if "Untitled"
                    if metadata.get("title", "").startswith("Untitled"):
                        preview = "Untitled"
                        # Find first user message for preview
                        for msg in history:
                            if msg["role"] == "user":
                                preview = msg["content"].strip()[:50] + "..." if len(msg["content"]) > 50 else msg["content"]
                                metadata["title"] = preview or "Untitled"
                                break
                        if preview == "Untitled":
                            try:
                                date_obj = datetime.fromisoformat(metadata.get("created_at", ""))
                                preview = date_obj.strftime("%Y-%m-%d %H:%M")
                            except ValueError:
                                preview = filename.replace(".json", "")
                        metadata["title"] = preview
                    conversations.append({
                        "metadata": metadata,
                        "history": history,
                        "filepath": filepath})
            except Exception as e:
                logging.error(f"Failed to load {filename}: {e}")
    # Sort by created_at descending
    conversations.sort(key=lambda c: c["metadata"].get("created_at", ""), reverse=True)
    return conversations

def load_specific_conversation(globals, conversation_id):
    """Loads a specific conversation by ID into globals."""
    chat_dir = os.path.normpath(load_data_path("local", "chats"))
    filename = os.path.join(chat_dir, f"chat_{conversation_id}.json")
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            globals.conversation_id = data["metadata"]["conversation_id"]
            globals.created_at = data["metadata"]["created_at"]
            globals.conversation_history = data["history"]
            globals.chat_history = data["history"]
            globals.is_new_conversation = False
            logging.info(f"Loaded conversation {conversation_id}")
    except Exception as e:
        logging.error(f"Failed to load conversation {conversation_id}: {e}")
