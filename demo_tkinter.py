#!/usr/bin/env python3
"""
Simple Tkinter version of the Voice Assistant demo.
This version uses Tkinter (built into Python) for maximum compatibility.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time

try:
    import pyttsx3
    TTS_AVAILABLE = True
    print("✅ pyttsx3 available - audio enabled")
except ImportError:
    TTS_AVAILABLE = False
    print("❌ pyttsx3 not available - audio disabled")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class VoiceEngine:
    """Voice engine with real TTS."""
    
    def __init__(self):
        self.current_voice_mode = "Male"
        self.audio_enabled = TTS_AVAILABLE
        
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self._configure_voice()
                print("✅ TTS engine initialized")
            except Exception as e:
                print(f"❌ TTS initialization failed: {e}")
                self.audio_enabled = False
                self.tts_engine = None
        else:
            self.tts_engine = None
    
    def _configure_voice(self):
        """Configure the TTS voice."""
        if not self.tts_engine:
            return
            
        voices = self.tts_engine.getProperty('voices')
        if not voices:
            return
            
        if self.current_voice_mode == "Female":
            for voice in voices:
                if 'female' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            self.tts_engine.setProperty('rate', 180)
            
        elif self.current_voice_mode == "Male":
            for voice in voices:
                if 'male' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            else:
                if voices:
                    self.tts_engine.setProperty('voice', voices[0].id)
            self.tts_engine.setProperty('rate', 170)
            
        elif self.current_voice_mode == "Alien":
            if voices:
                self.tts_engine.setProperty('voice', voices[-1].id)
            self.tts_engine.setProperty('rate', 140)
            
        self.tts_engine.setProperty('volume', 0.9)
    
    def set_voice_mode(self, mode):
        """Set voice mode."""
        self.current_voice_mode = mode
        self._configure_voice()
    
    def speak(self, text):
        """Speak text with robust error handling."""
        if not self.audio_enabled or not self.tts_engine:
            print(f"TTS disabled - would speak: {text}")
            return
            
        def speak_thread():
            try:
                print(f"🔊 Speaking: {text}")
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                print("✅ Speech completed")
            except Exception as e:
                print(f"❌ TTS error: {e}")
                # Disable TTS if it keeps failing
                self.audio_enabled = False
        
        try:
            thread = threading.Thread(target=speak_thread)
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"❌ Thread creation error: {e}")
            self.audio_enabled = False

class DemoAI:
    """Demo AI with predefined responses."""
    
    def __init__(self):
        self.responses = [
            "Hello! I'm ARIA, your futuristic voice assistant. I can hear you loud and clear!",
            "My audio system is working perfectly! Can you hear my voice?",
            "This demo showcases real text-to-speech functionality without needing any API keys.",
            "Try changing my voice mode to hear different voices - Male, Female, or Alien!",
            "I would normally be powered by GPT-4, but this demo works completely offline.",
            "The voice synthesis is happening in real-time on your computer.",
            "This demonstrates how accessible AI voice technology has become.",
            "Thank you for testing my voice capabilities!"
        ]
        self.index = 0
    
    def get_response(self, user_input=""):
        """Get a demo response."""
        response = self.responses[self.index % len(self.responses)]
        self.index += 1
        return response

class RealAI:
    """Real OpenAI integration."""
    
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        self.history = []
    
    def get_response(self, user_input):
        """Get real AI response."""
        try:
            self.history.append({"role": "user", "content": user_input})
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are ARIA, a helpful voice assistant. Be concise and friendly."},
                    *self.history[-8:]
                ],
                max_tokens=100
            )
            
            ai_response = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": ai_response})
            return ai_response
            
        except Exception as e:
            return f"AI Error: {str(e)}"

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 ARIA Voice Assistant - Tkinter Demo")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize components
        self.voice_engine = VoiceEngine()
        self.ai = DemoAI()
        self.real_ai = None
        
        self.setup_ui()
        self.welcome()
    
    def setup_ui(self):
        """Setup the user interface."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme
        style.configure('Dark.TFrame', background='#1a1a1a')
        style.configure('Dark.TLabel', background='#1a1a1a', foreground='#00ffff')
        style.configure('Dark.TButton', background='#2a2a2a', foreground='#00ffff')
        
        # Main frame
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = ttk.Label(main_frame, text="🎤 ARIA Voice Assistant", 
                         font=('Monaco', 20, 'bold'), style='Dark.TLabel')
        title.pack(pady=10)
        
        # Audio status
        audio_status = "🔊 Audio: ENABLED" if TTS_AVAILABLE else "🔇 Audio: DISABLED"
        status_label = ttk.Label(main_frame, text=audio_status, 
                               font=('Monaco', 12), style='Dark.TLabel')
        status_label.pack(pady=5)
        
        # Voice mode frame
        voice_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        voice_frame.pack(pady=10)
        
        ttk.Label(voice_frame, text="Voice Mode:", style='Dark.TLabel').pack(side=tk.LEFT, padx=5)
        
        self.voice_var = tk.StringVar(value="Male")
        voice_combo = ttk.Combobox(voice_frame, textvariable=self.voice_var, 
                                  values=["Male", "Female", "Alien"], state="readonly")
        voice_combo.pack(side=tk.LEFT, padx=5)
        voice_combo.bind('<<ComboboxSelected>>', self.on_voice_change)
        
        # Test button
        test_btn = ttk.Button(main_frame, text="🎤 Test Voice Assistant", 
                             command=self.test_voice, style='Dark.TButton')
        test_btn.pack(pady=20)
        
        # Conversation area
        conv_label = ttk.Label(main_frame, text="Conversation:", 
                              font=('Monaco', 12, 'bold'), style='Dark.TLabel')
        conv_label.pack(anchor=tk.W, pady=(20,5))
        
        self.conversation = scrolledtext.ScrolledText(main_frame, width=80, height=15,
                                                     bg='#2a2a2a', fg='#ffffff',
                                                     font=('Monaco', 10))
        self.conversation.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # API key frame
        api_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        api_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(api_frame, text="🤖 OpenAI API Key (optional):", 
                 style='Dark.TLabel').pack(side=tk.LEFT)
        
        self.api_entry = tk.Entry(api_frame, show="*", bg='#2a2a2a', fg='#ffffff',
                                 font=('Monaco', 10))
        self.api_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Button(api_frame, text="Enable Real AI", 
                  command=self.enable_real_ai, style='Dark.TButton').pack(side=tk.RIGHT)
        
        # Control buttons
        btn_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Clear", command=self.clear_conversation, 
                  style='Dark.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Test Audio", command=self.test_audio, 
                  style='Dark.TButton').pack(side=tk.LEFT, padx=5)
    
    def add_message(self, speaker, message):
        """Add message to conversation."""
        self.conversation.insert(tk.END, f"{speaker}: {message}\n\n")
        self.conversation.see(tk.END)
    
    def on_voice_change(self, event=None):
        """Handle voice mode change."""
        mode = self.voice_var.get()
        self.voice_engine.set_voice_mode(mode)
        self.add_message("System", f"Voice changed to {mode}")
        
        # Use safe speak
        try:
            if TTS_AVAILABLE:
                self.safe_speak(f"Voice mode changed to {mode}")
        except Exception as e:
            print(f"Voice change speak error: {e}")
    
    def test_voice(self):
        """Test the voice assistant."""
        user_input = "Hello ARIA, can you hear me?"
        self.add_message("You", user_input)
        
        # Get AI response
        if self.real_ai:
            def get_real_response():
                response = self.real_ai.get_response(user_input)
                self.root.after(0, lambda: self.handle_response(response))
            threading.Thread(target=get_real_response, daemon=True).start()
        else:
            response = self.ai.get_response(user_input)
            self.handle_response(response)
    
    def handle_response(self, response):
        """Handle AI response."""
        self.add_message("ARIA", response)
        # Use safe speak
        try:
            if TTS_AVAILABLE:
                self.safe_speak(response)
        except Exception as e:
            print(f"Response speak error: {e}")
    
    def test_audio(self):
        """Test audio directly."""
        test_msg = f"Testing {self.voice_var.get()} voice mode. Audio is working!"
        self.add_message("ARIA", test_msg)
        try:
            if TTS_AVAILABLE:
                self.safe_speak(test_msg)
            else:
                messagebox.showinfo("Audio Test", "Audio not available - pyttsx3 not installed")
        except Exception as e:
            print(f"Audio test error: {e}")
            messagebox.showerror("Audio Error", f"TTS system error: {str(e)}")
    
    def enable_real_ai(self):
        """Enable real AI with API key."""
        api_key = self.api_entry.get().strip()
        if not api_key:
            messagebox.showwarning("API Key", "Please enter an OpenAI API key")
            return
        
        if not OPENAI_AVAILABLE:
            messagebox.showerror("OpenAI", "OpenAI package not installed")
            return
        
        try:
            self.real_ai = RealAI(api_key)
            self.add_message("System", "✅ Real AI enabled!")
            try:
                if TTS_AVAILABLE:
                    self.safe_speak("Real AI enabled successfully!")
            except Exception as e:
                print(f"Real AI speak error: {e}")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to connect: {str(e)}")
    
    def clear_conversation(self):
        """Clear conversation."""
        self.conversation.delete(1.0, tk.END)
        self.ai = DemoAI()  # Reset demo AI
    
    def welcome(self):
        """Show welcome message."""
        welcome_msg = "Welcome to ARIA! I'm ready to talk. Click 'Test Voice Assistant' to begin!"
        self.add_message("ARIA", welcome_msg)
        
        # Add safe mode option - disable TTS if it's causing crashes
        try:
            if TTS_AVAILABLE and hasattr(self.voice_engine, 'audio_enabled') and self.voice_engine.audio_enabled:
                # Delay welcome speech by 2 seconds to let UI settle
                self.root.after(2000, lambda: self.safe_speak(welcome_msg))
            else:
                print("TTS disabled - skipping welcome speech")
        except Exception as e:
            print(f"Welcome speech error: {e}")
    
    def safe_speak(self, text):
        """Safely speak text with additional error handling."""
        try:
            if hasattr(self.voice_engine, 'speak'):
                self.voice_engine.speak(text)
        except Exception as e:
            print(f"Safe speak error: {e}")
            self.add_message("System", "⚠️ Audio system disabled due to errors")

def main():
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 