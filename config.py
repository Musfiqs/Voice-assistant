"""
Configuration file for the Voice Assistant application.
Store your OpenAI API key and other settings here.
"""

import os

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
OPENAI_MODEL = "gpt-4"

# App Configuration
APP_TITLE = "Futuristic Voice Assistant"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
BACKGROUND_COLOR = "#1a1a1a"  # Matte black
PRIMARY_COLOR = "#00ffff"     # Cyan/blue-green
SECONDARY_COLOR = "#808080"   # Light gray
ACCENT_COLOR = "#ff6b6b"      # Red accent

# Animation Configuration
CIRCLE_RADIUS = 100
PULSE_SPEED = 0.05
ROTATION_SPEED = 1.0

# Voice Configuration
VOICE_MODES = {
    "Male": {"rate": 200, "pitch": 0.5},
    "Female": {"rate": 180, "pitch": 0.8},
    "Alien": {"rate": 150, "pitch": 0.3}
}

# Audio Configuration
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024 