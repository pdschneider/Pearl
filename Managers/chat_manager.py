# Managers/chat_manager.py
import threading, queue
from Connections.ollama import chat_stream
from Managers.speech_manager import kokoro_speak, default_speak
from Managers.chat_history import save_conversation, add_message

# Chat Functions
def send_message(globals, ui_elements, event=None):
    """Sends queries to the LLM"""
    q = queue.Queue()
    model = globals.active_model
    user_text = ui_elements['entrybox'].get("1.0", "end").strip()
    if not user_text:
        return
    
    ui_elements["add_bubble"]("user", user_text)
    ui_elements['entrybox'].delete("1.0", "end")

    messages = globals.chat_history + [{"role": "user", "content": user_text}]
    threading.Thread(target=chat_stream, args=(model, messages, q), daemon=True, name="Chat Stream").start()

    globals.assistant_label = ui_elements["add_bubble"]("assistant", "")
    globals.assistant_message = ""

    globals.chat_history.append({"role": "user", "content": user_text})

    def pull_response():
        """Pulls the response from Ollama via the thread-safe queue"""
        try:
            while True:
                item = q.get_nowait()
                if item is None:
                    globals.chat_history.append({"role": "assistant", "content": globals.assistant_message})
                    # TTS
                    globals.assistant_message = globals.assistant_message.replace("***", "").replace("___", "").replace("**", "").replace("__", "").replace("*", "").replace("_", "").replace("~~", "")
                    if globals.kokoro_active and globals.tts_enabled == True and globals.tts_source == "kokoro":
                        kokoro_speak(globals.assistant_message, globals.active_voice)
                    elif globals.tts_enabled == True and globals.tts_source == "default":
                        default_speak(globals.assistant_message)
                    # Save
                    if globals.save_chats:
                        add_message("assistant", globals.assistant_message, combo=None)
                    save_conversation()
                    return

                globals.assistant_message += item.replace("***", "").replace("___", "").replace("**", "").replace("__", "").replace("*", "").replace("_", "").replace("~~", "")
                if globals.assistant_label:
                    globals.assistant_label.configure(text=globals.assistant_message)
                ui_elements["scroll_to_bottom"]()

        except queue.Empty:
            pass

        globals.root.after(20, pull_response)

    pull_response()
