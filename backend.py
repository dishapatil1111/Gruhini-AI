import re
import requests

from config.settings import OLLAMA_URL, DEFAULT_MODEL
from rag.retriever import retrieve

from utils.memory_manager import (
    load_profile,
    load_career,
    load_skills,
)

from utils.memory_extractor import (
    extract_memory,
    save_extracted_memory,
)


# ==================================================
# SESSION
# ==================================================

SESSION = {
    "interview": {
        "active": False,
        "domain": None,
        "question": None,
        "waiting": False,
        "count": 0,
    },
    "aptitude": {
        "question": None,
        "waiting": False,
    },
    "study": {
        "topic": None,
    },
}


# ==================================================
# LLM
# ==================================================

def call_llm(prompt):
    """
    Send a prompt to the local Ollama model.
    """

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

    except requests.exceptions.ConnectionError:
        return (
            "⚠️ I couldn't connect to Ollama. "
            "Please make sure Ollama is running."
        )

    except requests.exceptions.Timeout:
        return (
            "⚠️ The local AI model took too long to respond. "
            "Please try again."
        )

    except Exception as e:
        return f"⚠️ Error:\n{e}"


# ==================================================
# VALIDATION
# ==================================================

def is_valid(text):
    """
    Basic validation for user input.
    """

    text = text.strip()

    return (
        len(text) > 3
        and text.lower() not in [
            "hi",
            "hello",
            "hey",
            "ok",
        ]
    )


def is_greeting(text):
    """
    Detect simple greetings.
    """

    return text.strip().lower() in [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    ]


# ==================================================
# MEMORY
# ==================================================

def capture_memory(user_input):
    """
    Detect and save explicit personal information
    from the user's message.

    Only information explicitly detected by the
    memory extractor is saved.
    """

    memory = extract_memory(user_input)

    has_memory = any(
        [
            bool(memory.get("profile")),
            bool(memory.get("career")),
            bool(memory.get("skills")),
        ]
    )

    if has_memory:
        save_extracted_memory(memory)

    return memory


def get_memory_context():
    """
    Load saved local memory and format it for the LLM.
    """

    profile = load_profile()
    career = load_career()
    skills = load_skills()

    return f"""
USER PROFILE:
{profile}

CAREER GOALS:
{career}

SKILLS:
{skills}
"""


# ==================================================
# CONVERSATION HISTORY
# ==================================================

def get_history_context(history, max_messages=6):
    """
    Convert recent chat history into a compact prompt.

    Only the most recent messages are included so the
    prompt does not grow indefinitely.
    """

    if not history:
        return ""

    recent_messages = history[-max_messages:]

    lines = []

    for message in recent_messages:

        role = message.get("role", "").strip()
        content = message.get("content", "").strip()

        if not content:
            continue

        if role == "user":
            label = "User"

        elif role == "assistant":
            label = "Assistant"

        else:
            label = role.title() or "Message"

        lines.append(
            f"{label}: {content}"
        )

    if not lines:
        return ""

    return "\n".join(lines)


# ==================================================
# MEMORY QUERY DETECTION
# ==================================================

