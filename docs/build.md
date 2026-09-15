
# 🚀 How to Build

Pearl can be built from source code via Pyinstaller or Nuitka on both Windows and Linux. This is for advanced users only - the simplest way to run Pearl is to download the latest release.

## 🐧 Linux

Open your IDE (VSCode recommended) and create a virtual environment using Python 3.13.15:

**Download Python 3.13.15** from [Deadsnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa).

```
python3 -m venv pearl_venv

source pearl_venv/bin/activate
```

**IMPORTANT: Must have patchelf installed: `sudo apt patchelf`**

### Pyinstaller

Run these commands to install dependencies and generate the file:

```
pip install -r packaging/requirements.txt

pyinstaller packaging/Pearl-Linux.spec --clean
```

### Nuitka

Run these commands to install dependencies and generate the file:

```
pip install -r packaging/requirements.txt

nuitka \
    --standalone \
    --quiet \
    --remove-output \
    --output-dir=dist \
    --product-version=0.4.1 \
    --file-version=0.4.1 \
    --company-name=Pearl \
    --product-name=Pearl \
    --output-filename=pearl-gui \
    --enable-plugin=pyside6 \
    --enable-plugin=tk-inter \
    --include-qt-plugins=platforms,iconengines,imageformats \
    --include-package=pyttsx3.drivers \
    --include-data-dir=defaults=defaults \
    --include-data-dir=docs=docs \
    --include-data-files=CHANGELOG.md=CHANGELOG.md \
    main.py
```

**Make sure to specify the version number in the command**

This produces a folder at dist/main.dist/ containing pearl-gui and all bundled libraries.

*Note: Nuitka builds can take significantly longer than PyInstaller. Assume 5-10 minutes to complete.*

## AppImage

To build an AppImage file, follow these steps after building the file with the previous command.

Install appimagetool if not already installed:
```
wget https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage

chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

**IMPORTANT: Set AppRun inside Pearl.AppDir as executable prior to building the AppImage**

Copy the entire contents of dist/main.dist/ to packaging/Pearl.AppDir/usr/bin:

```
# Copy built file to AppImage directory
mkdir -p packaging/Pearl.AppDir/usr/bin
cp -r dist/main.dist/* packaging/Pearl.AppDir/usr/bin/
```

Run this command from the app's root directory:
`appimagetool packaging/Pearl.AppDir Pearl-Linux.AppImage -v`

## DEBIAN

For a Debian (.deb) file, follow these steps after building the file with the command listed earlier (before the AppImage section).

Copy built file to deb directory:
```
mkdir -p packaging/deb/usr/lib/pearl-gui
cp -r dist/main.dist/* packaging/deb/usr/lib/pearl-gui/
```

Create the wrapper script:
```
mkdir -p packaging/deb/usr/bin
printf '#!/bin/sh\nexec /usr/lib/pearl-gui/pearl-gui "$@"\n' > packaging/deb/usr/bin/pearl-gui
```

Set permissions:
```
find packaging/deb -type d -exec chmod 755 {} +
find packaging/deb/DEBIAN -type f -exec chmod 755 {} +
find packaging/deb -type f ! -path "*/DEBIAN/*" -exec chmod 644 {} +
chmod 755 packaging/deb/usr/bin/pearl-gui
chmod 755 packaging/deb/usr/lib/pearl-gui/pearl-gui
```

Build DEB:
```
fakeroot dpkg-deb --build packaging/deb "Pearl-Linux-v0.4.1.deb"
```

Set permissions for .deb file:
```
chmod 644 "Pearl-Linux-v0.4.1.deb"
```

**Important: Make sure that you replace the version number properly to match the filename.**

## 🖥️ Windows

On Windows, Pearl can be built via Pyinstaller or Nuitka.

**IMPORTANT: Must have Visual Studio Build Tools installed with C++ / MSVC bindings**

**Python 3.13.15 recommended**

Open your IDE and create a virtual environment using these commands:

```
python -m venv pearl_venv

pearl_venv\Scripts\Activate.ps1
```

### Pyinstaller

To build via Pyinstaller, run this command to install dependencies and generate the file:

```
pip install -r packaging/requirements.txt

pyinstaller packaging/Pearl-Windows.spec --clean

```

### Nuitka

To build via Nuitka, run this command to install dependencies and generate the file:

```
pip install -r packaging/requirements.txt

nuitka `
    --msvc=latest `
    --standalone `
    --remove-output `
    --enable-plugin=pyside6 `
    --include-qt-plugins=platforms `
    --enable-plugin=tk-inter `
    --windows-console-mode=disable `
    --output-dir=dist `
    --windows-icon-from-ico=defaults/assets/pearl.ico `
    --include-package-data=pdf2image `
    --include-package-data=pytesseract `
    --include-package=pyttsx3.drivers `
    --include-data-dir=defaults=defaults `
    --include-data-dir=docs=docs `
    --include-raw-dir=bin=bin `
    --include-data-files=CHANGELOG.md=CHANGELOG.md `
    --file-version=0.4.1.0 `
    --product-version=0.4.1.0 `
    --company-name="Phillip Schneider" `
    --product-name="Pearl" `
    --file-description="Personal Everything Assistant Running Locally" `
    --copyright="Copyright © 2026 $AUTHOR. Apache 2.0." `
    --output-filename=Pearl.exe `
    main.py

```

**Make sure to update the product version and file version with the correct version number (e.g. 0.4.1.0).**

*Note: Nuitka builds can take significantly longer than Pyinstaller. Assume 5-10 minutes to complete.*

Pearl will be found in the dist/ folder.

---

That's it! If you have any questions or run into any errors, you can report them via GitHub issues or send me an email at bugs@phillipplays.com.

---

## Folder Structure (deb - inside packaging/)

``` bash
deb/
├── DEBIAN
├── etc
│   └── pearl-gui
└── usr
    ├── bin
    ├── lib
    │   └── pearl-gui
    └── share
        ├── applications
        ├── doc
        │   └── pearl-gui
        ├── icons
        │   └── hicolor
        │       ├── 128x128
        │       │   └── apps
        │       ├── 256x256
        │       │   └── apps
        │       └── scalable
        ├── pearl-gui
        ├── man
        │   └── man1
        ├── metainfo
        └── pixmaps

```

## Folder Structure (appimage - inside packaging/)

``` bash
Pearl/packaging/Pearl.AppDir/
├── AppRun                                    # AppImage entry point
├── io.github.pdschneider.pearl.desktop       # Desktop integration file
├── pearl.png                                 # App icon
└── usr/
    ├── bin/                                  # Compiled binary goes here during packaging
    └── share/
        ├── applications/
        │   └── io.github.pdschneider.pearl.desktop
        └── metainfo/
            └── io.github.pdschneider.pearl.appdata.xml

```

---

*Up to date as of v0.4.1*
