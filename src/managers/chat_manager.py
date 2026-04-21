# Managers/chat_manager.py
import threading
import queue
import logging
import time
import sounddevice as sd
from src.connections.ollama import chat_stream
from src.managers.sound_manager import play_tts
from src.managers.chat_history import (save_conversation,
                                   add_message,
                                   start_new_conversation)
from src.utils.context import detect_context
from src.utils.toast import show_toast
from src.utils.hardware import cpu_temp_info
from datetime import datetime


# Chat Functions
def send_message(globals, ui_elements):
    """Sends queries to the LLM."""

    # Returns if user send a message within the past 2 seconds
    now = time.time()
    if now - globals.last_message_time <= 2:
        logging.warning(f"Sending messages too fast - must wait 2 seconds.")
        return
    else:
        globals.last_message_time = now


    # Returns if thread count exceeds 6
    active_threads = threading.active_count()
    logging.info(f"Total Active Threads: {active_threads}")
    if active_threads > 6:
        logging.warning(f"Active threads: {active_threads} - sending messages too fast")
        show_toast(globals, message=f"Active threads: {active_threads} - Sending messages too fast!", _type="error")
        return

    # Stops any currently playing audio
    try:
        sd.stop()
        if globals.os_name.startswith("Windows"):
            sd.wait()
        with globals.speaking_lock:
            globals.is_speaking = False
    except Exception as e:
        logging.error(f"Could not stop TTS due to: {e}")

    # Cancels output if stop button is pressed
    if globals.cancel_event:
        globals.cancel_event.set()
        globals.still_streaming = False

    # Prevents sending a message if LLM is currently streaming
    if globals.still_streaming:
        return

    # Sets flag to indicate the LLM is now streaming
    globals.still_streaming = True

    # Create threading event for cancellation
    globals.cancel_event = threading.Event()

    # Create queue
    q = queue.Queue()
    
    # Set active model
    model = globals.active_model

    # Strip whitespace from entry box contents
    clean_text = ui_elements['entrybox'].get("1.0", "end").strip()

    # Append file attachment contents to user text if applicable
    if not clean_text and globals.file_attachment:
        user_text = f"Refer to the following: {globals.file_attachment}"
    elif clean_text and globals.file_attachment:
        user_text = clean_text + f"Refer to the following: {globals.file_attachment}"
    elif clean_text and not globals.file_attachment:
        user_text = clean_text
    else:
        return

    # Set to defaults for new conversations
    if globals.is_new_conversation:
        start_new_conversation(globals)
        globals.context_warning = True

    # Inspect for context if enabled
    if globals.enable_context:
        threading.Thread(target=detect_context,
                         args=(globals, user_text),
                         daemon=True,
                         name="Context Thread").start()

    # Add bubble and delete entry box contents
    ui_elements["add_bubble"]("user", clean_text)
    ui_elements['entrybox'].delete("1.0", "end")

    # Reset file attachment to None
    globals.file_attachment = None

    # Tack on user text and attachment (if applicable) to conversation history
    messages = globals.conversation_history + [{"role": "user",
                                                "content": user_text}]
    
    # Query Ollama in a thread
    threading.Thread(target=chat_stream,
                     args=(globals,
                           model,
                           messages,
                           q,
                           globals.cancel_event),
                           daemon=True,
                           name="Chat Stream").start()

    current_model = globals.active_model
    globals.assistant_label = ui_elements["add_bubble"]("assistant", "", model=current_model)

    # Reset assistant message
    globals.assistant_message = ""

    # Append message to conversation history
    add_message(globals, "user", clean_text)

    # Sets message start time
    globals.message_start_time = datetime.now().isoformat()

    # Re-enables file attachment button
    globals.file_button.configure(state="normal")
    globals.attach_tip.configure(message="Attach")
    globals.file_attachment = None
    globals.attachment_path = None

    # Toggle button to stop mode
    ui_elements["send_button"].configure(text=None,
                                         image=globals.stop_icon,
                                         command=lambda: globals.cancel_event.set()
                                         if globals.cancel_event else None)
    tokens = 0

    def pull_response(user_text):
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
                    
                    # Scrub markdown elements from response (for TTS)
                    for component in globals.markdown_components:
                        globals.assistant_message.replace(component, "")

                    # Health Check
                    if globals.os_name.startswith("Linux"):
                        temp = cpu_temp_info()['cpu_temp_c']
                        if temp >= 100:
                            logging.critical(f"CRITICAL WARNING: CPU TEMP: {temp}C")
                        elif temp >= 90:
                            logging.warning(f"WARNING: CPU temp: {temp}C")
                        else:
                            logging.debug(f"CPU Temp: {temp}C")

                    # TTS
                    play_tts(globals, text=globals.assistant_message)

                    # Add message to conversation history
                    add_message(globals,
                                "assistant",
                                globals.assistant_message,
                                model=globals.active_model,
                                tokens=tokens)
                    
                    # So the stats widget gets token count
                    if globals.widget_rows:
                        last_widget = globals.widget_rows[-1]
                        if last_widget.role == "assistant":
                            last_widget.tokens = tokens
                            last_widget._update_stats()

                    # Only save to file if save_chats is on
                    if globals.save_chats:
                        threading.Thread(target=save_conversation,
                                         args=(globals, user_text),
                                         daemon=True,
                                         name="Save Chats Thread").start()
                    else:
                        globals.is_new_conversation = False

                    # Debug print full conversation history
                    # logging.debug(f"\nFull conversation history:\n{globals.conversation_history}\n")

                    globals.still_streaming = False
                    ui_elements["send_button"].configure(text=None,
                                                         image=globals.send_icon,
                                                         command=lambda: send_message(globals, ui_elements))
                    return

                if globals.current_response_id == local_id:
                    # Scrub markdown while text is streaming
                    globals.assistant_message += item.replace(
                        "***", "").replace(
                            "___", "").replace(
                                "**", "").replace(
                                    "__", "").replace(
                                        "*", "").replace(
                                            "_", "").replace(
                                                "~~", "").replace(
                                                    "#####", "").replace(
                                                        "####", "").replace(
                                                            "###", "")
                    if globals.assistant_label:
                        globals.assistant_label.configure(
                            text=globals.assistant_message)
                    ui_elements["scroll_to_bottom"]()

        except queue.Empty:
            pass

        if globals.current_response_id != local_id:
            globals.still_streaming = False
            return

        globals.root.after(20, lambda: pull_response(user_text))

    pull_response(user_text)
