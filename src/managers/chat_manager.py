# src/managers/chat_manager.py
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
from src.utils.tts_scrub import scrub_for_tts
from datetime import datetime
from PySide6.QtCore import QTimer


# Chat Functions
def send_message(globs, ui_elements):
    """Sends queries to the LLM."""

    # Returns if user send a message within the past 2 seconds
    now = time.time()
    if now - globs.last_message_time <= 2:
        logging.warning(f"Sending messages too fast - must wait 2 seconds.")
        return
    else:
        globs.last_message_time = now


    # Returns if thread count exceeds 6
    active_threads = threading.active_count()
    logging.info(f"Total Active Threads: {active_threads}")
    if active_threads > 6:
        logging.warning(f"Active threads: {active_threads} - sending messages too fast")
        show_toast(globs, message=f"Active threads: {active_threads} - Sending messages too fast!", _type="error")
        return

    # Stops any currently playing audio
    try:
        sd.stop()
        if globs.os_name.startswith("Windows"):
            sd.wait()
        with globs.speaking_lock:
            globs.is_speaking = False
    except Exception as e:
        logging.error(f"Could not stop TTS due to: {e}")

    # Cancels output if stop button is pressed
    if globs.cancel_event:
        globs.cancel_event.set()
        globs.still_streaming = False

    # Prevents sending a message if LLM is currently streaming
    if globs.still_streaming:
        return

    # Sets flag to indicate the LLM is now streaming
    globs.still_streaming = True

    # Create threading event for cancellation
    globs.cancel_event = threading.Event()

    # Create queue
    q = queue.Queue()
    
    # Set active model
    model = globs.active_model

    # Strip whitespace from entry box contents
    if not globs.legacy_mode:
        clean_text = globs.input_box.toPlainText().strip()
    else:
        clean_text = globs.input_box.get("1.0", "end").strip()

    # Append file attachment contents to user text if applicable
    if not clean_text and globs.file_attachment:
        user_text = f"Describe to the following: {globs.file_attachment}"
    elif clean_text and globs.file_attachment:
        user_text = clean_text + f" Refer to the following: {globs.file_attachment}"
    elif clean_text and not globs.file_attachment:
        user_text = clean_text
    else:
        return

    # Set to defaults for new conversations
    if globs.is_new_conversation:
        start_new_conversation(globs)
        globs.context_warning = True

    # Inspect for context if enabled
    if globs.enable_context:
        threading.Thread(target=detect_context,
                         args=(globs, user_text),
                         daemon=True,
                         name="Context Thread").start()

    # Add bubble
    ui_elements["add_bubble"](globs, role="user", text=clean_text)

    # Delete entry box contents
    if not globs.legacy_mode:
        globs.input_box.clear()
    else:
        globs.input_box.delete("1.0", "end")

    # Reset file attachment to None
    globs.file_attachment = None

    # Tack on user text and attachment (if applicable) to conversation history
    if not globs.image_attachment:
        messages = globs.conversation_history + [{"role": "user",
                                                    "content": user_text}]
    else:
        messages = globs.conversation_history + [{"role": "user",
                                                    "content": user_text,
                                                    "images": [globs.image_attachment]}]
    
    # Query Ollama in a thread
    threading.Thread(target=chat_stream,
                     args=(globs,
                           model,
                           messages,
                           q,
                           globs.cancel_event),
                           daemon=True,
                           name="Chat Stream").start()

    current_model = globs.active_model
    globs.assistant_label = ui_elements["add_bubble"](globs, role="assistant", text="", model=current_model)

    # Reset assistant message
    globs.assistant_message = ""

    # Append message to conversation history
    add_message(globs, "user", clean_text)

    # Sets message start time
    globs.message_start_time = datetime.now().isoformat()

    # Re-enables file attachment button
    if not globs.legacy_mode:
        pass
    else:
        globs.file_button.configure(state="normal")
        globs.attach_tip.configure(message="Attach")
    globs.file_attachment = None
    globs.attachment_path = None

    # Toggle button to stop mode
    if globs.legacy_mode:
        globs.send_button.configure(
            text=None,
            image=globs.stop_icon,
            command=lambda: globs.cancel_event.set()
            if globs.cancel_event else None)
    else:
        globs.send_button.setText("■")
        globs.send_button.setVisible(True)
    tokens = 0

    def pull_response(user_text):
        """Pulls the response from Ollama via the thread-safe queue"""
        nonlocal tokens
        local_id = globs.current_response_id
        try:
            while True:
                item = q.get_nowait()
                tokens += 1
                if item is None:
                    if globs.current_response_id != local_id:
                        logging.debug(f"Discarding stale response (ID {local_id})")
                        globs.still_streaming = False
                        return

                    # Health Check
                    if globs.os_name.startswith("Linux"):
                        temp = cpu_temp_info()['cpu_temp_c']
                        if temp >= 100:
                            logging.critical(f"CRITICAL WARNING: CPU TEMP: {temp}C")
                        elif temp >= 90:
                            logging.warning(f"WARNING: CPU temp: {temp}C")
                        else:
                            logging.debug(f"CPU Temp: {temp}C")

                    # Final clean markdown render
                    if globs.assistant_label and not globs.legacy_mode:
                        globs.assistant_label.setMarkdown(globs.assistant_message)

                    # TTS
                    play_tts(globs, text=scrub_for_tts(globs.assistant_message))

                    # Add message to conversation history
                    add_message(globs,
                                "assistant",
                                globs.assistant_message,
                                model=globs.active_model,
                                tokens=tokens)
                    
                    # So the stats widget gets token count
                    if globs.widget_rows:
                        last_widget = globs.widget_rows[-1]
                        if last_widget.role == "assistant":
                            last_widget.tokens = tokens
                            last_widget._update_stats()

                    # Only save to file if save_chats is on
                    if globs.save_chats:
                        threading.Thread(target=save_conversation,
                                         args=(globs, user_text),
                                         daemon=True,
                                         name="Save Chats Thread").start()
                    else:
                        globs.is_new_conversation = False

                    # Debug print full conversation history
                    # logging.debug(f"\nFull conversation history:\n{globs.conversation_history}\n")

                    globs.still_streaming = False
                    if globs.legacy_mode:
                        globs.send_button.configure(
                            text=None,
                            image=globs.send_icon,
                            command=lambda: send_message(globs, ui_elements))
                    else:
                        globs.send_button.setText("➤")
                        if not globs.input_box.toPlainText().strip():
                            globs.send_button.setVisible(False)
                    return

                if globs.current_response_id == local_id:
                    # Accumulate raw response (markdown intact)
                    if isinstance(item, str):
                        globs.assistant_message += item
                    if globs.assistant_label:
                        if not globs.legacy_mode:
                            globs.assistant_label.setMarkdown(
                                globs.assistant_message)
                        else:
                            globs.assistant_label.configure(
                                text=globs.assistant_message)
                            globs.chat_frame._parent_canvas.yview_moveto(1.0)

        except queue.Empty:
            pass

        if globs.current_response_id != local_id:
            globs.still_streaming = False
            return

        if not globs.legacy_mode:
            QTimer.singleShot(20, lambda: pull_response(user_text))
        else:
            globs.root.after(20, lambda: pull_response(user_text))

    pull_response(user_text)
