# Managers/attachments.py
from PySide6.QtWidgets import QFileDialog
import logging
import os
import pdfplumber
from Utils.toast import show_toast

try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logging.warning("OCR libraries (pdf2image/pytesseract) not found. Fallback disabled.")

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
                      ".c", ".h", ".cs",
                      ".kt", ".swift", ".dart",
                      ".ts", ".tsx", ".jsx",
                      ".rb", ".pl", ".lua",
                      ".scala", ".hs", ".jl",
                      ".yml", ".env", ".r",
                      ".text", ".asc", ".properties",
                      ".m3u", ".lst", ".list",
                      ".gitignore", ".gitattributes",
                      ".pdf"]

def attach_file(globals):
    """Attach a file to a message."""
    globals.file_attachment = None
    globals.attachment_path = None

    # Open dialog box for filepath
    file, filter = QFileDialog.getOpenFileName(
        None,
        "Attach File",
        "",
        "All Files (*.*)",
        options=QFileDialog.Option.DontUseNativeDialog)
    
    # Return if file is not selected or is a directory
    if not file or not os.path.isfile(file):
        return

    # Store file path in global variable
    globals.attachment_path = file
    logging.info(f"Attached file: {file}")

    try:
        passed = False
        max_character_length = 10001

        # Open and extract file contents if filetype is accepted, save as global variable
        for i in accepted_filetypes:
            if file.lower().endswith(i):
                passed = True
                break
        
        # Exit with warning if file type is not supported
        if not passed:
            logging.warning(f"File type not supported: {file}")
            show_toast(globals, message=f"File type not supported: {file}", _type="error")
            return

        # Open and read file if passed
        if file.lower().endswith(".pdf"):
            attachment = parse_pdf(globals, file)
        else:
            with open(file, "r", encoding='utf-8') as f:
                attachment = f.read(max_character_length).strip()

        # Exit with warning if file is empty
        if not attachment:
            globals.attachment_path = None
            logging.warning(f"File is empty: {file}")
            show_toast(globals, message=f"File is empty: {file}", _type="error")
            return

        # Erase attachment and exit if file is too long
        if len(attachment) > 10000:
            logging.warning(f"File attachment too large. Maximum character length: 10,000.")
            show_toast(
                globals,
                message="File too large - Maximum character length: 10,000",
                _type="error")
            globals.attachment_path = None
            attachment = ""
            return

    # Exit on exception
    except UnicodeDecodeError:
        globals.attachment_path = None
        show_toast(globals, message="Cannot read file — wrong encoding or binary file", _type="error")
        return
    except Exception as e:
        globals.attachment_path = None
        logging.warning(f"Could not attach file due to: {e}")
        show_toast(
            globals,
            message=f"Could not attach file - Likely an unsupported file type with the wrong extension",
            _type="error")
        return
    
    # Set global variable and  disable button
    globals.file_attachment = attachment
    globals.file_button.configure(state="disabled")
    globals.attach_tip.configure(message="File Already Attached")


def parse_pdf(globals, file):
    """Parse text from a PDF."""
    text_collected = ""
    try:
        with pdfplumber.open(file) as pdf:
            if len(pdf.pages) > 50:
                logging.warning(f"PDF files can only be 50 pages or less.")
                show_toast(globals, message="Only 50 page or less PDF files are supported.", _type="error")
                return
            for page in pdf.pages:
                text = page.extract_text(layout=True) or ""
                if text.strip():
                    text_collected += text.strip() + "\n\n"
        if text_collected:
            return text_collected
    
        # Only run OCR if no text was extracted
        elif not text_collected.strip():
            logging.debug("pdfplumber returned no text - falling back to OCR")
            ocr_text = extract_with_ocr(file)
            return ocr_text
    
    except Exception as e:
        logging.error(f"Error reading with pdfplumber: {e}\nAttempting fallback OCR...")
        return ""

def extract_with_ocr(file):
    """Extract text with OCR if pdfplumber fails."""
    if not OCR_AVAILABLE:
        logging.warning(f"OCR not available for {file}. Skipping fallback.")
        return ""
    try:
        images = convert_from_path(file)
        text_collected = ""
        for image in images:
            text = pytesseract.image_to_string(image)
            if text.strip():
                text_collected += text + "\n\n"
        logging.debug(f"Full PDF text with OCR: {text_collected}")
        return str(text_collected)

    except Exception as e:
        logging.error(f"OCR error on {file}: {e}")
        return ""
