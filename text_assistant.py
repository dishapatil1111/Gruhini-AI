import requests
import json
import os
import random

# ---------------- CONFIG ----------------
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "phi3"
ASSISTANT_NAME = "Gruhini"
TIMEOUT_SECONDS = 180
MEMORY_FILE = "memory.json"
# ----------------------------------------

# Load memory
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {}

# Default mode
memory.setdefault("mode", "normal")

def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

print(f"🤖 {ASSISTANT_NAME} — Hybrid AI Assistant")
print("Modes: normal | interview | aptitude")
print("Commands:")
print("  mode interview | mode aptitude | mode normal")
print("  exit\n")

# Interview questions
INTERVIEW_QUESTIONS = [
    "Tell me about yourself.",
    "Explain a project you are proud of.",
    "What are your strengths and weaknesses?",
    "How do you handle failure?",
    "Why should we hire you?"
]

# Aptitude questions
APTITUDE_QUESTIONS = [
    {
        "q": "If a train travels 60 km in 1 hour, how far will it travel in 30 minutes?",
        "a": "30 km"
    },
    {
        "q": "What comes next in the series: 2, 4, 8, 16, ?",
        "a": "32"
    },
    {
        "q": "If 5 workers take 10 days to finish a job, how long will 10 workers take?",
        "a": "5 days"
    }
]

# -------- PERSONALITY PROMPT --------
def personality_prompt():
    return f"""
You are {ASSISTANT_NAME}, an intelligent, friendly, and supportive AI assistant.

PERSONALITY:
- Sound calm, confident, and human-like.
- Be encouraging and respectful, especially to students.
- Explain concepts clearly using simple language first.
- Use step-by-step explanations when helpful.
- Avoid unnecessary jargon unless the user asks for it.
- If a question is unclear, gently ask for clarification.
- Be concise by default, but expand when the user asks for detail.
- Think logically before answering.

ROLE ADAPTATION:
- In normal mode: behave like a knowledgeable mentor (similar to ChatGPT).
- In interview mode: behave like a professional interviewer.
- In aptitude mode: behave like a trainer guiding problem-solving.

USER CONTEXT:
Here is what you know about the user so far:
{json.dumps(memory, indent=2)}

Always use this context naturally in your responses.
"""

# ---------------- MAIN LOOP ----------------
while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "quit", "stop"]:
        print(f"{ASSISTANT_NAME}: Goodbye 👋")
        break

    # -------- MODE SWITCHING --------
    if user_input.lower().startswith("mode"):
        mode = user_input.lower().replace("mode", "").strip()
        if mode in ["normal", "interview", "aptitude"]:
            memory["mode"] = mode
            save_memory()
            print(f"{ASSISTANT_NAME}: Switched to {mode} mode ✅\n")
        else:
            print(f"{ASSISTANT_NAME}: Unknown mode ❌\n")
        continue

    # -------- MEMORY CAPTURE --------
    if "my name is" in user_input.lower():
        name = user_input.split("my name is")[-1].strip()
        memory["user_name"] = name
        save_memory()
        print(f"{ASSISTANT_NAME}: Nice to meet you, {name} 😊\n")
        continue

    if "remember that" in user_input.lower():
        note = user_input.split("remember that")[-1].strip()
        memory.setdefault("notes", []).append(note)
        save_memory()
        print(f"{ASSISTANT_NAME}: I’ll remember that 👍\n")
        continue

    # -------- MODE LOGIC --------
    mode = memory.get("mode", "normal")

    # 🎤 INTERVIEW MODE
    if mode == "interview":
        question = random.choice(INTERVIEW_QUESTIONS)
        print(f"\n{ASSISTANT_NAME} (Interviewer): {question}\n")
        continue

    # 🧮 APTITUDE MODE
    if mode == "aptitude":
        qa = random.choice(APTITUDE_QUESTIONS)
        print(f"\n{ASSISTANT_NAME} (Aptitude): {qa['q']}")
        input("Your answer: ")
        print(f"{ASSISTANT_NAME}: Correct answer is {qa['a']}\n")
        continue

    # 💬 NORMAL MODE (LLM)
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": personality_prompt()
            },
            {"role": "user", "content": user_input}
        ],
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=TIMEOUT_SECONDS
        )
        data = response.json()

        if "message" in data:
            answer = data["message"]["content"]
        elif "response" in data:
            answer = data["response"]
        else:
            answer = "Sorry, I couldn't generate a response."

        print(f"\n{ASSISTANT_NAME}: {answer}\n")

    except Exception as e:
        print(f"{ASSISTANT_NAME}: I am thinking… please try again.")
        print("Details:", e)
