# Managers/attachments.py
from PySide6.QtWidgets import QFileDialog
import logging
import os
import pdfplumber
import subprocess
import platform
import base64
from src.utils.toast import show_toast
from src.connections.ollama import create_model_list, gpu_check
from rs_bpe.bpe import openai
from docx import Document

os_name = platform.platform()

# Silence window spam
if os_name.startswith("Windows"):
    _original_popen = subprocess.Popen
    def _popen_nowindow(*args, **kwargs):
        kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        return _original_popen(*args, **kwargs)
    subprocess.Popen = _popen_nowindow

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
                      ".pdf", ".repo", ".htm",
                      ".java", ".xhtml", ".scss",
                      ".sass", ".less", ".vbs",
                      ".asp", ".ipynb", ".editorconfig",
                      ".htaccess", ".dockerignore",
                      ".bashrc", ".bash_aliases",
                      ".bash_history", ".lynxrc",
                      ".bash_logout", ".gitconfig",
                      ".python_history", ".profile",
                      ".taskrc", ".selected_editor",
                      ".steampid", ".sweeprc",
                      ".sweeptimes", ".update-timestamp",
                      ".wget-hsts", ".windows-serial",
                      ".xinputrc", ".xsession-errors",
                      ".zshrc", ".lesshst", ".iss",
                      ".desktop", ".pid", ".directory",
                      ".adm", ".admx", ".adml",
                      ".eml", ".zig", ".nim",
                      ".erl", ".ex", ".exs",
                      ".sol", ".vue", ".svelte",
                      ".tf", ".tfvars", ".f",
                      ".f90", ".asm", ".s",
                      ".cmake", ".gradle", ".m",
                      ".mm", ".vimrc", ".inputrc",
                      ".npmrc", ".nvmrc", ".yarnrc",
                      ".eslintrc", ".prettierrc",
                      ".babelrc", ".pylintrc",
                      ".flake8", ".gemrc", ".docx",
                      ".jpg", ".jpeg", ".png",
                      ".gif"]

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
        max_character_length = 20_000

        # Open and extract file contents if filetype is accepted, save as global variable
        for i in accepted_filetypes:
            if file.lower().endswith(i):
                passed = True
                break

        # Exit with warning if file type is not supported
        if not passed:
            logging.warning(f"File type not supported: {file}")
            show_toast(globals, message=f"File type not supported", _type="error")
            return

        # Exit if file size is too big
        max_file_size = 52_428_800  # 50MB
        file_size = os.path.getsize(globals.attachment_path)
        logging.debug(f"File Size: {file_size}")
        if file_size > max_file_size:
            logging.warning(f"File size too large (Max: {max_file_size})")
            show_toast(globals, message=f"File size too large (Max: {max_file_size})", _type="error")
            return

        # Open and read file
        if file.lower().endswith(".pdf"):
            logging.debug(f"Parsing PDF file...")
            attachment = parse_pdf(globals, file)
        elif file.lower().endswith(".docx"):
            logging.debug(f"Parsing docx file...")
            attachment = parse_docx(file)
        elif file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            globals.image_attachment = globals.attachment_path
            attachment = "Image Attached"
            logging.debug(f"Image Attachment: {globals.image_attachment}")
        else:
            logging.debug(f"Reading plain text file...")
            with open(file, "r", encoding='utf-8') as f:
                attachment = f.read(max_character_length + 1).strip()

        # Exit with warning if file is empty
        if not attachment:
            globals.attachment_path = None
            logging.warning(f"File is empty: {file}")
            show_toast(globals, message=f"File is empty: {file}", _type="error")
            return

        # Erase attachment and exit if file is too long
        if len(attachment) > 30_000:
            logging.warning(f"File attachment too large. Maximum character length: {max_character_length}.")
            show_toast(
                globals,
                message=f"File too long - Maximum character length: {max_character_length}",
                _type="error")
            globals.attachment_path = None
            attachment = ""
            return
        
        # Calculate context length
        model_data = create_model_list(globals)
        model_max_context = model_data[globals.active_model]["context_length"]

        # Determine if context length can exceed 64,000
        is_gpu = gpu_check()
        if is_gpu:
            globals.context_length = model_max_context
        else:
            globals.context_length = model_max_context if model_max_context < 64000 else 64000
        logging.debug(f"Max Context Length: {globals.context_length}")

        # Calculate tokens within document
        encoder = openai.cl100k_base()
        tokens = encoder.encode(str(attachment))
        token_count = len(tokens)
        logging.debug(f"Attachment token length: {token_count}")

        # Exit with warning if file exceeds max tokens
        if token_count > globals.context_length:
            logging.warning(f"Attachment exceeds maximum token count - please upload a smaller file or switch to a different model.")
            show_toast(
                globals,
                message="File too long - attachment exceeds maximum token count for this model",
                _type="error")
            globals.attachment_path = None
            attachment = ""
            return
        
        # Turn image into readable format
        if globals.image_attachment:
            with open(globals.image_attachment, "rb") as f:
                globals.image_attachment = base64.b64encode(f.read()).decode('utf-8')

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
        if os_name.startswith("Windows"):
            import pdf2image.pdf2image
            pdf2image.pdf2image.Popen = _popen_nowindow
            # Point to bundled popplar files
            kwargs = {}
            base = os.path.dirname(os.path.abspath(__file__))
            pytesseract.pytesseract.tesseract_cmd = os.path.join(base, '..', '..', 'bin', 'Tesseract', 'tesseract.exe')
            # Walk up to project root
            project_root = os.path.normpath(os.path.join(base, '..', '..'))
            poppler_bin = os.path.join(project_root, 'bin', 'Poppler', 'Library', 'bin')
            if os.path.isdir(poppler_bin):
                kwargs['poppler_path'] = poppler_bin
    except:
        logging.error(f"Unable to find Poppler / Tesseract")
    try:
        images = convert_from_path(file, **kwargs)  # Convert PDF to list of images
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

def parse_docx(file):
    """Parses .docx files to plain text."""
    try:
        doc = Document(file)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        logging.error(f"Unable to parse .docx file due to: {e}")
        return ""