def answer_memory_query(user_input):
    """
    Answer questions about saved user memory directly
    from local JSON storage.

    The LLM is NOT used for these questions.

    This prevents hallucination of personal information.
    """

    text = user_input.strip().lower()

    profile = load_profile()
    career = load_career()
    skills = load_skills()

    # ==================================================
    # TARGET CAREER / ROLE
    # ==================================================

    if (
        "what career" in text
        or "what role" in text
        or "career am i preparing" in text
        or "role am i preparing" in text
        or "what am i preparing for" in text
    ):

        role = career.get(
            "target_role",
            "",
        ).strip()

        if role:
            return (
                f"You are currently preparing "
                f"for a {role} role."
            )

        return (
            "I don't currently have a target "
            "career or role saved."
        )

    # ==================================================
    # CAREER GOAL
    # ==================================================

    if (
        "career goal" in text
        or "career goals" in text
        or "what is my goal" in text
        or "what are my goals" in text
    ):

        goal = career.get(
            "career_goal",
            "",
        ).strip()

        if goal:
            return (
                f"Your saved career goal is: {goal}"
            )

        return (
            "I don't currently have a career goal saved."
        )

    # ==================================================
    # TARGET INDUSTRY
    # ==================================================

    if (
        "target industry" in text
        or "which industry" in text
        or "what industry" in text
    ):

        industry = career.get(
            "target_industry",
            "",
        ).strip()

        if industry:
            return (
                f"Your saved target industry is "
                f"{industry}."
            )

        return (
            "I don't currently have a target industry saved."
        )

    # ==================================================
    # PROGRAMMING LANGUAGES
    # ==================================================

    if (
        "what programming languages" in text
        or "which programming languages" in text
        or "what languages do i know" in text
        or "which languages do i know" in text
    ):

        languages = skills.get(
            "programming_languages",
            [],
        )

        if languages:
            return (
                "According to your saved memory, "
                f"you know: {', '.join(languages)}."
            )

        return (
            "I don't currently have any programming "
            "languages saved."
        )

    # ==================================================
    # ALL SKILLS
    # ==================================================

    if (
        "what skills do i have" in text
        or "what skills do i currently have" in text
        or "which skills do i have" in text
        or "what are my skills" in text
        or "show my skills" in text
    ):

        sections = []

        categories = {
            "Programming Languages": "programming_languages",
            "Frameworks": "frameworks",
            "Tools": "tools",
            "AI/ML": "ai_ml",
            "Data Skills": "data_skills",
        }

        for label, key in categories.items():

            values = skills.get(key, [])

            if values:

                sections.append(
                    f"- {label}: {', '.join(values)}"
                )

        if not sections:
            return (
                "I don't currently have any skills saved."
            )

        return (
            "According to your saved memory:\n\n"
            + "\n".join(sections)
        )

    # ==================================================
    # PROFILE
    # ==================================================

    if (
        "what is my name" in text
        or "what's my name" in text
        or "do you know my name" in text
    ):

        name = profile.get(
            "name",
            "",
        ).strip()

        if name:
            return f"Your saved name is {name}."

        return (
            "I don't currently have your name saved."
        )

    # ==================================================
    # DEGREE
    # ==================================================

    if (
        "what degree am i doing" in text
        or "what degree do i have" in text
        or "what am i studying" in text
    ):

        degree = profile.get(
            "degree",
            "",
        ).strip()

        if degree:
            return (
                f"Your saved degree is {degree}."
            )

        return (
            "I don't currently have your degree saved."
        )

    # ==================================================
    # SPECIFIC SKILL CHECK
    # ==================================================

    skill_match = re.search(
        r"\bdo i know\s+(.+?)\??$",
        text,
        re.IGNORECASE,
    )

    if skill_match:

        requested_skill = (
            skill_match.group(1)
            .strip()
            .lower()
        )

        all_saved_skills = []

        for values in skills.values():

            if isinstance(values, list):
                all_saved_skills.extend(values)

        normalized_saved = [
            skill.strip().lower()
            for skill in all_saved_skills
        ]

        if requested_skill in normalized_saved:

            return (
                f"Yes. {requested_skill.title()} "
                "is currently in your saved skills."
            )

        return (
            f"No. {requested_skill.title()} "
            "is not currently in your saved skills."
        )

    # ==================================================
    # NO MEMORY QUERY
    # ==================================================

    return None


# ==================================================
# RAG
# ==================================================

def get_context(query):
    """
    Retrieve relevant knowledge from the local RAG index.

    Short queries skip retrieval.
    Retrieval failures never crash the application.
    """

    if len(query.strip()) < 10:
        return ""

    try:

        results = retrieve(query)

        if not results:
            return ""

        return "\n".join(results)

    except Exception:
        return ""


# ==================================================
# RAG DECISION
# ==================================================

