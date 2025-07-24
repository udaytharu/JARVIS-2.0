# ===================== Imports and Setup =====================
from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextTOScreen,
    TempDirectoryPath,
    AnswerModifier,
    QueryModifier,
    GetAssistantStatus
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.Navigation import (
    get_navigator, universal_navigator,
    ScrollUp, ScrollDown, SwipeLeft, SwipeRight, SwipeUp, SwipeDown
)
import pyautogui
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech, play_audio_file
from Backend.ImageGeneration import GenerateImages
from dotenv import dotenv_values
from asyncio import run
from time import sleep, time, localtime
import subprocess
import threading
import json
import os
import logging
import sys
import pyaudio
import numpy as np

# ===================== Logging and Environment =====================
# Remove or comment out logging.basicConfig if it writes to a file
# Only keep console logging if needed
env_vars = dotenv_values(".env")
USERNAME = env_vars.get("Username", "User")
ASSISTANT_NAME = env_vars.get("Assistantname", "Assistant")
DEFAULT_MESSAGE = f'''{USERNAME} 😄: Hello {ASSISTANT_NAME} 🌟, How are you?\n{ASSISTANT_NAME} 🤖: Welcome {USERNAME} 🎉, I am doing well. How may I help you today? 😊'''
subprocesses = []
FUNCTIONS = ["open", "close", "play", "system", "content", "google search", "youtube search", "write", "create presentation", 
             "scroll", "swipe", "pdf", "youtube", "web", "zoom", "page", "home", "end", "next", "previous", "up", "down", 
             "enter", "escape", "tab", "backspace", "delete", "select", "copy", "paste", "cut", "undo", "redo", "save", 
             "find", "replace", "refresh", "fullscreen"]
os.makedirs("Data", exist_ok=True)
os.makedirs(os.path.join("Frontend", "Files"), exist_ok=True)
last_interaction_time = time()

# ===================== Utility Functions =====================
def detect_clap():
    """Detect a clap sound using the microphone."""
    CHUNK = 1024
    RATE = 44100
    THRESHOLD = 3000
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.float32)
        stream.stop_stream()
        stream.close()
        p.terminate()
        amplitude = np.abs(np.max(data))
        logging.debug(f"Clap detection: Amplitude = {amplitude}, Threshold = {THRESHOLD}")
        return amplitude > THRESHOLD
    except Exception as e:
        logging.error(f"Error in clap detection: {e}")
        return False

def show_default_chat_if_no_chats():
    """Show default chat if no previous chats exist."""
    chat_log_path = r"Data\ChatLog.json"
    try:
        with open(chat_log_path, "r", encoding='utf-8') as file:
            if len(file.read()) < 5:
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
                    file.write("")
                with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
                    file.write(DEFAULT_MESSAGE)
    except FileNotFoundError:
        with open(chat_log_path, "w", encoding='utf-8') as file:
            json.dump([], file)
        with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
            file.write("")
        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
            file.write(DEFAULT_MESSAGE)

