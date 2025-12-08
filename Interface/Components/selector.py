# Interface/Components/selector.py
import logging
import customtkinter as ctk
from Connections.ollama import get_all_models, get_loaded_models, unload_model

class Treeview:
    def __init__(self, globals_obj, parent, get_dir=None):
        """Initializes class variables."""
        self.globals = globals_obj
        self.parent = parent
        self._rows = []
        self._selected = set()
        self._last_idx = None
        self._rename_bind_id = None
        if get_dir is None:
            self.get_dir = lambda: get_all_models()
        elif callable(get_dir):
            self.get_dir = get_dir
        else:
            self.get_dir = lambda: str(get_dir)
        self._build_ui()

    def _build_ui(self):
        """Builds the core selection UI."""
        try:
            self.selection_frame = ctk.CTkScrollableFrame(self.parent, fg_color="transparent")
            self.selection_frame.pack(fill="both", expand=True, pady=0, padx=10)
        except Exception as e:
            logging.critical(f"Could not create scrollable frame. Aborting treeview: {e}")
            return

        models = self.get_dir()
        loaded = get_loaded_models()
        for idx, model in enumerate(sorted(models)):
            row = ctk.CTkFrame(self.selection_frame, height=42, corner_radius=8)
            row.pack(fill="x", padx=8, pady=3)

            label = ctk.CTkLabel(row, text=model, anchor="w")
            label.pack(side="left", padx=12, pady=8, fill="x", expand=True)
            self._rows.append((row, model))
            if model == self.globals.active_model:
                label.configure(fg_color="red")

            if model in loaded:
                icon = ctk.CTkLabel(row, text="⤴", width=20)
                icon.pack(side="right", padx=5)
                icon.bind("<Button-1>", lambda e, m=model: self._unload_handler(e, m))

            row.bind("<Button-1>", lambda e, i=idx, f=model: self._on_row_click(e, i, f))
            label.bind("<Button-1>", lambda e, i=idx, f=model: self._on_row_click(e, i, f))

        self.selection_frame.focus_set()

    def _apply_highlight(self, row, on=True):
        """Highlights a specific row."""
        row.configure(fg_color="white" if on else "transparent")

    def _on_row_click(self, event, idx, filename):
        """Triggers selection of an item upon click"""
        if event.state & 0x0001:
            return
        if event.state & 0x0004:
            return
        self.selection_clear()
        self._selected.add(filename)
        self._last_idx = idx
        row, _ = self._rows[idx]
        self._apply_highlight(row, on=True)
        self.selection_frame.focus_set()

    def _unload_handler(self, event, model):
        """Handles unloading of models."""
        unload_model(model)
        self.refresh()
        return "break"

    def selection_clear(self):
        """Clears the selection after triggering an action."""
        for row, _ in self._rows:
            self._apply_highlight(row, on=False)
        self._selected.clear()
        self._last_idx = None

    def refresh(self):
        """Refreshes the selector UI after an action has changed its contents."""
        for row, _ in self._rows:
            row.destroy()
        self._rows.clear()
        self.selection_clear()

        models = get_all_models()
        loaded = get_loaded_models()
        for idx, model in enumerate(sorted(models)):
            row = ctk.CTkFrame(self.selection_frame, height=42, corner_radius=8)
            row.pack(fill="x", padx=8, pady=3)

            label = ctk.CTkLabel(row, text=model, anchor="w")
            label.pack(side="left", padx=12, pady=8, fill="x", expand=True)

            if model in loaded:
                icon = ctk.CTkLabel(row, text="⤴", width=20)
                icon.pack(side="right", padx=5)
                icon.bind("<Button-1>", lambda e, m=model: self._unload_handler(e, m))

            self._rows.append((row, model))
            row.bind("<Button-1>", lambda e, i=idx, f=model: self._on_row_click(e, i, f))
            label.bind("<Button-1>", lambda e, i=idx, f=model: self._on_row_click(e, i, f))
            self.selection_frame.focus_set()

    def selection(self):
        """Returns selected row."""
        return list(self._selected)
