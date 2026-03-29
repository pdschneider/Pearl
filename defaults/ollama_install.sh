#!/bin/bash

set -euo pipefail

echo ""
echo "=============================================================="
echo "               Ollama Installation for Pearl                  "
echo "=============================================================="
echo ""

# Exits if Ollama is already installed
if command -v ollama >/dev/null 2>&1; then
    echo "Ollama is already installed."
    echo ""
    read -n1 -r -p "Press any key to exit..."
    exit 0
fi

echo "This command will be run to install Ollama:"
echo "curl -fsSL https://ollama.com/install.sh | sh"
echo ""
echo 'Press Enter to install Ollama (you will need to enter your sudo password)...';
read -p '> ' dummy

curl -fsSL https://ollama.com/install.sh | sh

NEEDSFIX=true

# Fix common permission issue if present
if ollama ps >/dev/null 2>&1; then
    NEEDSFIX=false
else
    echo "Setting up persistent Ollama server..."
fi

echo ""

if [ "$NEEDSFIX" = "true" ]; then
    echo "Fixing /usr/share/ollama permission error..."
    sudo systemctl stop ollama 2>/dev/null || true
    sudo mkdir -p /usr/share/ollama/.ollama 2>/dev/null || true
    sudo chown -R ollama:ollama /usr/share/ollama 2>/dev/null || true
    sudo systemctl start ollama 2>/dev/null || true

    sleep 2
fi

if ollama ps >/dev/null 2>&1; then
    NEEDSFIX=false
else
    echo "Installation was not fully successful - troubleshoot at ollama.com"
    read -r dummy
    exit 0
fi

read -p "Install recommended model (llama3.2:latest)? [Y/n] " choice
if [[ "$choice" =~ ^[Yy]?$ ]]; then
    ollama pull llama3.2:latest
    echo "llama3.2:latest was installed!"
    echo ""
else
    echo "Skipping model install."
    echo ""
fi

echo 'Install finished! Press Enter to close this terminal and return to Pearl...';
read -r dummy
exit 0