def read_chat_log_json():
    """Read chat log from JSON file."""
    chat_log_path = r"Data\ChatLog.json"
    try:
        with open(chat_log_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def chat_log_integration():
    """Integrate chat log for display."""
    json_data = read_chat_log_json()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{USERNAME}: {entry['content']} 😄\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{ASSISTANT_NAME}: {entry['content']} 🌟\n"
    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def show_chats_on_gui():
    """Display chats on the GUI."""
    with open(TempDirectoryPath('Database.data'), 'r', encoding='utf-8') as file:
        data = file.read()
    if data:
        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:
            file.write(data)

def greet_user_by_time():
    """Greet the user based on the current time."""
    play_audio_file(r"Frontend/audio/start_sound.mp3")
    current_hour = localtime().tm_hour
    if 5 <= current_hour < 12:
        greeting = f"Good morning, boss! welcome back I'm {ASSISTANT_NAME}, your personal AI assistant. How can I help to improve your productivity?"
    elif 12 <= current_hour < 17:
        greeting = f"Good afternoon, boss! I'm {ASSISTANT_NAME}, your personal AI assistant. welcome back How can I help you today?"
    else:
        greeting = f"Good evening, boss! I'm {ASSISTANT_NAME}, your personal AI assistant. welcome back Ready to assist you."
    ShowTextTOScreen(f"{ASSISTANT_NAME} 🤖: {greeting}")
    TextToSpeech(greeting)
    sleep(0.5)

def check_system():
    """Check if all required system components exist."""
    components = ["Backend", "Frontend", "Data"]
    for component in components:
        if not os.path.isdir(component):
            ShowTextTOScreen(f"{ASSISTANT_NAME}: Error - {component} directory missing! 🚫")
            TextToSpeech(f"Error - {component} directory missing")
            return False
    return True

# ===================== Main Assistant Functions =====================
def initial_execution():
    """Run initial setup and greetings."""
    global last_interaction_time
    ShowTextTOScreen(f"{ASSISTANT_NAME} 🤖: Initializing...")
    TextToSpeech("System initializing")
    sleep(0.5)
    if not check_system():
        ShowTextTOScreen(f"{ASSISTANT_NAME} 🤖: Initialization failed. Please fix issues and restart.")
        TextToSpeech("Initialization failed. Please fix issues and restart.")
        sys.exit(1)
    show_default_chat_if_no_chats()
    chat_log_integration()
    show_chats_on_gui()
    greet_user_by_time()
    SetAssistantStatus("Available... ✅")
    last_interaction_time = time()

initial_execution()

def shutdown_assistant():
    """Graceful and robust shutdown with user confirmation and cleanup."""
    try:
        SetAssistantStatus("Shutting down... 🔚")
        ShowTextTOScreen(f"{ASSISTANT_NAME}: Goodbye {USERNAME}! Please say 'bye' to confirm shutdown or 'cancel' to abort.")
        TextToSpeech("Goodbye! Please say bye to confirm shutdown or say cancel to abort.")
        sleep(2)
        user_response = SpeechRecognition().lower().strip()
        if any(bye_word in user_response for bye_word in ["bye", "goodbye"]):
            # Attempt to terminate all subprocesses
            for p in subprocesses:
                try:
                    if p.poll() is None:
                        p.terminate()
                        p.wait(timeout=5)
                except Exception:
                    try:
                        p.kill()
                    except Exception:
                        pass
            # Optionally save logs or state here
            ShowTextTOScreen(f"{ASSISTANT_NAME}: System shutdown complete. See you next time, {USERNAME}!")
            TextToSpeech("System shutdown complete. See you next time!")
            sleep(1)
            sys.exit(0)
        else:
            SetAssistantStatus("Available... ✅")
            ShowTextTOScreen(f"{ASSISTANT_NAME}: Shutdown cancelled. I'm back and ready to help! 😄")
            TextToSpeech("Shutdown cancelled. I'm back and ready to help!")
    except Exception as e:
        logging.error(f"Error during shutdown: {e}")
        SetAssistantStatus("Error during shutdown!")
        ShowTextTOScreen(f"{ASSISTANT_NAME}: Error during shutdown: {e}")
        TextToSpeech("An error occurred during shutdown. Please try again or close the program manually.")

def execute_navigation_commands(commands):
    """Execute navigation commands directly."""
    results = []
    
    for command in commands:
        cmd = command.strip().lower()
        if not cmd:
            continue
            
        try:
            # Basic Scroll and Swipe Commands
            if cmd.startswith("scroll up"):
                amount = 3
                if " by " in cmd:
                    try:
                        amount = int(cmd.split(" by ")[1].split()[0])
                    except (ValueError, IndexError):
                        pass
                results.append(ScrollUp(amount))
            elif cmd.startswith("scroll down"):
                amount = 3
                if " by " in cmd:
                    try:
                        amount = int(cmd.split(" by ")[1].split()[0])
                    except (ValueError, IndexError):
                        pass
                results.append(ScrollDown(amount))
            elif cmd.startswith("swipe left"):
                amount = 100
                if " by " in cmd:
                    try:
                        amount = int(cmd.split(" by ")[1].split()[0])
                    except (ValueError, IndexError):
                        pass
                results.append(SwipeLeft(amount))
            elif cmd.startswith("swipe right"):
                amount = 100
                if " by " in cmd:
                    try:
                        amount = int(cmd.split(" by ")[1].split()[0])
                    except (ValueError, IndexError):
                        pass
                results.append(SwipeRight(amount))
            elif cmd.startswith("swipe up"):
                amount = 100
                if " by " in cmd:
                    try:
                        amount = int(cmd.split(" by ")[1].split()[0])
                    except (ValueError, IndexError):
                        pass
                results.append(SwipeUp(amount))
            elif cmd.startswith("swipe down"):
                amount = 100
                if " by " in cmd:
                    try:
                        amount = int(cmd.split(" by ")[1].split()[0])
                    except (ValueError, IndexError):
                        pass
                results.append(SwipeDown(amount))
            # Universal Navigation Commands (works in any application)
            elif cmd.startswith("zoom in"):
                results.append(universal_navigator.zoom_in())
            elif cmd.startswith("zoom out"):
                results.append(universal_navigator.zoom_out())
            elif cmd.startswith("reset zoom"):
                results.append(universal_navigator.reset_zoom())
            elif cmd.startswith("page up"):
                results.append(universal_navigator.page_up())
            elif cmd.startswith("page down"):
                results.append(universal_navigator.page_down())
            elif cmd.startswith("go home") or cmd.startswith("home"):
                results.append(universal_navigator.home())
            elif cmd.startswith("go end") or cmd.startswith("end"):
                results.append(universal_navigator.end())
            elif cmd.startswith("next") or cmd.startswith("next item"):
                results.append(universal_navigator.next_item())
            elif cmd.startswith("previous") or cmd.startswith("previous item"):
                results.append(universal_navigator.previous_item())
            elif cmd.startswith("up") or cmd.startswith("up item"):
                results.append(universal_navigator.up_item())
            elif cmd.startswith("down") or cmd.startswith("down item"):
                results.append(universal_navigator.down_item())
            elif cmd.startswith("enter"):
                results.append(universal_navigator.enter())
            elif cmd.startswith("escape") or cmd.startswith("esc"):
                results.append(universal_navigator.escape())
            elif cmd.startswith("tab"):
                results.append(universal_navigator.tab())
            elif cmd.startswith("backspace"):
                results.append(universal_navigator.backspace())
            elif cmd.startswith("delete"):
                results.append(universal_navigator.delete())
            elif cmd.startswith("select all"):
                results.append(universal_navigator.select_all())
            elif cmd.startswith("copy"):
                results.append(universal_navigator.copy())
            elif cmd.startswith("paste"):
                results.append(universal_navigator.paste())
            elif cmd.startswith("cut"):
                results.append(universal_navigator.cut())
            elif cmd.startswith("undo"):
                results.append(universal_navigator.undo())
            elif cmd.startswith("redo"):
                results.append(universal_navigator.redo())
            elif cmd.startswith("save"):
                results.append(universal_navigator.save())
            elif cmd.startswith("open file"):
                results.append(universal_navigator.open_file())
            elif cmd.startswith("new file"):
                results.append(universal_navigator.new_file())
            elif cmd.startswith("print"):
                results.append(universal_navigator.print_file())
            elif cmd.startswith("find"):
                results.append(universal_navigator.find())
            elif cmd.startswith("replace"):
                results.append(universal_navigator.replace())
            elif cmd.startswith("refresh"):
                results.append(universal_navigator.refresh())
            elif cmd.startswith("fullscreen"):
                results.append(universal_navigator.fullscreen())
            # Legacy PDF Navigation Commands (for backward compatibility)
            elif cmd.startswith("pdf next page"):
                results.append(universal_navigator.next_item())
            elif cmd.startswith("pdf previous page"):
                results.append(universal_navigator.previous_item())
            elif cmd.startswith("pdf zoom in"):
                results.append(universal_navigator.zoom_in())
            elif cmd.startswith("pdf zoom out"):
                results.append(universal_navigator.zoom_out())
            elif cmd.startswith("pdf go to page"):
                try:
                    page_number = int(cmd.split("page")[-1].strip())
                    # Use Ctrl+G for go to page (works in most PDF readers)
                    universal_navigator.find()
                    pyautogui.write(str(page_number))
                    results.append(universal_navigator.enter())
                except (ValueError, IndexError):
                    logging.error("Invalid page number for PDF navigation")
                    results.append(False)
            elif cmd.startswith("pdf scroll up"):
                amount = 3
                if " by " in cmd:
                    try:
                        amount = int(cmd.split(" by ")[1].split()[0])
                    except (ValueError, IndexError):
                        pass
                results.append(universal_navigator.scroll_up(amount))
            elif cmd.startswith("pdf scroll down"):
                amount = 3
                if " by " in cmd:
                    try:
                        amount = int(cmd.split(" by ")[1].split()[0])
                    except (ValueError, IndexError):
                        pass
                results.append(universal_navigator.scroll_down(amount))
            # Legacy YouTube Navigation Commands (for backward compatibility)
            elif cmd.startswith("youtube play") or cmd.startswith("youtube pause"):
                results.append(universal_navigator.enter())
            elif cmd.startswith("youtube skip forward"):
                results.append(universal_navigator.next_item())
            elif cmd.startswith("youtube skip backward"):
                results.append(universal_navigator.previous_item())
            elif cmd.startswith("youtube fullscreen"):
                results.append(universal_navigator.fullscreen())
            elif cmd.startswith("youtube volume up"):
                results.append(universal_navigator.up_item())
            elif cmd.startswith("youtube volume down"):
                results.append(universal_navigator.down_item())
            elif cmd.startswith("youtube next video"):
                results.append(universal_navigator.next_item())
            elif cmd.startswith("youtube previous video"):
                results.append(universal_navigator.previous_item())
            elif cmd.startswith("youtube scroll feed up"):
                amount = 3
                if " by " in cmd:
                    try:
                        amount = int(cmd.split(" by ")[1].split()[0])
                    except (ValueError, IndexError):
                        pass
                results.append(universal_navigator.scroll_up(amount))
            elif cmd.startswith("youtube scroll feed down"):
                amount = 3
                if " by " in cmd:
                    try:
                        amount = int(cmd.split(" by ")[1].split()[0])
                    except (ValueError, IndexError):
                        pass
                results.append(universal_navigator.scroll_down(amount))
            # Legacy Web Navigation Commands (for backward compatibility)
            elif cmd.startswith("web scroll up"):
                amount = 3
                if " by " in cmd:
                    try:
                        amount = int(cmd.split(" by ")[1].split()[0])
                    except (ValueError, IndexError):
                        pass
                results.append(universal_navigator.scroll_up(amount))
            elif cmd.startswith("web scroll down"):
                amount = 3
                if " by " in cmd:
                    try:
                        amount = int(cmd.split(" by ")[1].split()[0])
                    except (ValueError, IndexError):
                        pass
                results.append(universal_navigator.scroll_down(amount))
            elif cmd.startswith("web refresh"):
                results.append(universal_navigator.refresh())
            elif cmd.startswith("web go back"):
                try:
                    pyautogui.press('alt', 'left')
                    logging.info("Went back in browser history")
                    results.append(True)
                except Exception as e:
                    logging.error(f"Failed to go back: {str(e)}")
                    results.append(False)
            elif cmd.startswith("web go forward"):
                try:
                    pyautogui.press('alt', 'right')
                    logging.info("Went forward in browser history")
                    results.append(True)
                except Exception as e:
                    logging.error(f"Failed to go forward: {str(e)}")
                    results.append(False)
            else:
                logging.warning(f"Unknown navigation command: {cmd}")
                results.append(False)
        except Exception as e:
            logging.error(f"Navigation command processing error: {str(e)}")
            results.append(False)

    return results

def main_execution():
    """Main user interaction and task execution loop."""
    global last_interaction_time
    SetAssistantStatus("Listening... 👂")
    query = SpeechRecognition()
    if not query or not query.strip():
        return  # Do nothing if no user input
    last_interaction_time = time()
    ShowTextTOScreen(f"{USERNAME}: {query} 😄")
    SetAssistantStatus("Thinking... 🤔")
    decision = FirstLayerDMM(query)
    logging.info(f"Decision: {decision}")
    image_execution = any("generate image" in q for q in decision)
    task_execution = any(any(q.startswith(func) for func in FUNCTIONS) for q in decision)
    merged_query = " and ".join([" ".join(q.split()[1:]) for q in decision if q.startswith("general") or q.startswith("realtime")])
    # Image generation
    if image_execution:
        ShowTextTOScreen(f"{ASSISTANT_NAME} 🤖: Generating image...")
        threading.Thread(target=TextToSpeech, args=("Generating image",), daemon=True).start()
        with open(r"Frontend\Files\ImageGeneration.data", 'w') as file:
            file.write(f"{query}, True")
        try:
            p1 = subprocess.Popen(
                ['python', r'Backend\ImageGeneration.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=False
            )
            subprocesses.append(p1)
            sleep(1)
            SetAssistantStatus("Available... ✅")
            ShowTextTOScreen(f"{ASSISTANT_NAME}: Image generated! 🎉")
            threading.Thread(target=TextToSpeech, args=("Image generated!",), daemon=True).start()
        except Exception as e:
            logging.error(f"Error starting ImageGeneration.py: {e}")
            ShowTextTOScreen(f"{ASSISTANT_NAME}: Image generation failed. Retry? 😞")
            threading.Thread(target=TextToSpeech, args=("Image generation failed. Please retry.",), daemon=True).start()
        return True
    # Navigation execution
    navigation_commands = [q for q in decision if any(q.startswith(nav) for nav in [
        "scroll", "swipe", "pdf", "youtube", "web", "zoom", "page", "home", "end", "next", "previous", 
        "up", "down", "enter", "escape", "tab", "backspace", "delete", "select", "copy", "paste", 
        "cut", "undo", "redo", "save", "find", "replace", "refresh", "fullscreen"
    ])]
    if navigation_commands:
        SetAssistantStatus("Navigating... 🧭")
        def run_navigation():
            try:
                success = execute_navigation_commands(navigation_commands)
                SetAssistantStatus("Available... ✅")
                if success and all(success):
                    ShowTextTOScreen(f"{ASSISTANT_NAME}: Navigation completed! 🎉")
                    threading.Thread(target=TextToSpeech, args=("Navigation completed!",), daemon=True).start()
                else:
                    ShowTextTOScreen(f"{ASSISTANT_NAME}: Navigation completed with some issues. 😞")
                    threading.Thread(target=TextToSpeech, args=("Navigation completed with some issues.",), daemon=True).start()
            except Exception as e:
                logging.error(f"Navigation execution error: {e}")
                SetAssistantStatus("Available... ✅")
                ShowTextTOScreen(f"{ASSISTANT_NAME}: Navigation failed. Please try again. 😞")
                threading.Thread(target=TextToSpeech, args=("Navigation failed. Please try again.",), daemon=True).start()
        threading.Thread(target=run_navigation, daemon=True).start()
        return True
    
    # Task execution (non-navigation)
    automation_commands = [q for q in decision if any(q.startswith(func) for func in ["open", "close", "play", "system", "content", "google search", "youtube search", "write", "create presentation"])]
    if automation_commands:
        SetAssistantStatus("Executing... 🚀")
        def run_automation():
            from asyncio import run as asyncio_run
            success = asyncio_run(Automation(automation_commands))
            SetAssistantStatus("Available... ✅")
            if success:
                ShowTextTOScreen(f"{ASSISTANT_NAME}: Command completed! 🎉")
                threading.Thread(target=TextToSpeech, args=("Command completed!",), daemon=True).start()
            else:
                ShowTextTOScreen(f"{ASSISTANT_NAME}: Command failed. Try again? 😞")
                threading.Thread(target=TextToSpeech, args=("Command failed. Please try again.",), daemon=True).start()
        threading.Thread(target=run_automation, daemon=True).start()
        return True
    # Realtime/general queries
    if any(q.startswith("realtime") for q in decision):
        SetAssistantStatus("Searching... 🔍")
        ShowTextTOScreen(f"{ASSISTANT_NAME} 🤖: Searching for your query... 🔍")
        threading.Thread(target=TextToSpeech, args=("Searching for your query",), daemon=True).start()
        def run_realtime():
            answer = RealtimeSearchEngine(QueryModifier(merged_query))
            ShowTextTOScreen(f"{ASSISTANT_NAME}: {answer} 🌐")
            SetAssistantStatus("Answering... 💬")
            threading.Thread(target=TextToSpeech, args=(answer,), daemon=True).start()
        threading.Thread(target=run_realtime, daemon=True).start()
        return True
    for q in decision:
        if "general" in q:
            SetAssistantStatus("Thinking... 🤔")
            def run_general():
                answer = ChatBot(QueryModifier(q.replace("general ", "")))
                ShowTextTOScreen(f"{ASSISTANT_NAME}: {answer} 🌟")
                SetAssistantStatus("Answering... 💬")
                threading.Thread(target=TextToSpeech, args=(answer,), daemon=True).start()
            threading.Thread(target=run_general, daemon=True).start()
            return True
        elif any(word in q.lower() for word in ["exit", "bye", "goodbye"]):
            shutdown_assistant()
            return True

def sleep_assistant():
    """Put the assistant into sleep state until user says 'wake up' or 'get up'."""
    SetAssistantStatus("Sleeping... 😴")
    ShowTextTOScreen(f"{ASSISTANT_NAME} 🤖: I am now sleeping. Say 'wake up' or 'get up' to continue.")
    TextToSpeech("I am now sleeping. Say wake up or get up to continue.")
    while True:
        query = SpeechRecognition()
        if query and any(phrase in query.lower() for phrase in ["wake up", "get up"]):
            SetAssistantStatus("Available... ✅")
            ShowTextTOScreen(f"{ASSISTANT_NAME} 🤖: I'm back and ready to help!")
            TextToSpeech("I'm back and ready to help!")
            break
        sleep(0.5)

# ===================== Threaded Main Loop =====================
def first_thread():
    global last_interaction_time
    while True:
        current_time = time()
        if (current_time - last_interaction_time) > 60:
            sleep_assistant()
            last_interaction_time = time()
        else:
            main_execution()
        sleep(0.1)

def second_thread():
    GraphicalUserInterface()

if __name__ == "__main__":
    thread1 = threading.Thread(target=first_thread, daemon=True)
    thread1.start()
    second_thread()