"""
AI Assistant Module for the Voice Assistant.
Handles OpenAI GPT integration and conversation management.
"""

import openai
import threading
from config import OPENAI_API_KEY, OPENAI_MODEL

class AIAssistant:
    def __init__(self):
        """Initialize the AI assistant with OpenAI configuration."""
        # Set up OpenAI client
        openai.api_key = OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Conversation history
        self.conversation_history = [
            {
                "role": "system",
                "content": """You are ARIA, a futuristic AI voice assistant. You are helpful, intelligent, and have a slightly futuristic personality. Keep your responses conversational and engaging, but concise enough for speech. You can help with various tasks, answer questions, and have friendly conversations. Always be respectful and helpful."""
            }
        ]
        
        self.is_processing = False
    
    def get_response(self, user_input, callback=None):
        """Get AI response from OpenAI GPT model."""
        def process_thread():
            self.is_processing = True
            try:
                # Add user message to conversation history
                self.conversation_history.append({
                    "role": "user",
                    "content": user_input
                })
                
                print(f"Sending to AI: {user_input}")
                
                # Get response from OpenAI
                response = self.client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=self.conversation_history,
                    max_tokens=500,
                    temperature=0.7,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
                
                # Extract the assistant's response
                ai_response = response.choices[0].message.content.strip()
                
                # Add assistant response to conversation history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": ai_response
                })
                
                # Keep conversation history manageable (last 10 exchanges)
                if len(self.conversation_history) > 21:  # system + 10 exchanges
                    self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-20:]
                
                print(f"AI Response: {ai_response}")
                
                if callback:
                    callback(ai_response, None)
                
                return ai_response
                
            except Exception as e:
                error_msg = f"AI Error: {str(e)}"
                print(error_msg)
                
                if callback:
                    callback(None, error_msg)
                
                return None
            finally:
                self.is_processing = False
        
        # Run AI processing in a separate thread
        thread = threading.Thread(target=process_thread)
        thread.daemon = True
        thread.start()
        return thread
    
    def clear_conversation(self):
        """Clear conversation history except system message."""
        self.conversation_history = [self.conversation_history[0]]
    
    def set_system_prompt(self, prompt):
        """Update the system prompt."""
        self.conversation_history[0]["content"] = prompt
    
    def get_conversation_summary(self):
        """Get a summary of the current conversation."""
        user_messages = [msg["content"] for msg in self.conversation_history if msg["role"] == "user"]
        assistant_messages = [msg["content"] for msg in self.conversation_history if msg["role"] == "assistant"]
        
        return {
            "total_exchanges": len(user_messages),
            "last_user_message": user_messages[-1] if user_messages else None,
            "last_assistant_message": assistant_messages[-1] if assistant_messages else None
        } 