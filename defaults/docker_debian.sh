#!/bin/bash

set -euo pipefail

echo ""
echo "=============================================================="
echo "               Docker Installation for Pearl                  "
echo "=============================================================="
echo ""

# Exits if Docker is already installed
if command -v docker >/dev/null 2>&1; then
    echo "Docker is already installed."
    echo ""
    read -n1 -r -p "Press any key to exit..."
    exit 0
fi

echo "This installer is for Debian-based systems only."
echo ""
echo ""
echo 'Press Enter to install Docker (you will need to enter your sudo password)...';
read -p '> ' dummy

# Remove conflicting packages
echo "Removing conflicting packages if present..."
sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-doc podman-docker containerd runc | cut -f1)
echo ""

# Add Docker's official GPG key:
echo "Updating repositories and adding official Docker GPG key..."
sudo apt update || echo "Warning: apt update had warnings/errors — continuing anyway"
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo ""

# Add the repository to Apt sources:
echo "Adding Docker repository to apt sources..."
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF
echo ""
read -r -p 'Press Enter to Continue...'

# Update
echo "Updating repositories..."
sudo apt update || echo "Warning: apt update had warnings/errors — continuing anyway"
echo ""

# Install Docker
echo "Installing Docker..."
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
echo ""

# Verify Docker is running, start if not
echo "Verifying that Docker is running..."
if ! sudo systemctl is-active --quiet docker; then
    echo "Docker isn’t running – starting it now…"
    sudo systemctl start docker
    # Optional: verify it started successfully
    if sudo systemctl is-active --quiet docker; then
        echo "✅ Docker started successfully."
    else
        echo "❌ Failed to start Docker. Check the logs with:"
        echo "   sudo journalctl -u docker"
        exit 1
    fi
fi

# Configure docker to start on boot
echo "Configuring Docker to start on boot..."
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
echo ""

# Granting user-level access
echo "Would you like to grant user level access to Docker (recommended)?"
read -p "This makes it easier for Pearl to correctly detect when Docker is running. [Y/n] " choice
if [[ "$choice" =~ ^[Yy]?$ ]]; then
    sudo groupadd -f docker
    sudo usermod -aG docker $USER
    echo "Docker was successfully granted user access!"
    echo "You may need to restart your PC for this to take effect."
    echo ""
else
    echo "Skipping..."
    echo ""
fi

# Give prompt and exit
echo 'Install finished! Press Enter to close this terminal and return to Pearl...';
read -r dummy
exit 0
