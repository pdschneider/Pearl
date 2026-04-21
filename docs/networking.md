# 🌐 Pearl Networking Setup (Linux)

This is a guide for setting up Pearl to use other Ollama-compatible devices on LAN to perform specific tasks, such as context detection and title generation. The guide is currently for Linux systems only.

## 🖧 Configure Ollama on the Server
Run these commands on the machine hosting Ollama, not the one running Pearl:

Install Ollama if not already installed:
```
curl -fsSL https://ollama.com/install.sh | sh
```

Stop Ollama and edit its configuration file:
```
sudo systemctl stop ollama
sudo systemctl edit ollama
```

Paste this between lines 2-4:
```
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
```

Restart Ollama:
```
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

Open Ollama's port for LAN access:
```
sudo ufw allow from 192.168.0.0/16 to any port 11434 comment "Ollama on LAN"
```

*Note: this IP configuration is for small office home office (SOHO) setups - if on a corporate network, your IP may be different.*

Verify: from host PC running Pearl, try:
```
curl http://<Host IP Address>:11434/
```

**IMPORTANT: You will need the IP address of the host PC. One way to find it is via network configuration at your default gateway (http://192.168.1.1). It is recommended that you also set a static IP for the host PC running Ollama to ensure Pearl can reach it after a reboot.**

If it returns "Ollama is running", success!

*Note: If the command fails, submit a bug report to bugs@phillipplays.com or open a GitHub issue.*

Finally, open Pearl, head to `Settings > Networking`, and input `http://<Host IP Address>:11434/` for whichever function you want the secondary PC to handle.

Congratulations, you are now networking with Pearl!
