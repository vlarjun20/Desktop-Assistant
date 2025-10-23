from openai import OpenAI
import speech_recognition as sr, pyttsx3, pyautogui, os, webbrowser, psutil, subprocess

openai = OpenAI(api_key="ollama", base_url="http://localhost:11434")
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        audio = recognizer.listen(source)
    try:
        cmd = recognizer.recognize_google(audio)
        print("You:", cmd)
        return cmd.lower()
    except:
        return ""

def open_app(app_name):
    apps = {
        "chrome": "chrome",
        "notepad": "notepad",
        "word": "winword",
        "excel": "excel",
        "spotify": "spotify",
        "file explorer": "explorer",
        "cmd": "cmd",
        "calculator": "calc",
        "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        "telegram": r"C:\Users\ARJUN\AppData\Roaming\Telegram Desktop\Telegram.exe",
        "edge": "msedge",
        "discord": r"C:\Users\ARJUN\AppData\Local\Discord\Update.exe",
        "whatsapp": r"C:\Users\ARJUN\AppData\Local\WhatsApp\WhatsApp.exe"

    }
    for key, value in apps.items():
        if key in app_name:
            os.system(f"start {value}")
            speak(f"Opening {key}")
            return True
    return False

def execute_command(text):
    if "open" in text:
        if open_app(text): return
        if "youtube" in text:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")
        elif "google" in text:
            webbrowser.open("https://google.com")
            speak("Opening Google")
        else:
            speak("App not found in my list.")
    elif "screenshot" in text:
        pyautogui.screenshot("screenshot.png")
        speak("Screenshot taken.")
    elif "type" in text:
        pyautogui.typewrite(text.replace("type", "").strip())
    elif "volume up" in text:
        pyautogui.press("volumeup")
        speak("Increasing volume.")
    elif "volume down" in text:
        pyautogui.press("volumedown")
        speak("Decreasing volume.")
    elif "close" in text:
        for proc in psutil.process_iter():
            if any(app in proc.name().lower() for app in ["chrome", "word", "excel"]):
                proc.kill()
                speak(f"Closed {proc.name()}")
    else:
        speak("Let me check that...")
        messages = [
    {
        "role": "system",
        "content": (
            "You are Jarvis, an intelligent AI assistant that runs on a user’s personal computer. "
            "You can interpret both text and voice commands to perform desktop automation tasks. "
            "Your role is to understand user intent and convert it into clear, executable actions."
            "\n\n"
            "=== Capabilities ===\n"
            "- You can open, close, and control applications (e.g., Chrome, WhatsApp, Word, Excel, Spotify, File Explorer, Notepad, CMD, Calculator).\n"
            "- You can perform general tasks like taking screenshots, typing text, adjusting volume, or searching the web.\n"
            "- You provide short, friendly spoken confirmations when tasks are executed (e.g., 'Opening Chrome', 'Screenshot saved').\n"
            "- You can also explain what command should be executed in plain English if asked.\n\n"
            "=== Behavioral Rules ===\n"
            "1. Be concise and polite — no long explanations unless requested.\n"
            "2. When a command cannot be executed, suggest what the user can try instead.\n"
            "3. Never perform destructive operations (like deleting files, formatting disks, or installing software) unless explicitly confirmed.\n"
            "4. Always assume you are interacting with a real Windows or Linux desktop environment.\n"
            "5. Your output should describe what to do, not raw Python or PowerShell code.\n"
            "6. For web tasks, prefer 'open YouTube', 'search Google', etc.\n"
            "7. For voice responses, speak naturally (e.g., 'Sure, I’m on it!' or 'Done!')."
        )
    },
    {
        "role": "user",
        "content": "User says: Open Chrome and search for latest AI news."
    }
]

        llm_reply = openai.chat.completions.create(
            model="llama3.2:latest",
            messages=messages
        )
        speak(llm_reply['choices'][0]['message']['content'])

speak("Hello! I'm ready.")
while True:
    command = listen()
    if "stop" in command or "exit" in command:
        speak("Goodbye!")
        break
    execute_command(command)
