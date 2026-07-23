import requests
from config.settings import OLLAMA_URL, DEFAULT_MODEL
from rag.retriever import retrieve



# ================= SESSION =================
SESSION = {
    "interview": {
        "active": False,
        "domain": None,
        "question": None,
        "waiting": False,
        "count": 0
    },
    "aptitude": {
        "question": None,
        "waiting": False
    },
    "study": {
        "topic": None
    }
}

# ================= LLM =================
def call_llm(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": DEFAULT_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        if "response" in data:
            return data["response"].strip()

        return f"Unexpected response:\n{data}"

    except Exception as e:
        return f"⚠️ Error:\n{e}"

# ================= VALIDATION =================
def is_valid(text):
    return len(text.strip()) > 3 and text.lower() not in ["hi", "hello", "hey", "ok"]

def is_greeting(text):
    return text.lower() in ["hi", "hello", "hey"]

# ================= RAG =================
def get_context(query):
    if len(query.strip()) < 10:
        return ""
    try:
        return "\n".join(retrieve(query))
    except:
        return ""

# ================= MAIN =================
def ask_gruhini(user_input, history, mode):

    user_input = user_input.strip()

    # ================= CHAT =================
    if mode == "Chat":

        if is_greeting(user_input):
            return "Hello! How can I help you today?"

        # unclear query detection
        if len(user_input.split()) <= 2:
            return "Can you please clarify your question a bit more?"

        context = get_context(user_input)

        prompt = f"""
Answer clearly and correctly.

If unsure → say you need clarification.

Context:
{context}

User: {user_input}
Assistant:
"""
        return call_llm(prompt)

    # ================= INTERVIEW =================
    elif mode == "Interview Trainer":

        interview = SESSION["interview"]

        if not interview["active"]:
            interview["active"] = True
            return "Which domain are you preparing for?"

        if interview["domain"] is None:
            if not is_valid(user_input):
                return "Enter a valid domain (e.g., data science, web dev)"

            interview["domain"] = user_input
            interview["count"] = 1

            q = call_llm(f"""
Ask ONE EASY interview question about {user_input}.
Do NOT explain.
""")

            interview["question"] = q
            interview["waiting"] = True

            return f"Question 1:\n{q}"

        if interview["waiting"]:
            feedback = call_llm(f"""
Evaluate answer.

Question: {interview["question"]}
Answer: {user_input}

STRICT FORMAT:
Rating: Good/Average/Poor
Feedback: short
Correct Answer: short
""")

            interview["count"] += 1

            q = call_llm(f"""
Ask ONE MEDIUM level interview question about {interview['domain']}.
Do NOT explain.
""")

            interview["question"] = q

            return f"{feedback}\n\nQuestion {interview['count']}:\n{q}"

    # ================= APTITUDE =================
    elif mode == "Aptitude Test":

        aptitude = SESSION["aptitude"]

        if not aptitude["waiting"]:

            q = call_llm("""
Generate ONE aptitude MCQ.

STRICT FORMAT ONLY:

Question: ...
A) ...
B) ...
C) ...
D) ...

DO NOT include answer.
""")

            aptitude["question"] = q
            aptitude["waiting"] = True

            return q

        else:
            result = call_llm(f"""
Question:
{aptitude["question"]}

User Answer: {user_input}

STRICT FORMAT:
Correct Answer: <A/B/C/D>
Explanation: short
""")

            aptitude["waiting"] = False
            return result

    # ================= STUDY =================
    elif mode == "Study Tutor":

        study = SESSION["study"]

        if study["topic"] is None:

            if not is_valid(user_input):
                return "Enter a proper topic 🙂"

            study["topic"] = user_input

        prompt = f"""
Teach ONLY this topic: {study["topic"]}

If user says "more" → continue same topic.

Format:
Title
Step 1
Step 2
Step 3
Example
"""
        return call_llm(prompt)

    # ================= CAREER =================
    elif mode == "Career Roadmap":

        if not is_valid(user_input):
            return "Enter a valid career field 🙂"

        prompt = f"""
Create a clean roadmap.

Field: {user_input}

Include:
- Skills
- Tools
- Projects
- Timeline (beginner → advanced)
"""
        return call_llm(prompt)

    return "Invalid mode"