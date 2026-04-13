
# 🚀 How to Build

Pearl can be built from source code via Pyinstaller on both Windows and Linux and Nuitka on Linux. This is for advanced users only - the simplest way to run Pearl is to download the latest release.

## 🐧 Linux

1. Open your IDE (VSCode recommended) and create a virtual environment using these commands:

```
python3 -m venv pearl_venv

source pearl_venv/bin/activate
```

2. Run these commands to install dependencies and generate the file:

**IMPORTANT: Must have patchelf installed: `sudo apt patchelf`**

Install appimagetool if not already installed:
```
wget https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage

chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

```
pip install -r packaging/requirements.txt

nuitka \
    --standalone \
    --onefile \
    --remove-output \
    --output-dir=dist \
    --enable-plugin=pyside6 \
    --enable-plugin=tk-inter \
    --include-qt-plugins=platforms,iconengines,imageformats \
    --include-package=pyttsx3.drivers \
    --include-data-dir=defaults=defaults \
    --include-data-files=CHANGELOG.md=CHANGELOG.md \
    --include-data-files=README.md=README.md \
    --include-data-files=LICENSE.txt=LICENSE.txt \
    pearl.py
```

3. **IMPORTANT: Set AppRun inside Pearl.AppDir as executable prior to building the AppImage**

4. Copy pearl.bin from dist/ to packaging/Pearl.AppDir/usr/bin

5. Run this command from the app's root directory:
`appimagetool packaging/Pearl.AppDir Pearl-Linux.AppImage -v`

## 🖥️ Windows

On Windows, Pearl should be built via Pyinstaller to bypass Windows Defender false positives. Nuitka works, but is more difficult to get working.

**IMPORTANT: Must have Visual Studio Build Tools installed with C++ / MSVC bindings**

**Python 3.10+ recommended**

Open your IDE (VSCode recommended) and create a virtual environment using these commands:

```
python -m venv pearl_venv

pearl_venv\Scripts\Activate.ps1
```

### Pyinstaller

To build via Pyinstaller (recommended), run this command to install dependencies and generate the file:

```
pip install -r packaging/requirements.txt

pyinstaller packaging/Pearl-Windows.spec --clean

```

### Nuitka

To build via Nuitka, run this command to install dependencies and generate the file:

```
pip install -r packaging/requirements.txt

nuitka --standalone --msvc=latest --onefile --remove-output --enable-plugin=pyside6 --include-qt-plugins=platforms --enable-plugin=tk-inter --windows-disable-console --output-dir=dist --include-package=pyttsx3.drivers --windows-icon-from-ico=defaults/assets/pearl.ico --include-data-dir=defaults=defaults --include-data-files=CHANGELOG.md=CHANGELOG.md --include-data-files=README.md=README.md pearl.py

```

*Note: Nuitka builds can take significantly longer than Pyinstaller. Assume 5-10 minutes to complete.*

Pearl will be found in the dist/ folder.

That's it! If you have any questions or run into any errors, you can report them via GitHub issues or send me an email at bugs@phillipplays.com.