def should_use_rag(user_input):
    """
    Decide whether a normal Chat question is likely
    to benefit from the local knowledge base.

    This avoids unnecessary retrieval for greetings,
    simple conversational messages, and memory queries.
    """

    text = user_input.strip().lower()

    if not text:
        return False

    if is_greeting(text):
        return False

    if len(text.split()) <= 2:
        return False

    knowledge_patterns = [
        r"\bwhat is\b",
        r"\bwhat are\b",
        r"\bexplain\b",
        r"\bdefine\b",
        r"\bhow does\b",
        r"\bhow do\b",
        r"\bwhy does\b",
        r"\bwhy is\b",
        r"\bdifference between\b",
        r"\bcompare\b",
        r"\bexample of\b",
        r"\bexamples of\b",
        r"\bhow to\b",
        r"\btutorial\b",
        r"\bguide\b",
        r"\blearn\b",
    ]

    for pattern in knowledge_patterns:

        if re.search(pattern, text):
            return True

    return False


# ==================================================
# CHAT PROMPT
# ==================================================

def build_chat_prompt(
    user_input,
    memory_context,
    rag_context,
    history_context,
):
    """
    Build the main Chat prompt.
    """

    return f"""
You are Gruhini, an AI assistant designed for
engineering students.

Your goal is to be useful, accurate, clear, and
student-friendly.

IMPORTANT MEMORY RULES:

1. Use saved user memory only when it is relevant.

2. Never invent personal information.

3. Never assume information that is not explicitly
   present in USER MEMORY.

4. Do not turn general knowledge into personal
   information.

5. If the user asks about their saved information,
   use only USER MEMORY.

6. If a memory field is empty, do not guess its value.

7. Do not introduce unrelated personal details.

8. If the user asks a normal knowledge question,
   answer it normally.

9. If relevant knowledge is provided below, use it
   to improve accuracy.

10. If the available knowledge is insufficient,
    clearly say so rather than inventing facts.

11. Keep the answer focused on the user's question.

CONVERSATION HISTORY:
{history_context}

USER MEMORY:
{memory_context}

RELEVANT KNOWLEDGE:
{rag_context}

CURRENT USER MESSAGE:
{user_input}

ASSISTANT:
"""


# ==================================================
# MAIN
# ==================================================

