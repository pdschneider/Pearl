# Interface/chat_window.py
import tkinter as tk
from tkinter import scrolledtext, ttk
import logging, queue, threading
from Connections.ollama import chat_stream
from Managers.speech_manager import kokoro_speak, default_speak
from Managers.chat_history import add_message, save_conversation
import themes

def create_chat_tab(globals):
    """Creates the chat frame for talking with the LLM."""

    # Sets tkinter widgets to inactive status if Ollama isn't found
    widget_state = None
    if globals.ollama_active:
        widget_state = "normal"
    else:
        widget_state = "disabled"

    chat_frame = ttk.Frame(globals.notebook)
    globals.notebook.add(chat_frame, text="Chat")

    text_frame = ttk.Frame(chat_frame)
    text_frame.pack(fill="both", expand=True, padx=10, pady=10)

    chat_box = scrolledtext.ScrolledText(text_frame,
                                         wrap=tk.WORD,
                                         state="disabled",
                                         font=(themes.body_font, 10),
                                         bg="white",
                                         fg="black",
                                         relief="flat",
                                         padx=10,
                                         pady=10)
    chat_box.pack(fill="both", expand=True)

    # Rich Text
    chat_box.tag_config("header",    font=(themes.title_font))
    chat_box.tag_config("user",      font=(themes.body_font), justify="left")
    chat_box.tag_config("assistant", font=(themes.body_font))
    chat_box.tag_config("you",       font=(themes.body_font), justify="left")
    chat_box.tag_config("timestamp", font=(themes.mono_font))
    chat_box.tag_config("error",     font=(themes.mono_font))

    # Markdown
    chat_box.tag_config("markdown_bold",   font=(themes.body_font, 11, "bold"))
    chat_box.tag_config("markdown_italic", font=(themes.body_font, 11, "italic"))
    chat_box.tag_config("markdown_bold_italic", font=(themes.body_font, 11, "bold", "italic"))
    chat_box.tag_config("markdown_strike", font=(themes.body_font, 11, "overstrike"))

    if not globals.ollama_active:
        chat_box.config(state="normal")
        chat_box.insert(f"1.0", 
                        f"To use Pearl's chat feature, Ollama must be installed.\n\n" \
                        f"Installation instructions:\n\n" \
                        f"Head to https://ollama.com/download and follow the instructions for your OS.\n\n" \
                        f"After installing Ollama, you'll need to also download a compatible model.\n\n" \
                        f"There are many models to choose from,\nbut the recommended starting model is " \
                        f"llama3.2:latest.\n\n" \
                        f"Find models here: https://ollama.com/search\n\n" \
                        f"Have fun!")
        chat_box.config(state="disabled")
    if globals.ollama_active:
        chat_box.config(state="normal")
        chat_box.insert(f"1.0", "Pearl at your service!\n\n", "header")

    entry_frame = ttk.Frame(chat_frame)
    entry_frame.pack(fill="both", padx=10, pady=5)

    entrybox = tk.Text(entry_frame,
              bg="white",
              fg="black",
              wrap="word",
              state=widget_state,
              height=5)
    entrybox.pack(side="left", padx=5, pady=5, fill="x", expand=True)
    entrybox.focus_set()

    ttk.Button(entry_frame,
               text="➤",
               state=widget_state,
               style="TSendbutton.TButton",
               command=lambda: send_message()).pack(side="left", padx=5, pady=5)

    # Chat Functions
    def send_message(event=None):
        """Sends queries to the LLM."""
        q = queue.Queue()
        model = globals.active_model
        user_text = entrybox.get("1.0", "end").strip()
        if not user_text:
            return
        messages = globals.chat_history + [{"role": "user", "content": user_text}]
        threading.Thread(target=chat_stream, args=(model, messages, q), daemon=True, name="Chat Stream").start()

        globals.markdown_tag = None
        globals.assistant_message = ""
        message = user_text
        if not message:
            return
        append_to_chat("You: ", "you")
        append_to_chat(message + "\n\n", "user")

        add_message("user", user_text, combo=None) # Adds user message to chat file

        #Create markers for markdown
        chat_box.mark_set("assistant_start", "end-1c")
        chat_box.mark_gravity("assistant_start", "left")

        entrybox.delete("1.0", "end")
        globals.chat_history.append({"role": "user", "content": message})

        def pull_response():
            """Pulls the response from Ollama via the thread-safe queue and sends those via item to append_with_markdown"""
            try:
                while True:
                    item = q.get_nowait()
                    if item is None:
                        globals.chat_history.append({"role": "assistant", "content": globals.assistant_message})
                        append_to_chat(f"\n\n")
                        globals.assistant_message = globals.assistant_message.replace("***", "").replace("___", "").replace("**", "").replace("__", "").replace("*", "").replace("_", "").replace("~~", "")
                        if globals.kokoro_active and globals.tts_enabled == True and globals.tts_source == "kokoro":
                            kokoro_speak(globals.assistant_message, globals.active_voice)
                        elif globals.tts_enabled == True and globals.tts_source == "default":
                            default_speak(globals.assistant_message)
                        if globals.save_chats:
                            add_message("assistant", globals.assistant_message, combo=None) # Adds assistant message to chat file
                        save_conversation()
                        return
                    globals.assistant_message += item
                    append_with_markdown(item)
                    chat_box.update_idletasks()
            except queue.Empty:
                pass
            globals.root.after(20, pull_response)
        pull_response()

    def append_to_chat(text="", tag=None):
        """Appends messages to the chat box."""
        chat_box.config(state="normal")
        chat_box.insert("end", text, tag)
        chat_box.config(state="disabled")
        chat_box.see("end")

    def append_with_markdown(chunk=""):
        """Appends assistant messages to chat box with markdown."""
        chat_box.config(state="normal")
        clean_chunk = chunk.strip()
        if (clean_chunk.startswith("***") or 
            clean_chunk.endswith("***") or 
            clean_chunk.startswith("___") or 
            clean_chunk.endswith("___")) and globals.markdown_tag != "markdown_bold_italic":
            globals.markdown_tag = "markdown_bold_italic"
            chunk = chunk.replace("***", "").replace("___", "")
            if chunk != "":
                chat_box.insert("end", chunk, globals.markdown_tag)
            chat_box.config(state="disabled")
            logging.info(f"Markdown flag set to bold italic")
            return
        elif (clean_chunk.startswith("***") or 
              clean_chunk.endswith("***") or 
              clean_chunk.startswith("___") or 
              clean_chunk.endswith("___")) and globals.markdown_tag == "markdown_bold_italic":
            globals.markdown_tag = "assistant"
            chunk = chunk.replace("***", "").replace("___", "")
            if chunk != "":
                chat_box.insert("end", chunk, globals.markdown_tag)
            chat_box.config(state="disabled")
            logging.debug(f"Markdown flag set back to assistant")
            return
        elif (clean_chunk.startswith("**") or 
              clean_chunk.endswith("**") or 
              clean_chunk.startswith("__") or 
              clean_chunk.endswith("__")) and globals.markdown_tag != "markdown_bold":
            globals.markdown_tag = "markdown_bold"
            chunk = chunk.replace("**", "").replace("__", "")
            if chunk != "":
                chat_box.insert("end", chunk, globals.markdown_tag)
            chat_box.config(state="disabled")
            logging.info(f"Markdown flag set to bold")
            return
        elif (clean_chunk.startswith("**") or 
              clean_chunk.endswith("**") or 
              clean_chunk.startswith("__") or 
              clean_chunk.endswith("__")) and globals.markdown_tag == "markdown_bold":
            globals.markdown_tag = "assistant"
            chunk = chunk.replace("**", "").replace("__", "")
            if chunk != "":
                chat_box.insert("end", chunk, globals.markdown_tag)
            chat_box.config(state="disabled")
            logging.debug(f"Markdown flag set back to assistant")
            return
        elif (clean_chunk.startswith("*") or 
              clean_chunk.endswith("*") or 
              clean_chunk.startswith("_") or 
              clean_chunk.endswith("_")) and globals.markdown_tag != "markdown_italic":
            globals.markdown_tag = "markdown_italic"
            chunk = chunk.replace("*", "").replace("_", "")
            if chunk != "":
                chat_box.insert("end", chunk, globals.markdown_tag)
            chat_box.config(state="disabled")
            logging.info(f"Markdown flag set to italic")
            return
        elif (clean_chunk.startswith("*") or 
              clean_chunk.endswith("*") or 
              clean_chunk.startswith("_") or 
              clean_chunk.endswith("_")) and globals.markdown_tag == "markdown_italic":
            globals.markdown_tag = "assistant"
            chunk = chunk.replace("*", "").replace("_", "")
            if chunk != "":
                chat_box.insert("end", chunk, globals.markdown_tag)
            chat_box.config(state="disabled")
            logging.debug(f"Markdown flag set back to assistant")
            return
        elif (clean_chunk.startswith("~~") or 
              clean_chunk.endswith("~~")) and globals.markdown_tag != "markdown_strike":
            globals.markdown_tag = "markdown_strike"
            chunk = chunk.replace("~~", "")
            if chunk != "":
                chat_box.insert("end", chunk, globals.markdown_tag)
            chat_box.config(state="disabled")
            logging.info(f"Markdown flag set to strike")
            return
        elif (clean_chunk.startswith("~~") or 
              clean_chunk.endswith("~~")) and globals.markdown_tag == "markdown_strike":
            globals.markdown_tag = "assistant"
            chunk = chunk.replace("~~", "")
            if chunk != "":
                chat_box.insert("end", chunk, globals.markdown_tag)
            chat_box.config(state="disabled")
            logging.debug(f"Markdown flag set back to assistant")
            return
        else:
            chat_box.insert("end", chunk, globals.markdown_tag)
            chat_box.config(state="disabled")
        chat_box.see("end")

    def upon_enter():
        """Triggerrs send message and prevents additional lines in the entry box upon pressing enter"""
        send_message()
        return "break"
    
    def upon_shift_enter():
        """Ensures Shift+Enter creates a new line in the entry box and nothing more"""
        entrybox.insert(tk.INSERT, "\n")
        return "break"

    entrybox.bind("<Return>", lambda e: upon_enter() if not e.state & 1 else "break")
    entrybox.bind("<Shift-Return>", lambda e: upon_shift_enter())