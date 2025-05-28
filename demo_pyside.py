#!/usr/bin/env python3
"""
Demo version of the Futuristic Voice Assistant using PySide6.
This version works without an OpenAI API key for testing the GUI.
"""

import sys
import time
import random
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("pyttsx3 not available - audio will be simulated")

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QTextEdit, QCheckBox, QLineEdit
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont

from config import *

class DemoAIAssistant:
    """Demo AI assistant with pre-programmed responses."""
    
    def __init__(self):
        self.responses = [
            "Hello! I'm ARIA, your futuristic voice assistant. This is a demo version!",
            "I'm working perfectly! The holographic interface is quite stunning, isn't it?",
            "In this demo, I can show you how the voice assistant interface works.",
            "The animated circle represents my consciousness. Pretty cool, right?",
            "This futuristic design showcases what's possible with modern UI technology.",
            "I would normally be powered by GPT-4, but this demo works offline!",
            "You can test different voice modes using the dropdown above.",
            "The conversation history keeps track of our entire discussion.",
            "Thank you for trying out this futuristic voice assistant demo!"
        ]
        self.response_index = 0
    
    def get_response(self, user_input, callback=None):
        """Get a demo response after a delay."""
        # Use QTimer instead of QThread for simplicity
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self._deliver_response(callback))
        timer.start(2000)  # 2 second delay
        return timer
    
    def _deliver_response(self, callback):
        """Deliver the response via callback."""
        response = self.responses[self.response_index % len(self.responses)]
        self.response_index += 1
        if callback:
            callback(response, None)
    
    def clear_conversation(self):
        """Reset response index."""
        self.response_index = 0

class DemoVoiceEngine:
    """Demo voice engine that simulates speech recognition and includes real TTS."""
    
    def __init__(self):
        self.current_voice_mode = "Male"
        self.is_listening = False
        self.is_speaking = False
        self.audio_enabled = TTS_AVAILABLE
        
        # Initialize TTS engine if available
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self._configure_voice()
            except Exception as e:
                print(f"TTS initialization failed: {e}")
                self.audio_enabled = False
                self.tts_engine = None
        else:
            self.tts_engine = None
        
        self.demo_phrases = [
            "Hello ARIA, how are you today?",
            "Can you tell me about this demo?",
            "What features do you have?",
            "This interface looks amazing!",
            "How does the voice recognition work?",
            "Show me the different voice modes",
            "What can you help me with?",
            "This is a great demonstration!"
        ]
        self.phrase_index = 0
    
    def _configure_voice(self):
        """Configure the TTS voice based on current mode."""
        if not self.tts_engine:
            return
            
        voices = self.tts_engine.getProperty('voices')
        if not voices:
            return
            
        # Configure voice based on mode
        if self.current_voice_mode == "Female":
            # Try to find a female voice
            for voice in voices:
                if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            self.tts_engine.setProperty('rate', 180)  # Slightly faster
            
        elif self.current_voice_mode == "Male":
            # Try to find a male voice (usually default)
            for voice in voices:
                if 'male' in voice.name.lower() or 'man' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            else:
                # Use first available voice if no male found
                if voices:
                    self.tts_engine.setProperty('voice', voices[0].id)
            self.tts_engine.setProperty('rate', 170)  # Normal speed
            
        elif self.current_voice_mode == "Alien":
            # Use any available voice with alien-like settings
            if voices:
                self.tts_engine.setProperty('voice', voices[-1].id)  # Use last voice
            self.tts_engine.setProperty('rate', 140)  # Slower, more robotic
            
        # Set volume
        self.tts_engine.setProperty('volume', 0.8)
    
    def set_voice_mode(self, mode):
        """Set the voice mode."""
        self.current_voice_mode = mode
        self._configure_voice()
    
    def set_audio_enabled(self, enabled):
        """Enable or disable audio output."""
        self.audio_enabled = enabled and TTS_AVAILABLE and self.tts_engine is not None
    
    def listen_for_speech(self, callback=None):
        """Simulate speech recognition."""
        self.is_listening = True
        
        # Use QTimer instead of QThread
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self._deliver_speech(callback))
        timer.start(3000)  # 3 second delay
        return timer
    
    def _deliver_speech(self, callback):
        """Deliver the recognized speech via callback."""
        text = self.demo_phrases[self.phrase_index % len(self.demo_phrases)]
        self.phrase_index += 1
        self.is_listening = False
        if callback:
            callback(text, None)
    
    def speak(self, text, callback=None):
        """Speak text using real TTS or simulate."""
        self.is_speaking = True
        
        if self.audio_enabled and self.tts_engine:
            # Use real TTS
            try:
                # Run TTS in a separate thread to avoid blocking UI
                def speak_thread():
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                    self.is_speaking = False
                    if callback:
                        # Use QTimer to safely call callback from main thread
                        QTimer.singleShot(0, callback)
                
                import threading
                thread = threading.Thread(target=speak_thread)
                thread.daemon = True
                thread.start()
                
            except Exception as e:
                print(f"TTS error: {e}")
                # Fall back to simulation
                self._simulate_speaking(text, callback)
        else:
            # Simulate speaking
            self._simulate_speaking(text, callback)
    
    def _simulate_speaking(self, text, callback):
        """Simulate text-to-speech with timer."""
        speaking_time = max(2000, len(text) * 100)  # milliseconds
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self._finish_speaking(callback))
        timer.start(speaking_time)
        return timer
    
    def _finish_speaking(self, callback):
        """Finish speaking simulation."""
        self.is_speaking = False
        if callback:
            callback()
    
    def stop_speaking(self):
        """Stop speaking."""
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass
        self.is_speaking = False

class DemoVoiceAssistantApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize demo components
        self.voice_engine = DemoVoiceEngine()
        self.ai_assistant = DemoAIAssistant()
        
        # Initialize UI
        self.init_ui()
        self.setup_connections()
        
        # Show welcome message
        QTimer.singleShot(1000, self.show_welcome_message)
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(f"{APP_TITLE} - DEMO MODE (PySide6)")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Set window style (same as main app)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {BACKGROUND_COLOR};
            }}
            QWidget {{
                background-color: {BACKGROUND_COLOR};
                color: {SECONDARY_COLOR};
                font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            }}
            QLabel {{
                color: {SECONDARY_COLOR};
                font-size: 14px;
            }}
            QComboBox {{
                background-color: #2a2a2a;
                border: 2px solid {PRIMARY_COLOR};
                border-radius: 5px;
                padding: 5px;
                color: {SECONDARY_COLOR};
                font-size: 12px;
            }}
            QPushButton {{
                background-color: #2a2a2a;
                border: 2px solid {PRIMARY_COLOR};
                border-radius: 5px;
                padding: 8px;
                color: {SECONDARY_COLOR};
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: #3a3a3a;
            }}
            QPushButton:pressed {{
                background-color: {PRIMARY_COLOR};
                color: {BACKGROUND_COLOR};
            }}
            QTextEdit {{
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-radius: 5px;
                padding: 10px;
                color: {SECONDARY_COLOR};
                font-size: 12px;
            }}
        """)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # Demo banner
        demo_banner = QLabel("🎭 DEMO MODE - PySide6 Version")
        demo_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        demo_banner.setFont(QFont("Monaco", 12, QFont.Weight.Bold))
        demo_banner.setStyleSheet(f"color: {ACCENT_COLOR}; background-color: #2a2a2a; padding: 10px; border-radius: 5px;")
        main_layout.addWidget(demo_banner)
        
        # Audio controls
        audio_controls = QWidget()
        audio_layout = QHBoxLayout(audio_controls)
        audio_layout.setContentsMargins(0, 0, 0, 0)
        
        # Voice mode selector
        voice_label = QLabel("Voice Mode:")
        audio_layout.addWidget(voice_label)
        
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["Male", "Female", "Alien"])
        self.voice_combo.setCurrentText("Male")
        audio_layout.addWidget(self.voice_combo)
        
        audio_layout.addStretch()
        
        # Audio toggle
        self.audio_checkbox = QCheckBox("🔊 Audio Enabled")
        self.audio_checkbox.setChecked(TTS_AVAILABLE)
        if not TTS_AVAILABLE:
            self.audio_checkbox.setEnabled(False)
            self.audio_checkbox.setText("🔇 Audio Unavailable")
        audio_layout.addWidget(self.audio_checkbox)
        
        main_layout.addWidget(audio_controls)
        
        # Simple centered circle placeholder
        circle_placeholder = QLabel("⚪ Animated Circle Here ⚪")
        circle_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        circle_placeholder.setFont(QFont("Monaco", 16))
        circle_placeholder.setStyleSheet(f"color: {PRIMARY_COLOR}; padding: 100px; border: 2px solid {PRIMARY_COLOR}; border-radius: 100px;")
        circle_placeholder.setFixedSize(200, 200)
        main_layout.addWidget(circle_placeholder, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Click button instead of circle
        self.test_button = QPushButton("🎤 Click to Test Demo")
        self.test_button.setFixedSize(200, 50)
        self.test_button.setFont(QFont("Monaco", 14))
        main_layout.addWidget(self.test_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Status text
        self.status_label = QLabel("PySide6 Demo Ready - Click button to test!")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Monaco", 14))
        self.status_label.setStyleSheet(f"color: {PRIMARY_COLOR}; font-weight: bold;")
        main_layout.addWidget(self.status_label)
        
        # Conversation display
        conversation_label = QLabel("Demo Conversation:")
        conversation_label.setFont(QFont("Monaco", 12, QFont.Weight.Bold))
        main_layout.addWidget(conversation_label)
        
        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        self.conversation_display.setMaximumHeight(200)
        self.conversation_display.setPlaceholderText("Demo conversation will appear here...")
        main_layout.addWidget(self.conversation_display)
        
        # Control buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.clear_button = QPushButton("Clear Conversation")
        self.clear_button.setFixedWidth(150)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch()
        
        self.info_button = QPushButton("About Demo")
        self.info_button.setFixedWidth(100)
        button_layout.addWidget(self.info_button)
        
        main_layout.addWidget(button_widget)
        
        # Optional OpenAI API key section
        api_widget = QWidget()
        api_layout = QHBoxLayout(api_widget)
        api_layout.setContentsMargins(0, 0, 0, 0)
        
        api_label = QLabel("🤖 OpenAI API Key (optional for real AI):")
        api_layout.addWidget(api_label)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("sk-... (leave empty for demo responses)")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addWidget(self.api_key_input)
        
        self.api_button = QPushButton("Enable AI")
        self.api_button.setFixedWidth(80)
        api_layout.addWidget(self.api_button)
        
        main_layout.addWidget(api_widget)
    
    def setup_connections(self):
        """Set up signal connections."""
        self.test_button.clicked.connect(self.on_test_clicked)
        self.clear_button.clicked.connect(self.clear_conversation)
        self.info_button.clicked.connect(self.show_info)
        
        # Connect audio controls
        self.voice_combo.currentTextChanged.connect(self.on_voice_mode_changed)
        self.audio_checkbox.toggled.connect(self.on_audio_toggled)
        
        # Connect API key button
        self.api_button.clicked.connect(self.on_api_key_entered)
    
    def on_voice_mode_changed(self, mode):
        """Handle voice mode change."""
        self.voice_engine.set_voice_mode(mode)
        self.add_to_conversation("System", f"Voice mode changed to: {mode}")
    
    def on_audio_toggled(self, enabled):
        """Handle audio toggle."""
        self.voice_engine.set_audio_enabled(enabled)
        status = "enabled" if enabled else "disabled"
        self.add_to_conversation("System", f"Audio output {status}")
    
    def show_welcome_message(self):
        """Show welcome message on startup."""
        welcome_msg = "Welcome to the PySide6 Voice Assistant demo! Click the test button to begin."
        self.add_to_conversation("ARIA", welcome_msg)
        
        # Speak welcome message if audio is enabled
        if TTS_AVAILABLE:
            self.voice_engine.speak(welcome_msg)
    
    def on_test_clicked(self):
        """Handle test button click."""
        self.status_label.setText("Demo: Simulating interaction...")
        
        # Simulate user input
        user_phrases = [
            "Hello ARIA, how are you?",
            "Tell me about this demo",
            "What can you do?",
            "This looks amazing!",
            "How does this work?",
            "Show me more features",
            "What else can you help with?",
            "This is incredible!"
        ]
        
        user_text = user_phrases[self.ai_assistant.response_index % len(user_phrases)]
        self.add_to_conversation("You", user_text)
        
        # Get AI response
        self.ai_assistant.get_response(user_text, self.on_ai_response)
    
    def on_ai_response(self, response, error):
        """Handle AI response."""
        if response:
            self.add_to_conversation("ARIA", response)
            # Speak the response
            self.voice_engine.speak(response)
            self.status_label.setText("PySide6 Demo Ready - Click button to test!")
    
    def add_to_conversation(self, speaker, message):
        """Add a message to the conversation display."""
        timestamp = self.get_timestamp()
        
        if speaker == "You":
            formatted_message = f"<span style='color: {ACCENT_COLOR}; font-weight: bold;'>[{timestamp}] {speaker}:</span> {message}"
        else:
            formatted_message = f"<span style='color: {PRIMARY_COLOR}; font-weight: bold;'>[{timestamp}] {speaker}:</span> {message}"
        
        self.conversation_display.append(formatted_message)
        
        # Auto-scroll to bottom
        cursor = self.conversation_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.conversation_display.setTextCursor(cursor)
    
    def clear_conversation(self):
        """Clear the conversation display."""
        self.conversation_display.clear()
        self.ai_assistant.clear_conversation()
    
    def show_info(self):
        """Show information about the demo."""
        info_msg = """This is a PySide6 version of the Voice Assistant demo.