def ask_gruhini(user_input, history, mode):

    user_input = user_input.strip()

    # ==================================================
    # EMPTY INPUT
    # ==================================================

    if not user_input:
        return "Please enter a question or message."

    # ==================================================
    # CHAT
    # ==================================================

    if mode == "Chat":

        # ----------------------------------------------
        # Greeting
        # ----------------------------------------------

        if is_greeting(user_input):

            return (
                "Hello! 👋 How can I help you today?"
            )

        # ----------------------------------------------
        # Capture explicit memory
        # ----------------------------------------------

        capture_memory(user_input)

        # ----------------------------------------------
        # Deterministic memory query
        # ----------------------------------------------

        memory_answer = answer_memory_query(
            user_input
        )

        if memory_answer:

            return memory_answer

        # ----------------------------------------------
        # Very short / unclear input
        # ----------------------------------------------

        if len(user_input.split()) <= 2:

            return (
                "Can you please clarify your "
                "question a bit more?"
            )

        # ----------------------------------------------
        # Memory context
        # ----------------------------------------------

        memory_context = get_memory_context()

        # ----------------------------------------------
        # Conversation history
        # ----------------------------------------------

        history_context = get_history_context(
            history
        )

        # ----------------------------------------------
        # RAG
        # ----------------------------------------------

        rag_context = ""

        if should_use_rag(user_input):

            rag_context = get_context(
                user_input
            )

        # ----------------------------------------------
        # Prompt
        # ----------------------------------------------

        prompt = build_chat_prompt(
            user_input=user_input,
            memory_context=memory_context,
            rag_context=rag_context,
            history_context=history_context,
        )

        return call_llm(prompt)

    # ==================================================
    # INTERVIEW TRAINER
    # ==================================================

    elif mode == "Interview Trainer":

        interview = SESSION["interview"]

        # ----------------------------------------------
        # Start
        # ----------------------------------------------

        if not interview["active"]:

            interview["active"] = True
            interview["domain"] = None
            interview["question"] = None
            interview["waiting"] = False
            interview["count"] = 0

            return (
                "Which domain are you preparing for?"
            )

        # ----------------------------------------------
        # Domain
        # ----------------------------------------------

        if interview["domain"] is None:

            if not is_valid(user_input):

                return (
                    "Enter a valid domain "
                    "(e.g., data science, web development)"
                )

            interview["domain"] = user_input
            interview["count"] = 1

            question = call_llm(
                f"""
Ask ONE EASY interview question about:

{user_input}

Rules:
- Ask exactly one question.
- Do not provide the answer.
- Do not explain.
"""
            )

            interview["question"] = question
            interview["waiting"] = True

            return (
                f"Question 1:\n{question}"
            )

        # ----------------------------------------------
        # Evaluate answer
        # ----------------------------------------------

        if interview["waiting"]:

            feedback = call_llm(
                f"""
Evaluate this interview answer.

Domain:
{interview["domain"]}

Question:
{interview["question"]}

Candidate Answer:
{user_input}

STRICT FORMAT:

Rating: Good/Average/Poor
Feedback: short and useful
Correct Answer: short
"""
            )

            interview["count"] += 1

            question = call_llm(
                f"""
Ask ONE MEDIUM-level interview question about:

{interview["domain"]}

Rules:
- Ask exactly one question.
- Do not provide the answer.
- Do not explain.
"""
            )

            interview["question"] = question
            interview["waiting"] = True

            return (
                f"{feedback}\n\n"
                f"Question {interview['count']}:\n"
                f"{question}"
            )

    # ==================================================
    # APTITUDE TEST
    # ==================================================

    elif mode == "Aptitude Test":

        aptitude = SESSION["aptitude"]

        # ----------------------------------------------
        # Generate question
        # ----------------------------------------------

        if not aptitude["waiting"]:

            question = call_llm(
                """
Generate ONE aptitude multiple-choice question.

STRICT FORMAT ONLY:

Question: ...
A) ...
B) ...
C) ...
D) ...

Rules:
- Do not include the correct answer.
- Do not include explanation.
"""
            )

            aptitude["question"] = question
            aptitude["waiting"] = True

            return question

        # ----------------------------------------------
        # Evaluate answer
        # ----------------------------------------------

        result = call_llm(
            f"""
Evaluate the user's answer.

Question:
{aptitude["question"]}

User Answer:
{user_input}

STRICT FORMAT:

Correct Answer: <A/B/C/D>
Explanation: short
"""
        )

        aptitude["waiting"] = False

        return result

    # ==================================================
    # STUDY TUTOR
    # ==================================================

    elif mode == "Study Tutor":

        study = SESSION["study"]

        # ----------------------------------------------
        # Topic
        # ----------------------------------------------

        if study["topic"] is None:

            if not is_valid(user_input):

                return "Enter a proper topic 🙂"

            study["topic"] = user_input

        # ----------------------------------------------
        # Study prompt
        # ----------------------------------------------

        prompt = f"""
You are Gruhini's Study Tutor.

Teach ONLY this topic:

{study["topic"]}

If the student asks for "more", continue the same
topic instead of starting a new topic.

Use a simple engineering-student-friendly explanation.

Format:

Title

Step 1

Step 2

Step 3

Example

Key Takeaway
"""

        return call_llm(prompt)

    # ==================================================
    # CAREER ROADMAP
    # ==================================================

    elif mode == "Career Roadmap":

        if not is_valid(user_input):

            return (
                "Enter a valid career field 🙂"
            )

        # ----------------------------------------------
        # Include relevant saved career memory
        # ----------------------------------------------

        career = load_career()
        skills = load_skills()

        prompt = f"""
You are Gruhini's Career Mentor.

Create a practical career roadmap.

Requested Field:
{user_input}

Saved Career Information:
{career}

Current Saved Skills:
{skills}

Use the saved information only when relevant.

Include:

1. Current Position
2. Skills to Learn
3. Tools to Learn
4. Projects to Build
5. Interview Preparation
6. Suggested Timeline
7. Beginner → Intermediate → Advanced progression

Do not invent personal information.
"""

        return call_llm(prompt)

    # ==================================================
    # INVALID MODE
    # ==================================================

    return "Invalid mode"