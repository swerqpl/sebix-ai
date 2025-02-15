import os
import json
import wave
import tempfile
import threading
import pyperclip
import pyaudio
import whisper
import webbrowser
import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
from pynput import keyboard
from gtts import gTTS
from openai import OpenAI
import subprocess

# Set working directory to the application folder
os.chdir("/Users/")

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI()

# Global variables
is_recording = False
temp_wave_filename = None
audio_frames = []
audio_interface = None
notes_dir = "notes"
pressed_keys = []

# Ensure notes directory exists
if not os.path.exists(notes_dir):
    os.makedirs(notes_dir)

# Function to convert text to speech
def convert_text_to_speech(text):
    tts = gTTS(text=text, lang="pl")
    tts.save("response.mp3")
    os.system("afplay response.mp3")  # MacOS

# Function to record audio
def record_audio():
    global is_recording, audio_frames, audio_stream
    while is_recording:
        data = audio_stream.read(1024)
        audio_frames.append(data)

# Function to start recording
def start_audio_recording():
    global is_recording, audio_frames, audio_stream, audio_interface, temp_wave_filename
    is_recording = True
    audio_frames = []
    temp_wave_filename = tempfile.mktemp(suffix=".wav")
    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    threading.Thread(target=record_audio).start()

# Function to stop recording
def stop_audio_recording():
    global is_recording, audio_frames, audio_stream, audio_interface, temp_wave_filename
    is_recording = False
    audio_stream.stop_stream()
    audio_stream.close()
    audio_interface.terminate()
    
    with wave.open(temp_wave_filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio_interface.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b"".join(audio_frames))
    
    threading.Thread(target=transcribe_and_process_audio, args=(temp_wave_filename,)).start()

# Function to transcribe audio and process the text
def transcribe_and_process_audio(filename):
    model = whisper.load_model("small") 
    result = model.transcribe(filename, language="pl")  # Set language to Polish
    text = result["text"].strip()
    os.remove(filename)
    pyperclip.copy(text)
    process_text_with_gpt(text)

# Function to process text with GPT
def process_text_with_gpt(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "developer", "content": "Przetwarzasz polecenia głosowe i odpowiadaj po polsku krótko i zwięźle. Zwracasz JSON z tekstem do przeczytania oraz opcjonalnym poleceniem na urządzenie macOS. Jeśli użytkownik chce otworzyć stronę internetową lun coś pszeglądarkowe, zwróć pełny adres URL w polu web_command bez ''(działają tu te komendt na macOS). Jeśli chce otworzyć aplikację, zwróć jej nazwę w 'app_command'."},
                {"role": "user", "content": text}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "voice_assistant_response",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "description": "Tekst do przeczytania na głos",
                                "type": "string"
                            },
                            "web_command": {
                                "description": "Opcjonalne polecenie do otwarcia strony internetowej (ale działają tu jakie kolwiek komendy na macos)",
                                "type": "string"
                            },
                            "app_command": {
                                "description": "nazwa aplikacji do uruchomienia",
                                "type": "string"
                            },
                            "note_action": {
                                "description": "Działanie na notatkach: create, read, update, delete lub list",
                                "type": "string"
                            },
                            "note_name": {
                                "description": "Nazwa notatki, której dotyczy akcja",
                                "type": "string"
                            },
                            "note_content": {
                                "description": "Treść notatki do zapisania lub edycji",
                                "type": "string"
                            }
                        },
                        "additionalProperties": False
                    }
                }
            }
        )
        
        data = json.loads(response.choices[0].message.content)
        print("JSON response:", json.dumps(data, indent=2))  # Added JSON display
        text_to_read = data.get("text", "Nie rozumiem polecenia.")
        
        if "web_command" in data and data["web_command"]:
            execute_web_command(data["web_command"])
        if "app_command" in data and data["app_command"]:
            execute_app_command(data["app_command"])
        if "note_action" in data:
            handle_note_action(data)
        
        convert_text_to_speech(text_to_read)
    except Exception as e:
        print(f"Error processing text with GPT: {e}")

# Function to execute web commands
def execute_web_command(command):
    print(f"Executing web command: {command}")
    webbrowser.open(command)

# Function to execute app commands
def execute_app_command(command):
    print(f"Executing app command: {command}")
    try:
        subprocess.run(["open", "-a", command], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing app command: {e}")

# Function to handle note actions
def handle_note_action(data):
    action = data.get("note_action")
    name = data.get("note_name")
    content = data.get("note_content", "")
    
    if action == "create":
        create_note(name, content)
    elif action == "read":
        read_note(name)
    elif action == "update":
        update_note(name, content)
    elif action == "delete":
        delete_note(name)
    elif action == "list":
        list_notes()

# Functions for note management
def create_note(name, content):
    filepath = os.path.join(notes_dir, f"{name}.txt")
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Note '{name}' created.")
    convert_text_to_speech(f"Notatka o nazwie {name} została stworzona.")

def read_note(name):
    filepath = os.path.join(notes_dir, f"{name}.txt")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            content = f.read()
        print(f"Content of '{name}':\n{content}")
        convert_text_to_speech(content)
    else:
        print(f"Note '{name}' does not exist.")

def update_note(name, content):
    filepath = os.path.join(notes_dir, f"{name}.txt")
    if os.path.exists(filepath):
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Note '{name}' updated.")
        convert_text_to_speech(f"Notatka o nazwie {name} została zaktualizowana.")
    else:
        print(f"Note '{name}' does not exist.")

def delete_note(name):
    filepath = os.path.join(notes_dir, f"{name}.txt")
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Note '{name}' deleted.")
    else:
        print(f"Note '{name}' does not exist.")

def list_notes():
    files = os.listdir(notes_dir)
    notes = [f[:-4] for f in files if f.endswith(".txt")]
    print("Notes:", ", ".join(notes))
    convert_text_to_speech("Lista notatek: " + ", ".join(notes))

# Function to toggle recording state
def toggle_recording_state():
    if not is_recording:
        print("Recording...")
        start_audio_recording()
    else:
        print("Stop recording...")
        stop_audio_recording()

# Function to handle hotkey activation
def on_hotkey_activate():
    toggle_recording_state()

# Function to start the keyboard listener
def start_keyboard_listener():
    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+<shift>+r'),
        on_activate=on_hotkey_activate
    )
    with keyboard.Listener(
            on_press=hotkey.press,
            on_release=hotkey.release) as listener:
        listener.join()

if __name__ == "__main__":
    print("Press Ctrl + Shift + R to start recording")
    start_keyboard_listener()
