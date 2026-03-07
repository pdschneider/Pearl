# Utils/ollama.py
import requests
import time
import json
import logging
import socket
import subprocess
import threading
from datetime import datetime
from Utils.hardware import get_disk_space, get_ram_info
from Utils.toast import show_toast
from Utils.save_settings import save_settings
from tkinter import messagebox


def ollama_version_test(globals):
    """Tests Ollama only to see if it is installed."""
    try:
        # Set if Ollama version has already been displayed
        print_version = True if not globals.ollama_version else False

        # Run ollama --version in terminal
        version_test = subprocess.run("ollama --version", shell=True, capture_output=True, timeout=2)
        if version_test.returncode == 0:
            globals.ollama_version = version_test.stdout.decode('utf-8').strip().split()[3]
            if print_version:
                logging.info(f"Ollama Version: {globals.ollama_version}")
            return True
        else:
            globals.ollama_active = False
            return False

    # Gracefully return false on exceptions
    except Exception as e:
        logging.error(
            f"Ollama not installed or not active. Chat features unavailable. Error: {e}")
        globals.ollama_active = False
        return False


def ollama_test(globals):
    """Tests Ollama to set flag for active/inactive."""
    try:
        # Simple version test to start
        version = ollama_version_test(globals)
        if not version:
            logging.warning(f"Ollama not installed. Chat features unavailable.")
            return False

        # If Ollama is installed, test if active
        basic_test = subprocess.run("ollama ps", shell=True, capture_output=True, timeout=4)
        if basic_test.returncode == 0:
            socket.create_connection(("localhost", 11434), timeout=1).close()
            globals.ollama_active = True
            return True
        else:
            logging.warning(f"Ollama is installed but not running. Chat features unavailable.")
            return False

    # Gracefully return false on exceptions
    except Exception as e:
        logging.error(
            f"Ollama not installed or not active. Chat features unavailable. Error: {e}")
        return False


def pull_model(globals):
    """Downloads the default model if not present."""
    test = ollama_test(globals)

    # If Ollama is not installed, offer to install it
    if not test:
        logging.warning(f"Ollama must be installed before downloading a model.")
        download = messagebox.askyesno(
            parent=globals.root,
            title="Ollama Not Installed",
            message="Ollama does not appear to be installed. Would you like to install Ollama and the default model (llama3.2:latest)?")
        if download:
            ollama_installation(globals)
            return

    # If Ollama is installed, prompt to download llama3.2:latest
    else:
        # Ask user if they would like to download llama3.2:latest
        download = messagebox.askyesno(
            parent=globals.root,
            title="Model Not Installed",
            message="The selected model is not installed. Would you like to install the default model (llama3.2:latest)?")

        # Exit if user chooses no
        if not download:
            logging.warning(f"User chose not to install llama3.2:latest.")
            return

        # Check disk space to ensure at least 4GB
        free_space = get_disk_space()['free_disk']
        logging.debug(f"Free disk space: {free_space}")
        if free_space < 4:
            logging.warning(f"Free disk space must be at least 4GB to install llama3.2.")
            show_toast(globals, message="Must have 4GB of free disk space to install Ollama", _type="error")
            return

        # Check available RAM to ensure at least 4GB
        free_ram = get_ram_info()['avail_ram_gb']
        if free_ram < 4:
            logging.warning(f"Available RAM must be at least 4GB to install llama3.2.")
            show_toast(globals, message="Must have 4GB of available RAM to install llama3.2", _type="error")
            return

        # Download llama3.2:latest on Linux
        if globals.os_name.startswith("Linux"):
            download_cmd = """
            #!/bin/bash

            set -euo pipefail

            read -p "Install recommended model (llama3.2:latest)? [Y/n] " choice
            if [[ "$choice" =~ ^[Yy]?$ ]]; then
                ollama pull llama3.2:latest
                echo "llama3.2:latest was installed!"
                echo ""
                echo 'Install finished! Press Enter to close this terminal and return to Pearl...';
                read -r dummy
                exit 0
            else
                echo "Skipping model install."
                echo ""
                read -r dummy
                exit 0
            fi
            """
            subprocess.Popen([
                "gnome-terminal",
                "--",
                "bash", "-c",
                f"{download_cmd}"
            ])
        elif globals.os_name.startswith("Windows"):
            download_cmd = (
                # Ask about model (Y/n like bash)
                "$choice = Read-Host 'Install recommended model llama3.2:latest? [Y/n]'; "
                "if ($choice -eq '' -or $choice -match '^[Yy]') { "
                "    Write-Host 'Pulling llama3.2:latest ... (may take a few minutes)' -ForegroundColor Cyan; "
                "    ollama pull llama3.2:latest; "
                "    Write-Host 'Model installed!' -ForegroundColor Green; "
                "} else { "
                "    Write-Host 'Skipping model download.' -ForegroundColor Yellow; "
                "}; "

                # Final message
                "Write-Host ''; "
                "Write-Host 'All done! Press Enter to close this window...'; "
                "Read-Host"
                )
        else:
            logging.warning(f"Only Windows and Linux are supported for model downloads.")
            messagebox.showinfo("OS Not Supported", message="Only Windows and Linux are supported for model downloads. Install models on Ollama.com instead.")


