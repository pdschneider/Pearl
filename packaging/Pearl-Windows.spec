# -*- mode: python ; coding: utf-8 -*-

# Hooks
from PyInstaller.utils.hooks import collect_all

ret_pyside = collect_all('PySide6')
ret_shiboken = collect_all('shiboken6')

a = Analysis(
    ['../pearl.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../defaults', 'defaults'),
        ('../CHANGELOG.md', '.'),
        ('../README.md', '.'),
    ],
    hiddenimports=['pygame', 'requests', 'packaging', 'pkg_resources', 'PIL._tkinter_finder', 'PySide6', 'shiboken6', 'pdfplumber', 'pytesseract'],
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
    name='Pearl',
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
    icon='../defaults/assets/pearl.ico',
    version='version.txt'
)