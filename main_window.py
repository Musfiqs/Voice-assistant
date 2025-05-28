"""
Main Window for the Futuristic Voice Assistant.
Integrates all components into a cohesive GUI application.
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QComboBox, QPushButton, 
                            QTextEdit, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor

from config import *
from animated_circle import AnimatedCircle
from voice_engine import VoiceEngine
from ai_assistant import AIAssistant

class VoiceAssistantApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.voice_engine = VoiceEngine()
        self.ai_assistant = AIAssistant()
        
        # UI state
        self.current_conversation = []
        
        # Initialize UI
        self.init_ui()
        
        # Connect signals
        self.setup_connections()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(APP_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Set window style
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
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-style: solid;
                border-width: 5px;
                border-color: {PRIMARY_COLOR} transparent transparent transparent;
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
                line-height: 1.5;
            }}
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
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
        self.status_label = QLabel("Click the circle to start voice interaction")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Monaco", 14))
        self.status_label.setStyleSheet(f"color: {PRIMARY_COLOR}; font-weight: bold;")
        parent_layout.addWidget(self.status_label)
    
    def create_bottom_section(self, parent_layout):
        """Create the bottom section with conversation display."""
        # Conversation display
        conversation_label = QLabel("Conversation:")
        conversation_label.setFont(QFont("Monaco", 12, QFont.Weight.Bold))
        parent_layout.addWidget(conversation_label)
        
        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        self.conversation_display.setMaximumHeight(200)
        self.conversation_display.setPlaceholderText("Conversation will appear here...")
        parent_layout.addWidget(self.conversation_display)
        
        # Control buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.clear_button = QPushButton("Clear Conversation")
        self.clear_button.setFixedWidth(150)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch()
        
        self.test_button = QPushButton("Test TTS")
        self.test_button.setFixedWidth(100)
        button_layout.addWidget(self.test_button)
        
        parent_layout.addWidget(button_widget)
    
    def create_status_section(self, parent_layout):
        """Create the status section."""
        self.status_bar = QLabel("Ready")
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
        # Circle click
        self.animated_circle.circle_clicked.connect(self.on_circle_clicked)
        
        # Voice mode change
        self.voice_selector.currentTextChanged.connect(self.on_voice_mode_changed)
        
        # Buttons
        self.clear_button.clicked.connect(self.clear_conversation)
        self.test_button.clicked.connect(self.test_tts)
    
    def on_circle_clicked(self):
        """Handle circle click to start voice interaction."""
        if self.voice_engine.is_listening or self.voice_engine.is_speaking:
            return
        
        self.status_label.setText("Listening... Speak now!")
        self.status_bar.setText("Listening for voice input...")
        self.animated_circle.set_state("listening")
        
        # Start voice recognition
        self.voice_engine.listen_for_speech(self.on_speech_recognized)
    
    def on_speech_recognized(self, text, error):
        """Handle speech recognition result."""
        if error:
            self.status_label.setText(f"Error: {error}")
            self.status_bar.setText("Ready")
            self.animated_circle.set_state("idle")
            return
        
        if text:
            # Update UI
            self.status_label.setText("Processing your request...")
            self.status_bar.setText("Getting AI response...")
            self.animated_circle.set_state("processing")
            
            # Add user message to conversation
            self.add_to_conversation("You", text)
            
            # Get AI response
            self.ai_assistant.get_response(text, self.on_ai_response)
    
    def on_ai_response(self, response, error):
        """Handle AI response."""
        if error:
            self.status_label.setText(f"AI Error: {error}")
            self.status_bar.setText("Ready")
            self.animated_circle.set_state("idle")
            return
        
        if response:
            # Add AI response to conversation
            self.add_to_conversation("ARIA", response)
            
            # Speak the response
            self.status_label.setText("Speaking response...")
            self.status_bar.setText("Playing AI response...")
            self.voice_engine.speak(response, self.on_speech_complete)
    
    def on_speech_complete(self):
        """Handle completion of speech output."""
        self.status_label.setText("Click the circle to start voice interaction")
        self.status_bar.setText("Ready")
        self.animated_circle.set_state("idle")
    
    def on_voice_mode_changed(self, mode):
        """Handle voice mode change."""
        self.voice_engine.set_voice_mode(mode)
        self.status_bar.setText(f"Voice mode changed to: {mode}")
    
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
        """Clear the conversation display and history."""
        self.conversation_display.clear()
        self.ai_assistant.clear_conversation()
        self.status_bar.setText("Conversation cleared")
    
    def test_tts(self):
        """Test the text-to-speech functionality."""
        test_message = f"Testing {self.voice_selector.currentText()} voice mode. Hello, I am ARIA, your futuristic voice assistant."
        self.voice_engine.speak(test_message)
        self.status_bar.setText(f"Testing {self.voice_selector.currentText()} voice...")
    
    def get_timestamp(self):
        """Get current timestamp for conversation."""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def closeEvent(self, event):
        """Handle application close event."""
        self.voice_engine.stop_speaking()
        event.accept()

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName(APP_TITLE)
    app.setApplicationVersion("1.0")
    
    # Create and show main window
    window = VoiceAssistantApp()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 