def ollama_installation(globals):
    """Install Ollama and any desired models."""
    # Do an initial check to see if Ollama is already installed.
    test = ollama_version_test(globals)
    if test:
        logging.warning(f"Ollama is already active and running. No need to install.")
        messagebox.showinfo("Ollama Already Installed", message="Ollama is already active and running. No need to install!")
        return

    # Check disk space to ensure at least 10GB
    free_space = get_disk_space()['free_disk']
    logging.debug(f"Free disk space: {free_space}")
    if free_space < 10:
        logging.warning(f"Free disk space must be at least 10GB to install Ollama.")
        show_toast(globals, message="Must have 10GB of free disk space to install Ollama", _type="error")
        return

    # Install Ollama on Linux
    if globals.os_name.startswith("Linux"):
        subprocess.Popen([
            "gnome-terminal",
            "--",
            "bash", "-c",
            f"{globals.ollama_sh}"
        ])

    # Install on Windows
    elif globals.os_name.startswith("Windows"):
        ps_command = (
    # Download + install Ollama
    "irm https://ollama.com/install.ps1 | iex; "

    # Small pause so output settles
    "Start-Sleep -Milliseconds 1500; "

    # Check if ollama works (basic smoke test)
    "if (Get-Command ollama -ErrorAction SilentlyContinue) { "
    "    Write-Host 'Ollama is installed and in PATH.' -ForegroundColor Green; "
    "} else { "
    "    Write-Host 'Warning: ollama command not found yet. Try reopening terminal.' -ForegroundColor Yellow; "
    "}; "

    # Ask about model (Y/n like bash)
    "$choice = Read-Host 'Install recommended model llama3.2:latest? [Y/n]'; "
    "if ($choice -eq '' -or $choice -match '^[Yy]') { "
    "    Write-Host 'Pulling llama3.2:latest ... (may take a few minutes)' -ForegroundColor Cyan; "
    "    ollama pull llama3.2:latest; "
    "    Write-Host 'Model installed!' -ForegroundColor Green; "
    "} else { "
    "    Write-Host 'Skipping model download.' -ForegroundColor Yellow; "
    "}; "

    # Final message
    "Write-Host ''; "
    "Write-Host 'All done! Press Enter to close this window...'; "
    "Read-Host"
)

        cmd_line = (
            'start "" powershell.exe '
            '-NoProfile '
            '-ExecutionPolicy Bypass '
            # '-NoExit ' would prevent the window from closing on Enter
            f'-Command "{ps_command}"'
        )

        subprocess.Popen(cmd_line, shell=True)
    else:
        logging.warning(f"Only Windows and Linux are supported for interactive install.")
        messagebox.showinfo("OS Not Supported", message="Only Windows and Linux are supported for interactive install. Use the web installer instead.")
    
    # Test again to see if it worked
    test = ollama_version_test(globals)
    if test:
        logging.info(f"Ollama was successfully installed!")
    else:
        logging.warning(f"Ollama does not appear to be installed.")


def uninstall_ollama(globals):
    """Fully uninstalls Ollama."""
    # Test if Ollama is actually installed
    ollama_installed = ollama_version_test(globals)

    # If Ollama is not installed, skip
    if not ollama_installed:
        logging.warning(f"Ollama not installed — no need to uninstall.")
        show_toast(globals, message="Ollama not installed — no need to uninstall")
        return

    if globals.os_name.startswith("Linux"):
        uninstall_cmd = (
            """
            echo "Uninstalling Ollama..."
            sudo systemctl stop ollama 2>/dev/null
            sudo systemctl disable ollama 2>/dev/null
            sudo rm -f /etc/systemd/system/ollama.service
            sudo systemctl daemon-reload
            sudo rm $(which ollama) 2>/dev/null
            sudo rm -r $(which ollama | tr 'bin' 'lib') 2>/dev/null || true
            sudo rm -rf /usr/share/ollama
            echo "Ollama uninstalled! Press Enter to close this terminal and return to Pearl..."
            read -r dummy
            exit 0
            """)
        subprocess.Popen([
            "gnome-terminal",
            "--",
            "bash", "-c",
            f"{uninstall_cmd}"
        ])
    elif globals.os_name.startswith("Windows"):
        logging.debug(f"Opening Windows uninstall program window...")
        subprocess.run("start appwiz.cpl", shell=True)
    else:
        logging.warning(f"Uninstall only supported on Linux and Windows.")
        show_toast(globals, message="Uninstall only supported on Linux and Windows.", _type="error")


