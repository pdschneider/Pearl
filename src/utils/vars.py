# Utils/vars.py
import customtkinter as ctk


def create_vars(globals):
    """Creates Tkinter variables"""
    globals.logging_var = ctk.StringVar(value=globals.logging_level)
    globals.theme_var = ctk.StringVar(value=globals.active_theme)
    globals.tts_var = ctk.BooleanVar(value=globals.tts_enabled)
    globals.kokoro_active_voice_var = ctk.StringVar(value=globals.kokoro_active_voice)
    globals.default_active_voice_var = ctk.StringVar(value=globals.default_active_voice)
    globals.tts_source_var = ctk.StringVar(value=globals.tts_source)
    globals.save_chats_var = ctk.BooleanVar(value=globals.save_chats)
    globals.sink_var = ctk.StringVar(value=globals.default_sink)
    globals.github_check_var = ctk.BooleanVar(value=globals.github_check)
    globals.language_var = ctk.StringVar(value=globals.language)
    globals.ollama_chat_path_var = ctk.StringVar(value=globals.ollama_chat_path)
    globals.ollama_context_path_var = ctk.StringVar(value=globals.ollama_context_path)
    globals.ollama_title_path_var = ctk.StringVar(value=globals.ollama_title_path)
    globals.enable_context_var = ctk.BooleanVar(value=globals.enable_context)
    globals.generate_titles_var = ctk.BooleanVar(value=globals.generate_titles)
