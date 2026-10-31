# -*- mode: python ; coding: utf-8 -*-

# --- SPAWN PYSIDE HOOKS START ---
from PyInstaller.utils.hooks import collect_all
ret_pyside = collect_all('PySide6')
ret_shiboken = collect_all('shiboken6')
# --- SPAWN PYSIDE HOOKS END ---

a = Analysis(
    ['../main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../defaults', 'defaults'),
        ('../docs', 'docs'),
        ('../CHANGELOG.md', '.'),
        ('../LICENSE.txt', '.')
    ],
    hiddenimports=[
        # --- SPAWN IMPORTS START ---
        'PIL',
        'PIL._tkinter_finder',
        'PySide6',
        '_tkinter',
        'packaging',
        'pdf2image',
        'pdfplumber',
        'pygame',
        'pytesseract',
        'requests',
        'shiboken6',
        'tkinter',
        # --- SPAWN IMPORTS END ---
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='LOWERAPPNAME',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True,
)