def get_all_models(globals):
    """Fetch list of available model names from Ollama API"""
    # Gracefully exit if Ollama is not installed
    if not globals.ollama_active:
        return

    try:
        # Test that Ollama is installed first
        test = ollama_version_test(globals)
        if not test or not globals.ollama_active:
            logging.warning(f"Unable to retrieve models - Ollama not installed.")
            return []

        # Query Ollama for current models
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            data = response.json()
            logging.debug(f"ALL MODELS: {list(set(model["name"] for model in data.get("models", [])))}")
            return list(set(model["name"] for model in data.get("models", [])))
        return []
    except Exception as e:
        logging.error(f"Error fetching models: {e}")
        return []


def get_loaded_models(globals):
    """Fetch list of currently loaded models from Ollama API"""
    # Gracefully exit if Ollama is not installed
    if not globals.ollama_active:
        return

    try:
        # Test that Ollama is installed first
        test = ollama_version_test(globals)
        if not test or not globals.ollama_active:
            logging.warning(f"Unable to retrieve models - Ollama not installed.")
            return []

        # Query Ollama for loaded models
        response = requests.get("http://localhost:11434/api/ps")
        if response.status_code == 200:
            data = response.json()
            logging.debug(f"LOADED MODELS: {[model["name"] for model in data.get("models", [])]}")
            return [model["name"] for model in data.get("models", [])]
        return []
    except Exception as e:
        logging.error(f"Error fetching loaded models: {e}")
        return []


def load_model(globals, model):
    """Load a model into memory with a 20-second timeout."""
    # Gracefully exit if Ollama is not installed
    if not globals.ollama_active:
        return

    def _load_in_thread(globals, model):
        """Loads the model in a thread to speed up start time & GUI."""
        payload = {"model": model,
               "prompt": "",
               "stream": False,
               "keep_alive": "30m"}
        try:
            response = requests.post(
                "http://localhost:11434/api/generate", json=payload, timeout=4)
            logging.debug(
                f"Sent request to {model}. Response code: {response.status_code}")
            if response.status_code == 200:
                start_time = time.time()
                while time.time() - start_time < 20:
                    if model in get_loaded_models(globals):
                        logging.info(f"{model} loaded!")
                        return True
                    time.sleep(1)
                logging.info(f"Timeout loading {model}")
                return False
        except Exception as e:
            logging.error(f"Failed to load {model}: {e}")
            return False
    
    threading.Thread(target=lambda: _load_in_thread(globals, model), daemon=True).start()


def unload_model(model):
    """Unload a model from memory"""
    # Gracefully exit if Ollama is not installed
    if not globals.ollama_active:
        return

    payload = {"model": model, "prompt": "", "keep_alive": 0, "stream": False}
    try:
        response = requests.post(
            "http://localhost:11434/api/generate", json=payload)
        if response.status_code == 200:
            start_time = time.time()
            while time.time() - start_time < 10:
                if model not in get_loaded_models():
                    logging.info(f"Unloaded {model}")
                    return True
                time.sleep(0.5)
            logging.info(f"Timeout unloading {model}")
            return False
    except Exception as e:
        logging.error(f"Failed to unload {model}: {e}")
        return False


def chat_stream(globals, model, messages, out_q, cancel_event):
    """
    Stream response from Ollama using the proper /chat endpoint.

    messages = list of dicts:
    [{"role": "user"|"assistant"|"system", "content": "..."}, ...]
    """
    # Gracefully exit if Ollama is not installed
    if not globals.ollama_active:
        return

    if globals.active_prompt:
        messages_and_prompt = [
            {"role": "system", "content": globals.system_prompt}] + messages
    if messages_and_prompt:
        messages = messages_and_prompt

    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": True}
    try:
        # Test Ollama first
        ollama_installed = ollama_version_test(globals)

        # Exit gracefully if Ollama is not installed
        if not ollama_installed:
            logging.warning(f"Ollama must be installed to use Pearl's chat feature.")
            out_q.put(
                    f"Ollama must be installed to use Pearl's chat feature.")
            got_response = False
            return

        # Query the Ollama API if Ollama is installed, set flag
        response = requests.post(url, json=payload, stream=True, timeout=30)
        if response:
            got_response = True

        # Prompt to download default model on 404
        if response.status_code == 404:
            logging.error(f"Error: {response.text}")
            absent_model = response.text.split()[1].replace("'", "")
            if absent_model == "llama3.2:latest":
                pull_model(globals)
                out_q.put(
                    f"At least one model must be installed to use Pearl's chat feature.")
                return
            else:
                out_q.put(
                    f"{absent_model} not found. Defaulting to llama3.2:latest.")
                globals.active_model = "llama3.2:latest"
                save_settings(active_model="llama3.2:latest")
                return

        # Gracefully return if status code is not 200
        if response.status_code != 200:
            out_q.put(
                f"Ollama error {response.status_code}: {response.text}\n")
            return

        # Output text in a stream
        for line in response.iter_lines():
            # Cancel output if cancel event is set
            if cancel_event.is_set():
                logging.debug(
                    f"Cancel event triggered during Ollama chat stream.")
                globals.message_end_time = datetime.now().isoformat()
                out_q.put(None)
                # Close only if response was given
                if got_response:
                    response.close()
                return
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    if chunk.get("done"):
                        break
                    out_q.put(chunk["message"]["content"])
                except json.JSONDecodeError:
                    continue
        logging.debug(f"{model} has finished streaming its response.")
    except requests.ConnectionError:
        out_q.put("Cannot reach Ollama — is it running?\n")
    except requests.Timeout:
        out_q.put("Ollama timed out\n")
    except Exception as e:
        out_q.put(f"Error: {e}\n")
    finally:
        globals.message_end_time = datetime.now().isoformat()
        out_q.put(None)
        # Close only if response was given
        if got_response:
            response.close()


