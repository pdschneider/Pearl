# 📖 How to Use Pearl

Pearl is a local AI chat app that utilizes Ollama for fully offline chats after installation.

This guide walks you through the main workflow and features.

## Getting Started

1. **Launch Pearl**  
   Run the built executable (`Pearl.exe` on Windows or `Pearl.AppImage` on Linux).

2. **Complete the Onboarding (first time only)**  
   The setup wizard will guide you through:
   - Installing Ollama + a model
   - Installing Docker
   - Installing Kokoro

3. **Main Screen Overview**  
   - **Chat area**: Shows the main chat space for message bubbles
   - **Input area**: Contains the input box with send and attach buttons
   - **Top menu**: Access to Settings, History, New Chats, and Bug Reports

## Settings

Open Settings from the top menu button. Key areas include:

- **General Settings** — Select theme and other general settings
- **Models** — Select your active model for chats, context, and title generation
- **Sound** — Enable/Disable TTS and select the source, voice, and speaker output
- **Networking** — Determine where Pearl queries Ollama (default is localhost)
- **Advanced** — Change logging level, open key folders, factory reset configuration and uninstall dependencies
- **About** — View version number, changelog, GitHub, and open wizard

## Tips for Best Results

- Use the best model that fits your current hardware (GPU-enabled PC's with AI support can handle more powerful models)
- Ensure attached files are relatively short in length
- Keep 'Generate Chat Titles' options checked for the best experience
- Avoid 'reasoning' or 'thinking' models as output can take a very long time to appear or format strangely

## Troubleshooting

- **Output is slow** → Choose a smaller model or close other open processes
- **Pearl doesn't respond** → Make sure that Ollama is installed and running with a compatible model (for the best experience use the built in installer script in the onboarding page/wizard). Sometimes, updating Ollama and restarting your PC fixes it.
- **Pearl is slow to start** → Try deleting old chats via Settings > General > Delete All Chats
- **TTS sounds robotic** → For enhanced TTS, Docker + Kokoro must be installed (found in wizard/onboarding page)
- **Pearl is slow in long conversations** → Start a new conversation or switch to a smaller model
- **Pearl crashes on startup or does not open** → Reinstall Pearl - if that doesn't work, open a GitHub issue or email bugs@phillipplays.com
- **I don't see the app anywhere after installation** → Open a terminal and enter "pearl-gui" - if that doesn't work, reinstall or open a GitHub issue

## Privacy & Safety

- All processing happens on your computer — no user data is sent online unless configured
- After initial installation, if Check for Updates is turned on the app will contact GitHub at startup for new updates
- For Windows users, upon launch, the app will make a request to SSL.com + your system's DNS resolver to verify that the certificate is valid

## Disclaimer

You are responsible for verifying all AI outputs - the developer and contributors are not responsible for the use of this app.

---

**Maintained by**: Phillip Schneider

Questions or suggestions? Open an issue on the [GitHub repository](https://github.com/pdschneider/InvoiceBuddy).
