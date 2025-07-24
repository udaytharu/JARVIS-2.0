import speech_recognition as sr
from dotenv import dotenv_values
import os
import mtranslate as mt
import logging
from threading import Lock

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")

# Initialize recognizer with optimized settings
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300  # Lower threshold for better sensitivity
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8  # Shorter pause for faster response
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5

# Thread lock for microphone access
mic_lock = Lock()

def SetAssistantStatus(Status):
    """Set assistant status with error handling."""
    try:
        current_dir = os.getcwd()
        temp_dir = os.path.join(current_dir, "Frontend", "Files")
        with open(os.path.join(temp_dir, 'Status.data'), "w", encoding='utf-8') as file:
            file.write(Status)
    except Exception as e:
        logging.error(f"Error setting assistant status: {e}")

def QueryModifier(Query):
    """Format query with proper punctuation."""
    if not Query:
        return ""
    
    new_query = Query.lower().strip()
    question_words = ["how", "what", "where", "when", "which", "why", "who", "whose", "whom", "can", "you", "what's", "where's", "how's"]
    
    # Check if it's a question
    is_question = any(word in new_query for word in question_words)
    
    # Remove existing punctuation and add appropriate one
    new_query = new_query.rstrip('.!?')
    
    if is_question:
        new_query += "?"
    else:
        new_query += "."
    
    return new_query.capitalize()

def UniversalTranslator(Text):
    """Translate text to English if needed."""
    try:
        if InputLanguage.lower() != "en" and "en" not in InputLanguage.lower():
            english_translation = mt.translate(Text, "en", "auto")
            return english_translation.capitalize()
        return Text
    except Exception as e:
        logging.error(f"Translation error: {e}")
        return Text

def get_microphone():
    """Get the best available microphone."""
    try:
        # Try to get the default microphone
        mic = sr.Microphone()
        
        # Adjust for ambient noise
        with mic_lock:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        return mic
    except Exception as e:
        logging.error(f"Error getting microphone: {e}")
        return None

def SpeechRecognition():
    """Enhanced speech recognition with better performance."""
    mic = get_microphone()
    if not mic:
        logging.error("No microphone available")
        return ""
    
    try:
        with mic_lock:
            with mic as source:
                SetAssistantStatus("Listening... 👂")
                
                # Listen for audio with timeout
                audio = recognizer.listen(
                    source, 
                    timeout=5, 
                    phrase_time_limit=10
                )
        
        SetAssistantStatus("Processing... 🤔")
        
        # Try multiple recognition services for better accuracy
        text = ""
        
        # First try Google Speech Recognition
        try:
            text = recognizer.recognize_google(
                audio, 
                language=InputLanguage
            )
        except sr.UnknownValueError:
            logging.debug("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logging.warning(f"Google Speech Recognition error: {e}")
        
        # Fallback to Sphinx if Google fails
        if not text:
            try:
                text = recognizer.recognize_sphinx(audio)
            except sr.UnknownValueError:
                logging.debug("Sphinx could not understand audio")
            except Exception as e:
                logging.error(f"Sphinx error: {e}")
        
        if text:
            # Translate if needed
            if InputLanguage.lower() != "en" and "en" not in InputLanguage.lower():
                SetAssistantStatus("Translating... 🌐")
                text = UniversalTranslator(text)
            
            return QueryModifier(text)
        else:
            return ""
            
    except sr.WaitTimeoutError:
        logging.debug("No speech detected within timeout")
        return ""
    except Exception as e:
        logging.error(f"Speech recognition error: {e}")
        return ""

def SpeechRecognitionWithFallback():
    """Speech recognition with multiple fallback options."""
    # Try the main recognition method
    result = SpeechRecognition()
    
    if result:
        return result
    
    # If no result, try with different settings
    try:
        # Temporarily adjust settings for better sensitivity
        original_threshold = recognizer.energy_threshold
        recognizer.energy_threshold = 200
        
        result = SpeechRecognition()
        
        # Restore original settings
        recognizer.energy_threshold = original_threshold
        
        return result
    except Exception as e:
        logging.error(f"Fallback recognition error: {e}")
        return ""

if __name__ == "__main__":
    # Test the speech recognition
    print("Testing speech recognition...")
    print("Speak something...")
    
    while True:
        try:
            text = SpeechRecognitionWithFallback()
            if text:
                print(f"Recognized: {text}")
            else:
                print("No speech detected")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            