def context_query(globals, model="llama3.2:latest", message=""):
    """Query the context model for changes in the conversation."""
    # Gracefully exit if Ollama is not installed or message is empty
    if not globals.ollama_active or not message:
        return

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": f"Based on this list, determine the best context of the message and return ONLY the word. Nothing else: 'Assistant', 'Therapist', 'Financial', 'Storyteller', 'Conspiracy', 'Meditation', 'Motivation'. The message: ' {message}",
            "stream": False},
            timeout=10)
        logging.debug(f"Context model status code: {response.status_code}")

        # Exit on failure
        if response.status_code != 200:
            logging.error(f"Context Query Failed | Status Code: {response.status_code}")
            return

        # Return response on success
        return response.json()["response"]

    except Exception as e:
        logging.error(f"Could not query context model due to: {e}")


def get_model_info(model):
    """Gets detailed model information for a specific model."""
    # Gracefully exit if Ollama is not installed
    if not globals.ollama_active:
        return

    empty_dict = {
        "architecture": "",
        "parameter_count": 0,
        "parameters": "Unknown",
        "embedding_length": "Unknown",
        "embedding_length_num": 0,
        "context_length": "Unknown",
        "context_length_num": 2048,
        "system_prompt": "No system prompt defined",
        "family": "Unknown"}
    try:
        response = requests.post(
            f"http://localhost:11434/api/show", json={"name": model}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            model_info = data.get("model_info", {})
            arch = model_info.get("general.architecture", "").lower()
            param_count = model_info.get("general.parameter_count", 0)
            params_str = "Unknown"
            if param_count > 0:
                if param_count > 1e12:
                    params_str = f"{param_count / 1e12:.1f}T"
                elif param_count > 1e9:
                    params_str = f"{param_count / 1e9:.1f}B"
                elif param_count > 1e6:
                    params_str = f"{param_count / 1e6:.1f}M"
                else:
                    params_str = str(param_count)
            embed_key = f"{arch}.embedding_length" if arch else ""
            embed_str = model_info.get(embed_key, "Unknown")
            embed_num = int(embed_str) if embed_str != "Unknown" else 0
            ctx_key = f"{arch}.context_length" if arch else ""
            ctx_str = model_info.get(ctx_key, "Unknown")
            ctx_num = int(ctx_str) if ctx_str != "Unknown" else 2048
            modelfile = data.get("modelfile", "")
            system_prompt = _extract_system(modelfile)
            return {
                "architecture": arch,
                "parameter_count": param_count,
                "parameters": params_str,
                "embedding_length": embed_str,
                "embedding_length_num": embed_num,
                "context_length": ctx_str,
                "context_length_num": ctx_num,
                "system_prompt": system_prompt,
                "family": data.get("details", {}).get(
                    "family", "Unknown").capitalize()
            }
        logging.warning(
            f"Failed to fetch model info for {model}, status code: {response.status_code}, response: {response.text}")
        return empty_dict
    except Exception as e:
        logging.error(f"Error fetching model info for {model}: {e}")
        return empty_dict


def _extract_system(modelfile):
    """Extracts the system prompt from model details"""
    # Gracefully exit if Ollama is not installed
    if not globals.ollama_active:
        return

    lines = modelfile.splitlines()
    system_lines = []
    in_system = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("SYSTEM"):
            in_system = True
            content = line[line.find("SYSTEM") + 6:].strip()
            if content:
                system_lines.append(content)
            continue
        if in_system:
            if stripped and stripped.split()[0].isupper() and ' ' in stripped:
                break
            system_lines.append(line.strip())
    return '\n'.join(system_lines).strip() or "No system prompt defined"
