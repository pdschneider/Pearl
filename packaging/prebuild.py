# packaging/version_gen.py
# Auto-generates version.txt from version.py for PyInstaller Windows builds
# Also updates Inno Script and Debian files

import re
import sys
from pathlib import Path

# Add the project root to Python path so we can import "version" reliably
project_root = Path(__file__).parent.parent.resolve()   # Goes up from packaging/ to root
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from version import __version__, __author__, __title__, __description__

# Parse version string into tuple (major, minor, patch, build)
try:
    clean_version = __version__.replace('-beta', '').replace('-rc', '').replace('-alpha', '')
    major, minor, patch = map(int, clean_version.split('.'))
    build = 0
except Exception:
    major, minor, patch, build = 0, 1, 0, 0

content = f'''# UTF-8
# Auto-generated from version.py - DO NOT EDIT MANUALLY

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({major}, {minor}, {patch}, {build}),
    prodvers=({major}, {minor}, {patch}, {build}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [
          StringStruct('CompanyName', '{__author__}'),
          StringStruct('FileDescription', '{__description__}'),
          StringStruct('FileVersion', '{__version__}'),
          StringStruct('InternalName', '{__title__}'),
          StringStruct('LegalCopyright', 'Copyright © 2026 {__author__}. Apache 2.0.'),
          StringStruct('OriginalFilename', '{__title__}.exe'),
          StringStruct('ProductName', '{__title__}'),
          StringStruct('ProductVersion', '{__version__}'),
          StringStruct('Comments', '{__description__}'),
        ])
      ]),
    VarFileInfo([VarStruct('Translation', [0x409, 1200])])
  ]
)
'''

# Also update the Inno Script file with correct information
inno_script_path = project_root / 'packaging' / 'InnoSetup.iss'

if inno_script_path.exists():
    with open(inno_script_path, 'r', encoding='utf-8') as f:
        inno_content = f.read()

    # Update the three defines using the values from version.py
    inno_content = re.sub(
        r'^#define MyAppName ".*"',
        f'#define MyAppName "{__title__}"',
        inno_content,
        flags=re.MULTILINE
    )
    inno_content = re.sub(
        r'^#define MyAppVersion ".*"',
        f'#define MyAppVersion "{__version__}"',
        inno_content,
        flags=re.MULTILINE
    )
    inno_content = re.sub(
        r'^#define MyAppPublisher ".*"',
        f'#define MyAppPublisher "{__author__}"',
        inno_content,
        flags=re.MULTILINE
    )

    with open(inno_script_path, 'w', encoding='utf-8') as f:
        f.write(inno_content)
    
    print(f"✅ Inno Setup script successfully updated")
    print(f"   Location: {inno_script_path}")
else:
    print(f"⚠️  Inno script not found at {inno_script_path}")

# Update the Debian control file
control_file_path = project_root / 'packaging' / 'deb' / 'DEBIAN' / 'control'

if control_file_path.exists():
    with open(control_file_path, 'r', encoding='utf-8') as f:
        control_content = f.read()

    # Replace the Version line specifically
    # This regex matches "Version: " followed by anything until the end of the line
    deb_version = __version__.replace('-beta', '~beta').replace('-rc', '~rc').replace('-alpha', '~alpha')

    control_content = re.sub(
        r'^Version: .*$',
        f'Version: {deb_version}',
        control_content,
        flags=re.MULTILINE)

    with open(control_file_path, 'w', encoding='utf-8') as f:
        f.write(control_content)
    
    print(f"✅ Debian control file successfully updated")
    print(f"   Location: {control_file_path}")
else:
    print(f"⚠️  Control file not found at {control_file_path}")

# Always write version.txt to the corect location
version_txt_path = project_root / 'packaging' / 'version.txt'

with open(version_txt_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ version.txt successfully generated with version {__version__}")
print(f"   Location: {version_txt_path}")

def sync_spec_files(project_root):
    """Read requirements.txt and inject hidden imports + PySide6 hooks into spec files."""

    req_path = project_root / 'packaging' / 'requirements.txt'
    if not req_path.exists():
        print("⚠️  requirements.txt not found")
        return

    req_text = req_path.read_text(encoding='utf-8').lower()

    # Extract package names without version specifiers
    req_packages = set()
    for line in req_text.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            pkg_name = re.split(r'[=<>!~]', line)[0]
            req_packages.add(pkg_name)

    # Maps requirements.txt package name to hidden import names
    HIDDEN_IMPORT_MAP = {
        'packaging': ['packaging'],
        'pillow': ['PIL._tkinter_finder', 'PIL'],
        'customtkinter': ['tkinter', '_tkinter'],
        'pygame': ['pygame'],
        'requests': ['requests'],
        'pdfplumber': ['pdfplumber'],
        'pytesseract': ['pytesseract'],
        'openpyxl': ['openpyxl'],
        'watchdog': ['watchdog'],
        'msoffcrypto-tool': ['msoffcrypto'],
        'pdf2image': ['pdf2image'],
    }

    # Build the list of hidden imports based on what's installed
    imports_to_add = []
    for req_pkg, hidden_imports in HIDDEN_IMPORT_MAP.items():
        if req_pkg in req_packages:
            imports_to_add.extend(hidden_imports)

    # Handle PySide6 hooks separately
    has_pyside = 'pyside6' in req_packages
    if has_pyside:
        imports_to_add.extend(['PySide6', 'shiboken6'])

    pyside_hooks = (
        "from PyInstaller.utils.hooks import collect_all\n"
        "ret_pyside = collect_all('PySide6')\n"
        "ret_shiboken = collect_all('shiboken6')"
    ) if has_pyside else ""

    # Find all spec files in packaging/
    spec_files = list((project_root / 'packaging').glob('*.spec'))

    for spec_path in spec_files:
        content = spec_path.read_text(encoding='utf-8')

        # Replace everything between the PYSIDE HOOKS markers
        content = re.sub(
            r'# --- SPAWN PYSIDE HOOKS START ---\n.*?# --- SPAWN PYSIDE HOOKS END ---',
            f'# --- SPAWN PYSIDE HOOKS START ---\n{pyside_hooks}\n# --- SPAWN PYSIDE HOOKS END ---',
            content,
            flags=re.DOTALL
        )

        # Replace everything between the IMPORTS markers
        if imports_to_add:
            imports_str = '\n'.join(
                f"        '{imp}'," for imp in sorted(set(imports_to_add))
            )
        else:
            imports_str = ""

        content = re.sub(
            r'# --- SPAWN IMPORTS START ---\n.*?# --- SPAWN IMPORTS END ---',
            f'# --- SPAWN IMPORTS START ---\n{imports_str}\n        # --- SPAWN IMPORTS END ---',
            content,
            flags=re.DOTALL
        )

        spec_path.write_text(content, encoding='utf-8')
        print(f"✅ Synced {spec_path.name} ({len(imports_to_add)} hidden imports)")

sync_spec_files(project_root)
