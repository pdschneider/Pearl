# All Dependencies of **Pearl**

A full list of dependencies and their current versions are available in [requirements.txt](../packaging/requirements.txt).

## altgraph
Graph data structure library

Required for: pyinstaller

LICENSE: MIT

Source: https://github.com/ronaldoussoren/altgraph

## certifi
Mozilla CA certificate bundle

Required for: requests

LICENSE: Mozilla Public License, v.2.0

Source: https://github.com/certifi/python-certifi

## cffi
C Foreign Function Interface for Python

Depends on: pycparser

Required for: cryptography

LICENSE: MIT No Attribution

Source: https://github.com/python-cffi/cffi

## charset-normalizer
Character encoding detection

Required for: requests

LICENSE: MIT

Source: https://github.com/jawah/charset_normalizer

## click
Composable command line interface creation kit

LICENSE: BSD 3-Clause License

Source: https://github.com/pallets/click

## cloudpickle
Extended pickling support for Python objects

LICENSE: All Rights Reserved

Source: https://github.com/cloudpipe/cloudpickle

## cryptography
Cryptographic primitives (hashing, signing, etc.)

Depends on: cffi

LICENSE: Apache 2.0 / BSD

Source: https://github.com/pyca/cryptography

## CTkToolTip
Tooltip widget for customtkinter (old UI - deprecated)

Depends on: customtkinter

LICENSE: CC0 1.0 Universal

Source: https://github.com/Akascape/CTkToolTip

## customtkinter
Modern themed Tkinter widgets (old UI - deprecated)

LICENSE: MIT

Source: https://github.com/tomschimansky/customtkinter

## darkdetect
Detects OS dark/light mode

Dependency of: customtkinter

LICENSE: All rights reserved.

Source: https://github.com/albertosottile/darkdetect

## defusedxml
XML bomb / DoS protection for stdlib XML modules

LICENSE: Python Software Foundation License v2 (PSFL)

Source: https://github.com/tiran/defusedxml

## idna
International Domain Name Handling

Required for: requests, urllib3

LICENSE: BSD 3-Clause License / All rights reserved.

Source: https://github.com/kjd/idna

## joblib
Lightweight pipelining and parallelism helpers

LICENSE: BSD 3-Clause License

Source: https://github.com/joblib/joblib

## lxml
XML and HTML processing (libxml2/libxslt bindings)

LICENSE: BSD 3-Clause License

Source: https://github.com/lxml/lxml

## Markdown
Markdown to HTML converter

LICENSE: BSD 3-Clause License

Source: https://github.com/Python-Markdown/markdown

## Nuitka
Python compiler turning Python into C executables

LICENSE: AGPL-3.0

Source: https://github.com/Nuitka/Nuitka

## numpy
Numerical computing with arrays

LICENSE: All rights reserved.

Source: https://github.com/numpy/numpy

## packaging
Version parsing, packaging utilities

LICENSE: Apache 2.0 / BSD

Source: https://github.com/pypa/packaging

## pdf2image
Converts PDF pages to PIL images

Required for: pillow

LICENSE: MIT

Source: https://github.com/Belval/pdf2image

## pdfminer.six
Low-level PDF text/layout extraction

Required for: pdfplumber

LICENSE: MIT

Source: https://github.com/pdfminer/pdfminer.six

## pdfplumber
High-level PDF table/text extraction

LICENSE: MIT

Source: https://github.com/jsvine/pdfplumber

## pep8
PEP8 style tracker

LICENSE: None

Source: https://github.com/treyhunner/pep8

## pillow
Image processing library (PIL fork)

LICENSE: MIT-CMU

Source: https://github.com/python-pillow/Pillow

## pip
Package installer

LICENSE: MIT

Source: https://github.com/pypa/pip

## poppler-windows
Necessary for OCR on Windows

LICENSE: MIT

Source: https://github.com/oschwartz10612/poppler-windows

## psutil
System process monitoring

LICENSE: BSD 3-Clause

Source: https://github.com/giampaolo/psutil

## pulsectl
PulseAudio (libpulse) bindings and mixer controls

LICENSE: MIT

Source: https://github.com/mk-fg/python-pulse-control

## pycparser
C language parser for Python

Required for: cffi

LICENSE: All rights reserved.

Source: https://github.com/eliben/pycparser

## pygame
SDL-based multimedia and input handling library

LICENSE: LGPL-2.1

Source: https://github.com/pygame/pygame

## pyinstaller
Bundles Python apps into standalone executables

Depends on: altgraph, pyinstaller-hooks-contrib

LICENSE: GPL-2.0 or later / Apache 2.0 / MIT

Source: https://github.com/pyinstaller/pyinstaller

## pyinstaller-hooks-contrib
Community-maintained PyInstaller hooks

Required for: pyinstaller

LICENSE: Apache 2.0 / GPL-2.0 or later

Source: https://github.com/pyinstaller/pyinstaller-hooks-contrib

## pypdfium2
PDF rendering engine

LICENSE: None

Source: https://github.com/pypdfium2-team/pypdfium2

## PySide6
Main Qt6 Python bindings

## PySide6_Addons
Addons for Qt6 Python bindings

## PySide6_Essentials
Essentials for Qt6 Python bindings

## pytesseract
Python wrapper for Tesseract OCR engine

License: Apache 2.0

Source: https://github.com/tesseract-ocr/tesseract

## python-docx
Reads/writes .docx Word documents

LICENSE: MIT

Source: https://github.com/python-openxml/python-docx

## pyttsx3
Text-to-speech synthesis across platforms

LICENSE: Mozilla Public License 2.0 (MPL-2.0)

Source: https://github.com/nateshmbhat/pyttsx3

## regex
Alternative regular expression module with extended features

LICENSE: Apache 2.0

Source: https://github.com/mrabarnett/mrab-regex

## requests
HTTP library for making HTTP/HTTPS requests

Depends on: urllib3, idna, certifi, charset-normalizer

LICENSE: Apache 2.0

Source: https://github.com/psf/requests

## rs_bpe
Rust-backed BPE tokenizer with Python bindings

LICENSE: MIT

Source: https://github.com/gweidart/rs-bpe

## setuptools
Package building/installation

LICENSE: MIT

Source: https://github.com/pypa/setuptools

## shiboken6
C++ to Python binding generator that powers PySide6

Required for PySide6

## sounddevice
Play/record audio via PortAudio

LICENSE: MIT

Source: https://github.com/spatialaudio/python-sounddevice

## soundfile
Read/write audio files via libsndfile

LICENSE: BSD 3-Clause License

Source: https://github.com/bastibe/python-soundfile

## tqdm
Fast, extensible progress meter

LICENSE: MPL-2.0 AND MIT

Source: https://github.com/tqdm/tqdm

## typing_extensions
Backported typing features

LICENSE: Python Software Foundation License (PSFL)

Source: https://github.com/python/typing_extensions

## urllib3
Lower level HTTP library

Required for: requests

LICENSE: MIT

Source: https://github.com/urllib3/urllib3

## zstandard
Zstandard compression library

Required by: Nuitka

LICENSE: BSD 3-Clause / All rights reserved.

Source: https://github.com/indygreg/python-zstandard

---

*Up to date as of v0.4.1*
