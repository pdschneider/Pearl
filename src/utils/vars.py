# Utils/vars.py
import customtkinter as ctk


def create_vars(globs):
    """Creates Tkinter variables"""
    globs.logging_var = ctk.StringVar(value=globs.logging_level)
    globs.theme_var = ctk.StringVar(value=globs.active_theme)
    globs.tts_var = ctk.BooleanVar(value=globs.tts_enabled)
    globs.kokoro_active_voice_var = ctk.StringVar(value=globs.kokoro_active_voice)
    globs.default_active_voice_var = ctk.StringVar(value=globs.default_active_voice)
    globs.tts_source_var = ctk.StringVar(value=globs.tts_source)
    globs.save_chats_var = ctk.BooleanVar(value=globs.save_chats)
    globs.sink_var = ctk.StringVar(value=globs.default_sink)
    globs.github_check_var = ctk.BooleanVar(value=globs.github_check)
    globs.language_var = ctk.StringVar(value=globs.language)
    globs.ollama_chat_path_var = ctk.StringVar(value=globs.ollama_chat_path)
    globs.ollama_context_path_var = ctk.StringVar(value=globs.ollama_context_path)
    globs.ollama_title_path_var = ctk.StringVar(value=globs.ollama_title_path)
    globs.enable_context_var = ctk.BooleanVar(value=globs.enable_context)
    globs.generate_titles_var = ctk.BooleanVar(value=globs.generate_titles)
    globs.beta_var = ctk.BooleanVar(value=globs.beta)
    globs.dynamic_window_size_var = ctk.BooleanVar(value=globs.dynamic_window_size)
    globs.legacy_mode_var = ctk.BooleanVar(value=globs.legacy_mode)
