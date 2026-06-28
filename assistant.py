import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import requests
import subprocess
import sys

# ---------------- CONFIG ----------------
VOSK_MODEL_PATH = "vosk-model"
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "phi3"
SAMPLE_RATE = 16000
MIC_INDEX = 5    # Conexant SmartAudio HD (DirectSound)
# ----------------------------------------

print("Using mic index:", MIC_INDEX)
print("Using Vosk model at:", VOSK_MODEL_PATH)

model = Model(VOSK_MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)

def speak(text):
    print("Assistant:", text)
    subprocess.run([
        "powershell",
        "-Command",
        f"Add-Type -AssemblyName System.Speech; "
        f"(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{text}')"
    ])

def ask_ai(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        data = r.json()

        if "message" in data:
            return data["message"]["content"]
        if "response" in data:
            return data["response"]
    except:
        pass

    return "Sorry, I had trouble answering that."

def listen():
    print("🎤 Listening... Speak now and then STOP.")
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        device=MIC_INDEX
    ) as stream:

        while True:
            data, _ = stream.read(4000)
            if recognizer.AcceptWaveform(data.tobytes()):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    print("You said:", text)
                    return text

# ---------------- MAIN ----------------
speak("Hello. I am your offline AI assistant.")
speak("Speak clearly, then stop.")

while True:
    command = listen()

    if "stop" in command or "exit" in command:
        speak("Goodbye")
        break

    answer = ask_ai(command)
    speak(answer)
