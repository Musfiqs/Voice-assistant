#!/usr/bin/env python3
"""
Setup script for the Futuristic Voice Assistant.
Helps with installation and initial configuration.
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def install_dependencies():
    """Install required Python packages."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("💡 Try running: pip install -r requirements.txt")
        return False

def check_api_key():
    """Check if OpenAI API key is configured."""
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your-openai-api-key-here':
        print("✅ OpenAI API key found in environment")
        return True
    else:
        print("⚠️  OpenAI API key not found or not set")
        print("💡 Set your API key using one of these methods:")
        print("   1. Environment variable: export OPENAI_API_KEY='your-key-here'")
        print("   2. Edit config.py and replace the placeholder")
        return False

def test_audio_devices():
    """Test if audio devices are available."""
    try:
        import pyaudio
        
        # Test microphone
        p = pyaudio.PyAudio()
        mic_count = 0
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                mic_count += 1
        
        p.terminate()
        
        if mic_count > 0:
            print(f"✅ Found {mic_count} microphone device(s)")
            return True
        else:
            print("⚠️  No microphone devices found")
            return False
            
    except ImportError:
        print("⚠️  PyAudio not installed - audio test skipped")
        return False
    except Exception as e:
        print(f"⚠️  Audio test failed: {e}")
        return False

def create_example_env():
    """Create an example environment file."""
    env_content = '''# Environment file for Futuristic Voice Assistant
# Set your OpenAI API key here

OPENAI_API_KEY=your-openai-api-key-here

# Optional: Customize OpenAI model (default: gpt-4)
# OPENAI_MODEL=gpt-3.5-turbo

# Instructions:
# 1. Get your OpenAI API key from: https://platform.openai.com/api-keys
# 2. Replace 'your-openai-api-key-here' with your actual API key
# 3. Save this file
# 4. Set the environment variable: export OPENAI_API_KEY='your-key-here'
'''
    
    try:
        with open('env_example.txt', 'w') as f:
            f.write(env_content)
        print("✅ Created env_example.txt with API key instructions")
        return True
    except Exception as e:
        print(f"⚠️  Could not create env_example.txt: {e}")
        return False

def main():
    """Main setup function."""
    print("🤖 Futuristic Voice Assistant Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\n📋 Checking system requirements...")
    
    # Install dependencies
    deps_ok = install_dependencies()
    
    # Check API key
    api_key_ok = check_api_key()
    
    # Test audio
    audio_ok = test_audio_devices()
    
    # Create example env file
    create_example_env()
    
    print("\n" + "=" * 40)
    print("📊 Setup Summary:")
    print(f"   Dependencies: {'✅' if deps_ok else '❌'}")
    print(f"   OpenAI API Key: {'✅' if api_key_ok else '⚠️'}")
    print(f"   Audio Devices: {'✅' if audio_ok else '⚠️'}")
    
    if deps_ok and api_key_ok and audio_ok:
        print("\n🎉 Setup complete! You can now run the application:")
        print("   python main_window.py")
        print("   or")
        print("   python run.py")
    else:
        print("\n⚠️  Setup incomplete. Please resolve the issues above.")
        if not api_key_ok:
            print("\n📝 To set your OpenAI API key:")
            print("   export OPENAI_API_KEY='your-actual-api-key-here'")
        if not audio_ok:
            print("\n🎤 Audio issues may affect voice recognition.")
            print("   Make sure your microphone is connected and working.")

if __name__ == "__main__":
    main() 