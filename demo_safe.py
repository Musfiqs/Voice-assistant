#!/usr/bin/env python3
"""
Safe Tkinter version of the Voice Assistant demo.
This version runs without TTS to avoid crashes and focuses on the UI and AI functionality.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time

# Force disable TTS for safety
TTS_AVAILABLE = False
print("🛡️ Running in SAFE MODE - TTS disabled to prevent crashes")

try:
    import openai
    OPENAI_AVAILABLE = True
    print("✅ OpenAI available")
except ImportError:
    OPENAI_AVAILABLE = False
    print("❌ OpenAI not available")

class SafeVoiceEngine:
    """Safe voice engine that only simulates speech."""
    
    def __init__(self):
        self.current_voice_mode = "Male"
        self.audio_enabled = False
        print("🛡️ Safe voice engine initialized - no actual audio")
    
    def set_voice_mode(self, mode):
        """Set voice mode (simulation only)."""
        self.current_voice_mode = mode
        print(f"🔄 Voice mode set to: {mode}")
    
    def speak(self, text):
        """Simulate speech by printing to console."""
        print(f"🗣️ ARIA would say: {text}")

class DemoAI:
    """Demo AI with predefined responses."""
    
    def __init__(self):
        self.responses = [
            "Hello! I'm ARIA, your voice assistant. I'm running in safe mode!",
            "My systems are working perfectly! This is a safe demonstration.",
            "This demo shows the interface and AI functionality without audio crashes.",
            "Try changing my voice mode - it won't make sound but shows the controls work!",
            "I would normally speak, but safe mode prevents audio system crashes.",
            "The conversation system is fully functional in this safe mode.",
            "You can still add an OpenAI API key for real AI responses!",
            "Thank you for testing my safe mode capabilities!"
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
                    {"role": "system", "content": "You are ARIA, a helpful voice assistant running in safe mode. Be concise and friendly."},
                    *self.history[-8:]
                ],
                max_tokens=100
            )
            
            ai_response = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": ai_response})
            return ai_response
            
        except Exception as e:
            return f"AI Error: {str(e)}"

class SafeVoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ ARIA Voice Assistant - SAFE MODE")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize components
        self.voice_engine = SafeVoiceEngine()
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
        title = ttk.Label(main_frame, text="🛡️ ARIA Voice Assistant - SAFE MODE", 
                         font=('Monaco', 18, 'bold'), style='Dark.TLabel')
        title.pack(pady=10)
        
        # Safety notice
        safety_label = ttk.Label(main_frame, text="🔇 Audio disabled for stability - Check console for 'speech' output", 
                               font=('Monaco', 10), style='Dark.TLabel')
        safety_label.pack(pady=5)
        
        # Voice mode frame
        voice_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        voice_frame.pack(pady=10)
        
        ttk.Label(voice_frame, text="Voice Mode (simulation):", style='Dark.TLabel').pack(side=tk.LEFT, padx=5)
        
        self.voice_var = tk.StringVar(value="Male")
        voice_combo = ttk.Combobox(voice_frame, textvariable=self.voice_var, 
                                  values=["Male", "Female", "Alien"], state="readonly")
        voice_combo.pack(side=tk.LEFT, padx=5)
        voice_combo.bind('<<ComboboxSelected>>', self.on_voice_change)
        
        # Test button
        test_btn = ttk.Button(main_frame, text="🎤 Test Voice Assistant (Safe Mode)", 
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
        # API key field left empty for security
        self.api_entry.insert(0, "")
        self.api_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Button(api_frame, text="Enable Real AI", 
                  command=self.enable_real_ai, style='Dark.TButton').pack(side=tk.RIGHT)
        
        # Control buttons
        btn_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Clear", command=self.clear_conversation, 
                  style='Dark.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Test Console Output", command=self.test_console, 
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
        self.voice_engine.speak(f"Voice mode changed to {mode}")
    
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
        self.voice_engine.speak(response)
    
    def test_console(self):
        """Test console output."""
        test_msg = f"Testing {self.voice_var.get()} voice mode in safe mode. Check the console!"
        self.add_message("ARIA", test_msg)
        self.voice_engine.speak(test_msg)
        messagebox.showinfo("Console Test", "Check your terminal/console for the speech output!")
    
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
            self.add_message("System", "✅ Real AI enabled in safe mode!")
            self.voice_engine.speak("Real AI enabled successfully!")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to connect: {str(e)}")
    
    def clear_conversation(self):
        """Clear conversation."""
        self.conversation.delete(1.0, tk.END)
        self.ai = DemoAI()  # Reset demo AI
    
    def welcome(self):
        """Show welcome message."""
        welcome_msg = "Welcome to ARIA Safe Mode! I'm ready to chat. Check the console for 'speech' output!"
        self.add_message("ARIA", welcome_msg)
        self.voice_engine.speak(welcome_msg)
        
        # Note: Add your OpenAI API key manually in the GUI if you want real AI responses

def main():
    print("🛡️ Starting ARIA in Safe Mode...")
    print("🗣️ Speech will be shown in console instead of audio")
    print("💬 This prevents TTS-related crashes")
    print()
    
    root = tk.Tk()
    app = SafeVoiceAssistantApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 