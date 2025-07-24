import pygame
import random
import asyncio
import edge_tts
import os
import hashlib
import threading
from concurrent.futures import ThreadPoolExecutor
from dotenv import dotenv_values
import logging
import tempfile

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-US-JennyNeural")

# Initialize pygame mixer once
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Thread pool for async operations
executor = ThreadPoolExecutor(max_workers=2)

async def TextToAudioFile(text, voice=AssistantVoice) -> str:
    """Convert text to audio file without caching."""
    # Generate a temporary file path that won't be saved
    temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    # Generate new audio file
    try:
        communicate = edge_tts.Communicate(
            text, 
            voice, 
            pitch='-5Hz', 
            rate='+15%'
        )
        await communicate.save(temp_path)
        return temp_path
    except Exception as e:
        logging.error(f"Error generating audio: {e}")
        # Clean up temp file if generation failed
        try:
            os.remove(temp_path)
        except:
            pass
        return None

def play_audio_file(file_path, stop_callback=None):
    """Play audio file with better error handling."""
    try:
        if not os.path.exists(file_path):
            logging.error(f"Audio file not found: {file_path}")
            return False
        
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        # Wait for audio to finish
        while pygame.mixer.music.get_busy():
            if stop_callback and stop_callback():
                pygame.mixer.music.stop()
                return False
            pygame.time.Clock().tick(30)  # Higher FPS for smoother playback
        
        return True
    except Exception as e:
        logging.error(f"Error playing audio: {e}")
        return False

def SimpleTextToSpeech(Text):
    """Simple, reliable text-to-speech function without caching."""
    if not Text or not Text.strip():
        print("⚠️ No text provided for speech")
        return False
    
    text = str(Text).strip()
    print(f"🗣️ Speaking: '{text[:50]}...'")
    
    temp_file_path = None
    
    try:
        # Initialize pygame mixer if not already done
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            print("✅ Pygame mixer initialized")
        
        # Set volume to maximum
        pygame.mixer.music.set_volume(1.0)
        
        # Generate audio file
        print("🎤 Generating audio...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            temp_file_path = loop.run_until_complete(TextToAudioFile(text))
        finally:
            loop.close()
        
        if not temp_file_path:
            print("❌ Failed to generate audio file")
            return False
        
        print(f"📁 Temporary audio file created")
        
        # Play the audio
        print("▶️ Playing audio...")
        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()
        
        # Wait for audio to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(30)
        
        print("✅ Audio playback completed")
        return True
        
    except Exception as e:
        print(f"❌ Error in SimpleTextToSpeech: {e}")
        return False
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                print("🗑️ Temporary audio file cleaned up")
            except Exception as e:
                print(f"⚠️ Could not clean up temp file: {e}")

def TextToSpeech(Text, func=lambda r=None: True):
    """Optimized text-to-speech with smart truncation."""
    if not Text or not Text.strip():
        print("⚠️ No text provided for speech")
        return
    
    # Clean and prepare text
    text = str(Text).strip()
    print(f"🗣️ Attempting to speak: '{text[:50]}...'")
    
    try:
        # Responses for long text
        responses = [
            "The rest of the result has been printed to the chat screen, kindly check it out sir.",
            "The rest of the text is now on the chat screen, sir, please check it.",
            "You can see the rest of the text on the chat screen, sir.",
            "The remaining part of the text is now on the chat screen, sir.",
            "Sir, you'll find more text on the chat screen for you to see.",
            "The rest of the answer is now on the chat screen, sir.",
            "Sir, please look at the chat screen, the rest of the answer is there.",
            "You'll find the complete answer on the chat screen, sir.",
            "The next part of the text is on the chat screen, sir.",
            "Sir, please check the chat screen for more information."
        ]
        
        # Smart text truncation for better UX
        sentences = text.split(".")
        if len(sentences) > 4 and len(text) >= 250:
            # Speak first two sentences + response
            spoken_text = ".".join(sentences[:2]) + ". " + random.choice(responses)
            print(f"🗣️ Speaking truncated text: '{spoken_text[:50]}...'")
            result = SimpleTextToSpeech(spoken_text)
        else:
            # Speak full text
            print(f"🗣️ Speaking full text: '{text[:50]}...'")
            result = SimpleTextToSpeech(text)
        
        if result:
            print("✅ Text-to-speech completed successfully")
        else:
            print("❌ Text-to-speech failed")
            
    except Exception as e:
        print(f"❌ Error in TextToSpeech: {e}")
        logging.error(f"TextToSpeech error: {e}")

def TextToSpeechAsync(Text, func=lambda r=None: True):
    """Async version of text-to-speech for non-blocking operation."""
    def run_tts():
        TextToSpeech(Text, func)
    
    # Run in background thread
    thread = threading.Thread(target=run_tts, daemon=True)
    thread.start()
    return thread

if __name__ == "__main__":
    print("Text-to-Speech Test Mode")
    print("Enter text to speak (or 'quit' to exit):")
    
    while True:
        try:
            text = input("> ")
            if text.lower() == 'quit':
                break
            TextToSpeech(text)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    # Cleanup
    executor.shutdown(wait=True)
    pygame.mixer.quit()

