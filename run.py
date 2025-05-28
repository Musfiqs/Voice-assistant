#!/usr/bin/env python3
"""
Quick launcher for the Futuristic Voice Assistant.
This script provides a simple way to start the application.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main_window import main
    
    if __name__ == "__main__":
        print("🤖 Starting Futuristic Voice Assistant...")
        print("📝 Make sure you have set your OPENAI_API_KEY environment variable")
        print("🎤 Ensure your microphone is connected and working")
        print("🔊 Check that your speakers/headphones are ready")
        print("=" * 50)
        
        main()
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Make sure you have installed all dependencies:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting application: {e}")
    sys.exit(1) 