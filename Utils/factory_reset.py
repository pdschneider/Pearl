# Utils/factory_reset.py
import shutil
import tkinter as tk
from tkinter import messagebox
from Utils.load_settings import load_data_path


def factory_reset(error):
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
