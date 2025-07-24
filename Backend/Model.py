import cohere
from rich import print
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
CohereAPIKey = env_vars.get("CohereAPIKey")

# Initialize Cohere Client
co = cohere.Client(api_key=CohereAPIKey)

# List of valid functions
funcs = [
    "exit", "general", "realtime", "open", "close", "play", "generate image", "system", "content", "google search", "youtube search", "reminder",
    "scroll", "swipe", "pdf", "youtube", "web", "zoom", "page", "home", "end", "next", "previous", "up", "down", 
    "enter", "escape", "tab", "backspace", "delete", "select", "copy", "paste", "cut", "undo", "redo", "save", 
    "find", "replace", "refresh", "fullscreen"
]

# Initialize messages and preamble prompt
messages = []
preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down , etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.
-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'youtube search 1st topic, youtube search 2nd topic' and so on.
-> Respond with 'scroll up (amount)' or 'scroll down (amount)' if a query is asking to scroll up or down like 'scroll up by 5', 'scroll down by 10', etc.
-> Respond with 'swipe left (amount)' or 'swipe right (amount)' or 'swipe up (amount)' or 'swipe down (amount)' if a query is asking to swipe in any direction like 'swipe left by 100', 'swipe right by 50', etc.
-> Respond with 'zoom in' or 'zoom out' if a query is asking to zoom in or out like 'zoom in', 'zoom out', etc.
-> Respond with 'page up' or 'page down' if a query is asking to go to previous or next page like 'page up', 'page down', etc.
-> Respond with 'home' or 'end' if a query is asking to go to beginning or end like 'go home', 'go to end', etc.
-> Respond with 'next' or 'previous' if a query is asking to go to next or previous item like 'next item', 'previous item', etc.
-> Respond with 'up' or 'down' if a query is asking to go up or down like 'go up', 'go down', etc.
-> Respond with 'enter' if a query is asking to press enter like 'press enter', 'hit enter', etc.
-> Respond with 'escape' if a query is asking to press escape like 'press escape', 'hit escape', etc.
-> Respond with 'tab' if a query is asking to press tab like 'press tab', 'hit tab', etc.
-> Respond with 'backspace' or 'delete' if a query is asking to delete like 'press backspace', 'press delete', etc.
-> Respond with 'select all' if a query is asking to select all like 'select all', 'select everything', etc.
-> Respond with 'copy' or 'paste' or 'cut' if a query is asking to copy, paste, or cut like 'copy this', 'paste that', 'cut this', etc.
-> Respond with 'undo' or 'redo' if a query is asking to undo or redo like 'undo that', 'redo that', etc.
-> Respond with 'save' if a query is asking to save like 'save this', 'save file', etc.
-> Respond with 'find' if a query is asking to find something like 'find text', 'search for', etc.
-> Respond with 'replace' if a query is asking to replace something like 'replace text', 'find and replace', etc.
-> Respond with 'refresh' if a query is asking to refresh like 'refresh page', 'reload', etc.
-> Respond with 'fullscreen' if a query is asking to go fullscreen like 'fullscreen', 'maximize', etc.
-> Respond with 'pdf next page' or 'pdf previous page' if a query is asking to navigate PDF pages like 'next page in PDF', 'previous page in PDF', etc.
-> Respond with 'pdf zoom in' or 'pdf zoom out' if a query is asking to zoom in PDF like 'zoom in PDF', 'zoom out PDF', etc.
-> Respond with 'pdf scroll up (amount)' or 'pdf scroll down (amount)' if a query is asking to scroll in PDF like 'scroll up in PDF by 5', 'scroll down in PDF by 10', etc.
-> Respond with 'youtube play' or 'youtube pause' if a query is asking to play or pause YouTube video like 'play video', 'pause video', etc.
-> Respond with 'youtube skip forward' or 'youtube skip backward' if a query is asking to skip in YouTube like 'skip forward', 'skip backward', etc.
-> Respond with 'youtube fullscreen' if a query is asking to go fullscreen in YouTube like 'fullscreen video', 'maximize video', etc.
-> Respond with 'youtube volume up' or 'youtube volume down' if a query is asking to change YouTube volume like 'volume up', 'volume down', etc.
-> Respond with 'youtube next video' or 'youtube previous video' if a query is asking to change YouTube videos like 'next video', 'previous video', etc.
-> Respond with 'youtube scroll feed up (amount)' or 'youtube scroll feed down (amount)' if a query is asking to scroll YouTube feed like 'scroll up in YouTube feed by 5', 'scroll down in YouTube feed by 10', etc.
-> Respond with 'web scroll up (amount)' or 'web scroll down (amount)' if a query is asking to scroll web page like 'scroll up in web page by 5', 'scroll down in web page by 10', etc.
-> Respond with 'web refresh' if a query is asking to refresh web page like 'refresh page', 'reload page', etc.
-> Respond with 'web go back' or 'web go forward' if a query is asking to navigate browser history like 'go back', 'go forward', etc.
*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp' ***
*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
"""

# Chat history
ChatHistory = [
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome and firefox"},
    {"role": "User", "message": "what is today's date and by the way remind me that i have a dancing performance on 5th aug at 11pm"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th aug dancing performance"},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me."}
]

def FirstLayerDMM(prompt: str = "test"):
    messages.append({"role": "user", "content": f"{prompt}"})
    stream = None
    try:
        # Initialize the generator
        stream = co.chat_stream(
            model='command-r-plus',
            message=prompt,
            temperature=0.7,
            chat_history=ChatHistory,
            prompt_truncation="OFF",
            connectors=[],
            preamble=preamble
        )

        response = ""

        # Collect the response from the generator
        for event in stream:
            if event.event_type == "text-generation":
                response += event.text

        # Process the response after collecting all text
        response = response.replace("\n", "").split(",")
        response = [i.strip() for i in response]

        # Filter valid tasks
        filtered_response = [
            task for task in response
            if any(task.startswith(func) for func in funcs)
        ]

        # Handle recursive case for "(query)"
        if "(query)" in filtered_response:
            return FirstLayerDMM(prompt=prompt)
        else:
            return filtered_response

    except Exception as e:
        print(f"Error: {e}")
        return ["general (query)"]  # Fallback response
    finally:
        # Ensure the generator is properly closed
        if stream is not None:
            stream.close()


if __name__ == "__main__":
    while True:
        print(FirstLayerDMM(input("--->")))
