# Utils/factory_reset.py
import shutil
import tkinter as tk
from tkinter import messagebox
from Utils.load_settings import load_data_path


def factory_reset_config(error=None):
    root = tk.Tk()
    root.withdraw()
    answer = messagebox.askyesno(parent=root,
                                 title="DANGER!!",
                                 message=f"It looks like you ran into an error"
                                 f" while building the GUI!\n"
                                 f"{error}\n"
                                 f"Would you like to reset settings "
                                 f"back to defaults?\n"
                                 f"This may or may not solve the issue "
                                 f"(and does not delete saved chats).",
                                 icon="error")
    if answer:
        shutil.rmtree(load_data_path("config"))
    root.destroy()

def total_factory_reset(globals):
    answer = messagebox.askyesno(parent=globals.root,
                                 title="Reset All Settings?",
                                 message=
"""
DANGER - This will reset all of your settings, chats, and logs.

Do you wish to completely wipe all Pearl-related data?
""",
                                 icon="error")
    if answer:
        try:
            shutil.rmtree(load_data_path("config"))
            shutil.rmtree(load_data_path("local"))
            shutil.rmtree(load_data_path("cache"))
            messagebox.showinfo(parent=globals.root,
                        title="Reset Successful!",
                        message=
"""
Successfully deleted all Pearl-related data!
""")
        except Exception as e:
            messagebox.showerror(parent=globals.root,
                        title="Reset Failed",
                        message=f"Unable to perform factory reset due to: {e}")
