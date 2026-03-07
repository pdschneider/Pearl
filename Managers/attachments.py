# Managers/attachments.py
from tkinter import filedialog
import logging
import os
from Utils.toast import show_toast


accepted_filetypes = [".txt", ".csv", ".json",
                      ".py", ".pyw", ".spec",
                      ".log", ".ini", ".cfg",
                      ".xml", ".sh", ".bat",
                      ".ps1", ".md", ".tsv",
                      ".toml", ".yaml", ".html",
                      ".css", ".rst", ".adoc",
                      ".tex", ".org", ".conf",
                      ".js", ".sql", ".go",
                      ".rs", ".php", ".cpp",
                      ".c", ".h", ".cs ",
                      ".kt", ".swift", ".dart",
                      ".ts", ".tsx", ".jsx",
                      ".rb", ".pl", ".lua",
                      ".scala", ".hs", ".jl",
                      ".yml", ".env", ".r",
                      ".text", ".asc", ".properties",
                      ".m3u", ".lst", ".list",
                      ".gitignore", ".gitattributes"]

def attach_file(globals):
    """Attach a file to a message."""
    globals.file_attachment = None
    globals.attachment_path = None

    # Open dialog box for filepath
    file = filedialog.askopenfilename(parent=globals.file_button,
                                        title="Select Attachment",
                                        filetypes=(("All files", "*.*"),
                                                    ("Text files", "*.txt"),
                                                    ("CSV files", "*.csv"),
                                                    ("Python files", "*.py")))
    
    # Return if file is not selected or is a directory
    if not file or not os.path.isfile(file):
        return

    # Store file path in global variable
    globals.attachment_path = file
    logging.info(f"Attached file: {file}")

    try:
        # Open and extract file contents if filetype is accepted, save as global variable
        for i in accepted_filetypes:
            if file.endswith(i):
                with open(file, "r", encoding='utf-8') as f:
                    attachment = f.read().strip()

        # Exit with warning if file type is not supported
        if not attachment:
            globals.attachment_path = None
            logging.warning(f"File type not supported: {file}")
            show_toast(globals, message=f"File type not supported: {file}", _type="error")
            return

        # Erase attachment and exit if file is too long
        logging.debug(f"File Attachment Character Length: {len(attachment)}")
        if len(attachment) > 10000:
            logging.warning(f"File attachment too large. Maximum character length: 10,000.")
            show_toast(
                globals,
                message="File attachment too large - Maximum character length: 10,000",
                _type="error")
            globals.attachment_path = None
            return

    # Exit on exception
    except Exception as e:
        logging.warning(f"Could not attach file due to: {e}")
        globals.attachment_path = None
        show_toast(
            globals,
            message=f"Could not attach file - Likely an unsupported file type with the wrong extension",
            _type="error")
        return
    
    # Set global variable and  disable button if file attachment succeeded
    if attachment:
        globals.file_attachment = attachment
        globals.file_button.configure(state="disabled")
        globals.attach_tip.configure(message="File Already Attached")
