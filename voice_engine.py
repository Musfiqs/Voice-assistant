"""
Voice Engine Module for the Voice Assistant.
Handles speech recognition and text-to-speech functionality.
"""

import speech_recognition as sr
import pyttsx3
import threading
import numpy as np
from config import VOICE_MODES

class VoiceEngine:
    def __init__(self):
        """Initialize the voice engine with speech recognition and TTS."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.current_voice_mode = "Male"
        self.is_listening = False
        self.is_speaking = False
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def set_voice_mode(self, mode):
        """Set the voice mode (Male, Female, Alien)."""
        if mode in VOICE_MODES:
            self.current_voice_mode = mode
            self._configure_tts_voice()
    
    def _configure_tts_voice(self):
        """Configure TTS engine based on current voice mode."""
        voices = self.tts_engine.getProperty('voices')
        settings = VOICE_MODES[self.current_voice_mode]
        
        # Set voice based on mode
        if self.current_voice_mode == "Female" and len(voices) > 1:
            self.tts_engine.setProperty('voice', voices[1].id)
        else:
            self.tts_engine.setProperty('voice', voices[0].id)
        
        # Set rate and volume
        self.tts_engine.setProperty('rate', settings['rate'])
        self.tts_engine.setProperty('volume', 0.9)
    
    def listen_for_speech(self, callback=None):
        """Listen for speech input and return transcribed text."""
        def listen_thread():
            self.is_listening = True
            try:
                with self.microphone as source:
                    print("Listening...")
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                
                print("Processing speech...")
                # Recognize speech using Google's service
                text = self.recognizer.recognize_google(audio)
                print(f"Transcribed: {text}")
                
                if callback:
                    callback(text, None)
                return text
                
            except sr.WaitTimeoutError:
                error_msg = "Listening timeout"
                print(error_msg)
                if callback:
                    callback(None, error_msg)
            except sr.UnknownValueError:
                error_msg = "Could not understand audio"
                print(error_msg)
                if callback:
                    callback(None, error_msg)
            except sr.RequestError as e:
                error_msg = f"Could not request results; {e}"
                print(error_msg)
                if callback:
                    callback(None, error_msg)
            finally:
                self.is_listening = False
        
        # Run listening in a separate thread
        thread = threading.Thread(target=listen_thread)
        thread.daemon = True
        thread.start()
        return thread
    
    def speak(self, text, callback=None):
        """Convert text to speech with current voice mode settings."""
        def speak_thread():
            self.is_speaking = True
            try:
                self._configure_tts_voice()
                
                # Apply alien voice effects
                if self.current_voice_mode == "Alien":
                    text = self._apply_alien_effects(text)
                
                print(f"Speaking: {text}")
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                
                if callback:
                    callback()
                    
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                self.is_speaking = False
        
        # Run TTS in a separate thread
        thread = threading.Thread(target=speak_thread)
        thread.daemon = True
        thread.start()
        return thread
    
    def _apply_alien_effects(self, text):
        """Apply alien-like effects to text (simple implementation)."""
        # Add some robotic spacing and emphasis
        words = text.split()
        alien_words = []
        
        for word in words:
            # Add emphasis to certain syllables
            if len(word) > 3:
                alien_word = word[:2] + "." + word[2:]
                alien_words.append(alien_word)
            else:
                alien_words.append(word)
        
        return " ".join(alien_words)
    
    def stop_speaking(self):
        """Stop current TTS playback."""
        try:
            self.tts_engine.stop()
            self.is_speaking = False
        except Exception as e:
            print(f"Error stopping TTS: {e}")
    
    def get_available_voices(self):
        """Get list of available TTS voices."""
        voices = self.tts_engine.getProperty('voices')
        return [voice.name for voice in voices] if voices else [] 