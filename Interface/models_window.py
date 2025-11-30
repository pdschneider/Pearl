# Interface/models_window.py
import logging
from tkinter import ttk
from tkinter import messagebox
from Connections.ollama import get_all_models, get_loaded_models, unload_model, load_model
from Utils.hardware import get_ram_info
import config

def create_models_tab(globals):
    """Creates the Models tab frame and initializes widgets"""
    models_frame = ttk.Frame(globals.notebook)
    globals.notebook.add(models_frame, text="Models")

    tree_frame = ttk.Frame(models_frame)
    tree_frame.pack(padx=5, pady=5, expand=True, fill="both")

    model_tree = ttk.Treeview(tree_frame, columns="loaded", height=15)
    model_tree.heading(column="#0", text="Models")
    model_tree.column(column="#0")
    model_tree.heading(column="loaded", text="Loaded")
    model_tree.column(column="loaded")

    def load_selected():
        """Loads selected model into memory"""
        available_ram = get_ram_info()
        sel = model_tree.selection()
        if available_ram != {}:
            if available_ram["avail_ram_gb"] < 1.0:
                logging.warning(f"Cannot load models with less than 1GB of available RAM.")
                messagebox.showerror(title="Not Enough RAM",
                                    message="Must have more than 1GB of available RAM to load models.",
                                    parent=models_frame,)
                return
        else:
            if not sel:
                return
            model_name = model_tree.item(sel[0], "text")
            load_model(model_name)
            refresh_tree()

    def unload_selected():
        """Unloads selected model from memory"""
        sel = model_tree.selection()
        if not sel:
            return
        model_name = model_tree.item(sel[0], "text")
        unload_model(model_name)
        refresh_tree()

    def set_selected():
        """Sets selected model as active model"""
        sel = model_tree.selection()
        if not sel:
            return
        available_ram = get_ram_info()
        model_name = model_tree.item(sel[0], "text")
        if available_ram != {}:
            if available_ram["avail_ram_gb"] < 1.0 and model_name not in get_loaded_models():
                logging.warning(f"Cannot load models with less than 1GB of available RAM.")
                messagebox.showerror(title="Not Enough RAM",
                                    message="Must have more than 1GB of available RAM to load models.",
                                    parent=models_frame,)
                return
        model_name = model_tree.item(sel[0], "text")
        globals.active_model = model_name
        config.save_settings(active_model=model_name)
        if model_name not in get_loaded_models():
            load_selected()
        refresh_tree()

    buttons_frame = ttk.Frame(models_frame)
    buttons_frame.pack(padx=5, pady=5)

    ttk.Button(buttons_frame, text="Load", command=load_selected).grid(row=0, column=0, padx=5)
    ttk.Button(buttons_frame, text="Unload", command=unload_selected).grid(row=0, column=1, padx=5)
    ttk.Button(buttons_frame, text="Select", command=set_selected).grid(row=0, column=2, padx=5)

    def refresh_tree():
        model_tree.delete(*model_tree.get_children())
        if globals.ollama_active:
            try:
                all_models = get_all_models()
                loaded_models = set(get_loaded_models())

                for model in all_models:
                    status = "Yes" if model in loaded_models else "No"
                    model_tree.insert(parent="", index="end", text=model, values=(status),)
                model_tree.pack(padx=5, pady=5, fill="both", expand=True)
            except Exception as e:
                logging.error(f"Could not refresh tree due to: {e}.")

    refresh_tree()