# Managers/chat_manager.py
import threading, queue, logging
import sounddevice as sd
from Connections.ollama import chat_stream
from Managers.sound_manager import kokoro_speak, default_speak
from Managers.chat_history import save_conversation, add_message, start_new_conversation
from Utils.context import detect_context
from datetime import datetime

# Chat Functions
def send_message(globals, ui_elements, event=None):
    """Sends queries to the LLM."""
    # Stops any currently playing audio
    sd.stop()

    # Prevents sending a message if LLM is currently streaming
    if globals.still_streaming:
        return

    # Sets flag to indicate the LLM is now streaming
    globals.still_streaming = True

    if globals.cancel_event:
        globals.cancel_event.set()
    
    globals.cancel_event = threading.Event()
    
    q = queue.Queue()
    model = globals.active_model
    clean_text = ui_elements['entrybox'].get("1.0", "end").strip()

    if not clean_text and globals.file_attachment:
        user_text = f"Refer to the following: {globals.file_attachment}"
    elif clean_text and globals.file_attachment:
        user_text = clean_text + f"Refer to the following: {globals.file_attachment}"
    elif clean_text and not globals.file_attachment:
        user_text = clean_text
    else:
        return

    if globals.is_new_conversation:
        globals.active_prompt = "Assistant"
        start_new_conversation(globals)

    # inspect for context
    detect_context(globals, user_text)

    ui_elements["add_bubble"]("user", clean_text)
    ui_elements['entrybox'].delete("1.0", "end")

    messages = globals.conversation_history + [{"role": "user", "content": user_text}]
    threading.Thread(target=chat_stream, args=(globals, model, messages, q, globals.cancel_event), daemon=True, name="Chat Stream").start()

    current_model = globals.active_model
    globals.assistant_label = ui_elements["add_bubble"]("assistant", "", model=current_model)
    globals.assistant_message = ""

    if globals.save_chats:
        add_message(globals, "user", clean_text)

    globals.message_start_time = datetime.now().isoformat()

    # Re-enables file attachment button
    globals.file_button.configure(state="normal")
    globals.attach_tip.configure(message="Attach")
    globals.file_attachment = None
    globals.attachment_path = None

    # Toggle button to stop mode
    ui_elements["send_button"].configure(text="■", command=lambda: globals.cancel_event.set() if globals.cancel_event else None)
    tokens = 0

    def pull_response():
        """Pulls the response from Ollama via the thread-safe queue"""
        nonlocal tokens
        local_id = globals.current_response_id
        try:
            while True:
                item = q.get_nowait()
                tokens += 1
                if item is None:
                    if globals.current_response_id != local_id:
                        logging.debug(f"Discarding stale response (ID {local_id})")
                        globals.still_streaming = False
                        return
                    # TTS
                    globals.assistant_message = globals.assistant_message.replace("***", "").replace("___", "").replace("**", "").replace("__", "").replace("*", "").replace("_", "").replace("~~", "")
                    if globals.kokoro_active and globals.tts_enabled == True and globals.tts_source == "Kokoro":
                        kokoro_speak(globals)
                    elif globals.tts_enabled == True and globals.tts_source == "Default":
                        default_speak(globals.assistant_message)
                    # Save
                    if globals.save_chats:
                        add_message(globals, "assistant", globals.assistant_message, model=globals.active_model, tokens=tokens)
                    save_conversation(globals)
                    globals.still_streaming = False
                    ui_elements["send_button"].configure(text="➤", command=lambda: send_message(globals, ui_elements))
                    return

                if globals.current_response_id == local_id:
                    globals.assistant_message += item.replace("***", "").replace("___", "").replace("**", "").replace("__", "").replace("*", "").replace("_", "").replace("~~", "")
                    if globals.assistant_label:
                        globals.assistant_label.configure(text=globals.assistant_message)
                    ui_elements["scroll_to_bottom"]()

        except queue.Empty:
            pass

        if globals.current_response_id != local_id:
            globals.still_streaming = False
            return

        globals.root.after(20, pull_response)

    pull_response()
