# 🎤 ARIA Voice Assistant

A futuristic AI voice assistant with a dark-themed GUI, built with Python. Features both demo mode and real OpenAI integration.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 🛡️ **Safe Mode**: Stable operation without TTS crashes
- 🤖 **AI Integration**: OpenAI GPT-3.5 support (optional)
- 🎭 **Voice Modes**: Male, Female, and Alien voice simulation
- 🌙 **Dark Theme**: Futuristic cyberpunk-style interface
- 💬 **Conversation History**: Full chat logging
- 🔐 **Secure**: No hardcoded API keys

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/voice-assistant.git
   cd voice-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python demo_safe.py
   ```

## 🎮 Usage

### Safe Mode (Recommended)
```bash
python demo_safe.py
```
- ✅ Stable operation
- 🗣️ Speech output in console
- 🎭 Full UI functionality
- 🤖 Optional OpenAI integration

### With Audio (Experimental)
```bash
python demo_tkinter.py
```
- 🔊 Real text-to-speech
- ⚠️ May crash on some systems

### Animated Version (PyQt6)
```bash
python demo.py
```
- 🎬 Holographic animated circle
- ⚠️ Requires PyQt6 platform support

## 🤖 AI Integration

To use real OpenAI responses:

1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. In the running application, paste your key in the "OpenAI API Key" field
3. Click "Enable Real AI"
4. Enjoy intelligent conversations!

## 📁 Project Structure

```
voice-assistant/
├── demo_safe.py          # Main safe application
├── demo_tkinter.py       # Audio-enabled version
├── demo.py              # PyQt6 animated version
├── demo_pyside.py       # PySide6 alternative
├── main_window.py       # Main PyQt6 GUI
├── animated_circle.py   # Holographic circle widget
├── voice_engine.py      # Speech recognition/TTS
├── ai_assistant.py      # OpenAI integration
├── config.py           # Configuration settings
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## 🛠️ Dependencies

- `tkinter` - GUI framework (built-in)
- `openai` - OpenAI API client
- `pyttsx3` - Text-to-speech (optional)
- `PyQt6` - Advanced GUI (optional)
- `PySide6` - Qt alternative (optional)

## 🎭 Voice Modes

- **Male**: Standard voice with normal speed
- **Female**: Higher pitch, slightly faster
- **Alien**: Slower, robotic voice simulation

## 🔐 Security

- No API keys stored in code
- Manual API key entry required
- Virtual environment isolation
- Secure credential handling

## 🐛 Troubleshooting

### Audio Issues
- Use `demo_safe.py` for guaranteed stability
- Check console for speech output
- Ensure `pyttsx3` is installed for audio

### PyQt6 Issues
- Try `demo_pyside.py` as alternative
- Install platform-specific Qt packages
- Use `demo_safe.py` as fallback

### API Errors
- Check OpenAI account quota
- Verify API key validity
- Demo mode works without API key

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-3.5 API
- Qt Project for GUI frameworks
- Python community for excellent libraries

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Try `demo_safe.py` for guaranteed operation
3. Open an issue on GitHub

---

**Built with ❤️ and Python** 