Features:
• Futuristic dark UI theme
• Simulated AI conversations
• Cross-platform compatibility
• No external dependencies needed

To get the full version with animations:
1. Install PyQt6 properly
2. Run the main application"""
        
        self.add_to_conversation("ARIA", info_msg)
    
    def get_timestamp(self):
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

    def on_api_key_entered(self):
        """Handle API key input."""
        api_key = self.api_key_input.text().strip()
        if api_key:
            try:
                # Try to initialize real OpenAI client
                import openai
                client = openai.OpenAI(api_key=api_key)
                
                # Test the API key with a simple request
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=10
                )
                
                # If successful, update AI assistant
                self.ai_assistant = RealAIAssistant(client)
                self.add_to_conversation("System", "✅ OpenAI API connected successfully! Now using real AI responses.")
                self.api_button.setText("✅ Active")
                self.api_button.setEnabled(False)
                
            except Exception as e:
                self.add_to_conversation("System", f"❌ API key error: {str(e)}")
        else:
            self.add_to_conversation("System", "Please enter a valid OpenAI API key")

class RealAIAssistant:
    """Real AI assistant using OpenAI API."""
    
    def __init__(self, client):
        self.client = client
        self.conversation_history = []
    
    def get_response(self, user_input, callback=None):
        """Get real AI response."""
        def get_real_response():
            try:
                # Add user message to history
                self.conversation_history.append({"role": "user", "content": user_input})
                
                # Get response from OpenAI
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are ARIA, a futuristic AI voice assistant. Be helpful, friendly, and concise."},
                        *self.conversation_history[-10:]  # Keep last 10 messages for context
                    ],
                    max_tokens=150
                )
                
                ai_response = response.choices[0].message.content
                self.conversation_history.append({"role": "assistant", "content": ai_response})
                
                if callback:
                    QTimer.singleShot(0, lambda: callback(ai_response, None))
                    
            except Exception as e:
                if callback:
                    QTimer.singleShot(0, lambda: callback(None, str(e)))
        
        import threading
        thread = threading.Thread(target=get_real_response)
        thread.daemon = True
        thread.start()
    
    def clear_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []

def main():
    """Main demo application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName(f"{APP_TITLE} - PySide6 Demo")
    app.setApplicationVersion("1.0-pyside6-demo")
    
    window = DemoVoiceAssistantApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 