# Interface/chat_window.py
import tkinter as tk
from tkinter import scrolledtext, ttk
from Connections.ollama import chat_stream

def create_chat_tab(globals):
    """Creates the chat frame for talking with the LLM."""
    chat_frame = ttk.Frame(globals.notebook)
    globals.notebook.add(chat_frame, text="Chat")

    text_frame = ttk.Frame(chat_frame)
    text_frame.pack(fill="both", expand=True, padx=10, pady=10)

    chat_box = scrolledtext.ScrolledText(text_frame,
                                         wrap=tk.WORD,
                                         state="disabled",
                                         font=("Ubuntu", 10),
                                         bg="white",
                                         fg="black",
                                         relief="flat",
                                         padx=10,
                                         pady=10)
    chat_box.pack(fill="both", expand=True)

    entry_frame = ttk.Frame(chat_frame)
    entry_frame.pack(fill="both", padx=10, pady=5)

    entrybox = tk.Text(entry_frame,
              bg="white",
              fg="black",
              wrap="word",
              height=5)
    entrybox.grid(row=0, column=0, padx=5, pady=5)
    entrybox.focus_set()

    ttk.Button(entry_frame,
               text="Send",
               style="TButton",
               command=lambda: send_message()).grid(row=0, column=1, padx=5, pady=5)

    # Chat Functions
    def append_to_chat(text=""):
        """Appends messages to the chat box."""
        chat_box.config(state="normal")
        chat_box.insert("end", text)
        chat_box.config(state="disabled")
        chat_box.see("end")

    def send_message(event=None):
        """Sends queries to the LLM."""
        message = entrybox.get("1.0", "end").strip()
        if not message:
            return
        append_to_chat("You: " + message + "\n\n")
        entrybox.delete("1.0", "end")
        globals.chat_history.append({"role": "user", "content": message})
        assistant_reply = ""
        for chunk in chat_stream(globals.active_model, globals.chat_history + [{"role": "user", "content": message}]):
            assistant_reply += chunk
            append_to_chat(chunk)
            chat_box.update_idletasks()
        globals.chat_history.append({"role": "assistant", "content": assistant_reply})
        append_to_chat(f"\n\n")

    entrybox.bind("<Return>", lambda e: send_message() if not e.state & 1 else "break")
    entrybox.bind("<Shift-Return>", lambda e: "break")