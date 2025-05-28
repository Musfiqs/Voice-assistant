#!/usr/bin/env python3
"""
Demo version of the Futuristic Voice Assistant.
This version works without an OpenAI API key for testing the GUI.
"""

import sys
import time
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QTextEdit
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from config import *
from animated_circle import AnimatedCircle

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
        def delayed_response():
            time.sleep(2)  # Simulate processing time
            response = self.responses[self.response_index % len(self.responses)]
            self.response_index += 1
            if callback:
                callback(response, None)
        
        thread = QThread()
        thread.run = delayed_response
        thread.start()
        return thread
    
    def clear_conversation(self):
        """Reset response index."""
        self.response_index = 0

class DemoVoiceEngine:
    """Demo voice engine that simulates speech recognition and TTS."""
    
    def __init__(self):
        self.current_voice_mode = "Male"
        self.is_listening = False
        self.is_speaking = False
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
    
    def set_voice_mode(self, mode):
        """Set the voice mode."""
        self.current_voice_mode = mode
    
    def listen_for_speech(self, callback=None):
        """Simulate speech recognition."""
        def simulate_listening():
            self.is_listening = True
            time.sleep(3)  # Simulate listening time
            
            # Get a demo phrase
            text = self.demo_phrases[self.phrase_index % len(self.demo_phrases)]
            self.phrase_index += 1
            
            self.is_listening = False
            if callback:
                callback(text, None)
        
        thread = QThread()
        thread.run = simulate_listening
        thread.start()
        return thread
    
    def speak(self, text, callback=None):
        """Simulate text-to-speech."""
        def simulate_speaking():
            self.is_speaking = True
            # Simulate speaking time based on text length
            speaking_time = max(2, len(text) * 0.1)
            time.sleep(speaking_time)
            self.is_speaking = False
            if callback:
                callback()
        
        thread = QThread()
        thread.run = simulate_speaking
        thread.start()
        return thread
    
    def stop_speaking(self):
        """Stop speaking simulation."""
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
        self.setWindowTitle(f"{APP_TITLE} - DEMO MODE")
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
        demo_banner = QLabel("🎭 DEMO MODE - No API Key Required")
        demo_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        demo_banner.setFont(QFont("Monaco", 12, QFont.Weight.Bold))
        demo_banner.setStyleSheet(f"color: {ACCENT_COLOR}; background-color: #2a2a2a; padding: 10px; border-radius: 5px;")
        main_layout.addWidget(demo_banner)
        
        # Top section with voice mode selector
        self.create_top_section(main_layout)
        
        # Center section with animated circle
        self.create_center_section(main_layout)
        
        # Bottom section with conversation display
        self.create_bottom_section(main_layout)
        
        # Status bar
        self.create_status_section(main_layout)
    
    def create_top_section(self, parent_layout):
        """Create the top section with voice mode selector."""
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Spacer to push voice selector to the right
        top_layout.addStretch()
        
        # Voice mode label and selector
        voice_label = QLabel("Voice Mode:")
        voice_label.setFont(QFont("Monaco", 12))
        top_layout.addWidget(voice_label)
        
        self.voice_selector = QComboBox()
        self.voice_selector.addItems(["Male", "Female", "Alien"])
        self.voice_selector.setCurrentText("Male")
        self.voice_selector.setFixedWidth(120)
        top_layout.addWidget(self.voice_selector)
        
        parent_layout.addWidget(top_widget)
    
    def create_center_section(self, parent_layout):
        """Create the center section with animated circle."""
        # Create a container for the circle
        circle_container = QWidget()
        circle_container.setFixedHeight(350)
        circle_layout = QVBoxLayout(circle_container)
        circle_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add the animated circle
        self.animated_circle = AnimatedCircle()
        circle_layout.addWidget(self.animated_circle, alignment=Qt.AlignmentFlag.AlignCenter)
        
        parent_layout.addWidget(circle_container)
        
        # Status text below circle
        self.status_label = QLabel("Click the circle to start demo interaction")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Monaco", 14))
        self.status_label.setStyleSheet(f"color: {PRIMARY_COLOR}; font-weight: bold;")
        parent_layout.addWidget(self.status_label)
    
    def create_bottom_section(self, parent_layout):
        """Create the bottom section with conversation display."""
        # Conversation display
        conversation_label = QLabel("Demo Conversation:")
        conversation_label.setFont(QFont("Monaco", 12, QFont.Weight.Bold))
        parent_layout.addWidget(conversation_label)
        
        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        self.conversation_display.setMaximumHeight(200)
        self.conversation_display.setPlaceholderText("Demo conversation will appear here...")
        parent_layout.addWidget(self.conversation_display)
        
        # Control buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.clear_button = QPushButton("Clear Conversation")
        self.clear_button.setFixedWidth(150)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch()
        
        self.full_version_button = QPushButton("Get Full Version")
        self.full_version_button.setFixedWidth(130)
        button_layout.addWidget(self.full_version_button)
        
        parent_layout.addWidget(button_widget)
    
    def create_status_section(self, parent_layout):
        """Create the status section."""
        self.status_bar = QLabel("Demo Ready - Click the circle to test!")
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_bar.setFont(QFont("Monaco", 10))
        self.status_bar.setStyleSheet(f"""
            background-color: #2a2a2a;
            border: 1px solid #404040;
            border-radius: 3px;
            padding: 5px;
            color: {SECONDARY_COLOR};
        """)
        parent_layout.addWidget(self.status_bar)
    
    def setup_connections(self):
        """Set up signal connections."""
        self.animated_circle.circle_clicked.connect(self.on_circle_clicked)
        self.voice_selector.currentTextChanged.connect(self.on_voice_mode_changed)
        self.clear_button.clicked.connect(self.clear_conversation)
        self.full_version_button.clicked.connect(self.show_full_version_info)
    
    def show_welcome_message(self):
        """Show welcome message on startup."""
        self.add_to_conversation("ARIA", "Welcome to the Voice Assistant demo! Click the holographic circle to begin.")
    
    def on_circle_clicked(self):
        """Handle circle click to start demo interaction."""
        if self.voice_engine.is_listening or self.voice_engine.is_speaking:
            return
        
        self.status_label.setText("Demo: Simulating speech recognition...")
        self.status_bar.setText("Listening for voice input (simulated)...")
        self.animated_circle.set_state("listening")
        
        # Start simulated voice recognition
        self.voice_engine.listen_for_speech(self.on_speech_recognized)
    
    def on_speech_recognized(self, text, error):
        """Handle simulated speech recognition result."""
        if text:
            self.status_label.setText("Demo: Processing your request...")
            self.status_bar.setText("Getting AI response (simulated)...")
            self.animated_circle.set_state("processing")
            
            # Add user message to conversation
            self.add_to_conversation("You", text)
            
            # Get AI response
            self.ai_assistant.get_response(text, self.on_ai_response)
    
    def on_ai_response(self, response, error):
        """Handle simulated AI response."""
        if response:
            # Add AI response to conversation
            self.add_to_conversation("ARIA", response)
            
            # Simulate speaking the response
            self.status_label.setText("Demo: Speaking response...")
            self.status_bar.setText("Playing AI response (simulated)...")
            self.voice_engine.speak(response, self.on_speech_complete)
    
    def on_speech_complete(self):
        """Handle completion of speech simulation."""
        self.status_label.setText("Click the circle to continue demo")
        self.status_bar.setText("Demo ready - Click the circle to test!")
        self.animated_circle.set_state("idle")
    
    def on_voice_mode_changed(self, mode):
        """Handle voice mode change."""
        self.voice_engine.set_voice_mode(mode)
        self.status_bar.setText(f"Demo: Voice mode changed to {mode}")
    
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
        self.status_bar.setText("Demo conversation cleared")
    
    def show_full_version_info(self):
        """Show information about the full version."""
        info_msg = """To use the full version with real AI:

1. Get an OpenAI API key from:
   https://platform.openai.com/api-keys

2. Set your API key:
   export OPENAI_API_KEY='your-key-here'

3. Run the full version:
   python main_window.py

The full version includes:
• Real GPT-4 AI responses
• Actual speech recognition
• Text-to-speech output
• All voice modes working"""
        
        self.add_to_conversation("ARIA", info_msg)
    
    def get_timestamp(self):
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")

def main():
    """Main demo application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName(f"{APP_TITLE} - Demo")
    app.setApplicationVersion("1.0-demo")
    
    window = DemoVoiceAssistantApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 