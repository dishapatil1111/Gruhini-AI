# 🎓 Gruhini AI

## Offline AI Career & Academic Workspace for Engineering Students

### Learn. Build. Practice. Grow. Get Hired.

---

Gruhini AI is an **offline-first AI workspace** designed to help engineering students throughout their academic and career journey.

Instead of switching between multiple websites and AI tools, Gruhini brings studying, coding, interview preparation, career guidance, and intelligent AI assistance into one unified platform.

Built with privacy, personalization, and productivity in mind, Gruhini enables students to learn faster, build better projects, prepare confidently for interviews, and continuously grow throughout their engineering journey.

---
# 🚀 Why Gruhini?

Engineering students often rely on multiple platforms throughout their learning journey.

One website for studying.

Another for coding.

Another for interview preparation.

Another for resume improvement.

Another for career planning.

Switching between different tools interrupts focus, slows learning, and makes it difficult to track long-term progress.

**Gruhini AI brings these essential workflows together into one intelligent offline workspace.**

Instead of spending time searching for the right tool, students can focus on what truly matters:

- 📚 Learning concepts
- 💻 Building projects
- 🎤 Preparing for interviews
- 💼 Growing their careers
- 🚀 Becoming better engineers

Gruhini is designed to become a long-term AI companion that grows with students throughout their engineering journey.

---
# 💡 Design Philosophy

Gruhini AI was created with one simple belief:

> **Engineering students should spend less time switching between tools and more time learning, building, and growing.**

Today's students often rely on multiple platforms for studying, coding, interview preparation, resume improvement, and career planning. This fragmented workflow interrupts learning and makes long-term progress difficult to track.

Gruhini AI brings these experiences together into one unified offline workspace.

Every feature in Gruhini is designed around five core principles:

- 🔒 **Privacy First** — User data stays on the local machine whenever possible.
- 💻 **Offline First** — Core AI capabilities work without requiring cloud AI services.
- 🎓 **Student Focused** — Every feature is built specifically for engineering students.
- 🧠 **Continuous Growth** — Gruhini aims to remember progress and provide personalized guidance over time.
- 🚀 **Practical Learning** — The goal is not only to answer questions, but to help students build real skills and real projects.

Gruhini is designed to become a long-term AI companion that supports students from their first semester to their first job.

---
# 🌟 What Makes Gruhini AI Different?

Unlike general-purpose AI assistants, Gruhini AI is designed specifically for engineering students.

Instead of providing isolated AI tools, Gruhini combines learning, coding, interview preparation, career planning, and future personalization into one unified offline workspace.

### Gruhini focuses on the complete student journey:

📚 Learn concepts

↓

💻 Build projects

↓

🎤 Prepare for interviews

↓

💼 Develop your career

↓

🚀 Get hired

Rather than replacing existing learning platforms, Gruhini acts as an intelligent companion that helps students organize, improve, and accelerate their entire learning journey.

The long-term vision is to provide personalized AI guidance that remembers progress, understands goals, and continuously adapts to each student's growth.

---
# 🎯 Who is Gruhini AI For?

Gruhini AI is designed for learners who want one intelligent workspace instead of multiple disconnected tools.

It is especially useful for:

- 🎓 Engineering Students
- 💼 Internship & Placement Preparation
- 💻 Programming Beginners
- 📚 Self-Learners
- 🚀 Students building technical projects and portfolios

Whether you're preparing for your first coding assignment or your first job interview, Gruhini AI aims to support your complete learning journey.

---

# ✨ Key Features

| Module | Description |
|---------|-------------|
| 💬 **AI Assistant** | Ask questions, solve problems, brainstorm ideas, and receive intelligent AI assistance. |
| 📚 **Study Hub** | Learn difficult concepts, revise topics, generate explanations, and improve understanding. |
| 💻 **Coding Hub** | Explain code, debug errors, optimize programs, and generate code snippets with AI assistance. |
| 🎤 **Interview Hub** | Practice technical and HR interviews, receive feedback, and improve interview confidence. |
| 💼 **Career Hub** | Build career roadmaps, analyze skill gaps, review resumes, and optimize LinkedIn profiles. |
| 🧠 **Memory Engine** *(Upcoming)* | Personalized AI memory that remembers goals, learning progress, conversations, and career growth across sessions. |

---
# 🧠 AI Workflow

Gruhini AI processes user requests through a simple offline-first AI pipeline.

```text
                👤 User
                    │
                    ▼
          Streamlit User Interface
                    │
                    ▼
            Gruhini Backend
                    │
         Does the query require knowledge retrieval?
             │                    │
            No                   Yes
             │                    │
             ▼                    ▼
      Send prompt           Retrieve Context
      to Mistral                 │
                                 ▼
                     Sentence Transformers
                                 │
                                 ▼
                         FAISS Vector Search
                                 │
                                 ▼
                      Relevant Knowledge Chunks
                                 │
                                 ▼
                     Ollama (Local Mistral LLM)
                                 │
                                 ▼
                        AI Generated Response
                                 │
                                 ▼
                               User
```

### Workflow Overview

1. The user submits a question through the Streamlit interface.
2. Gruhini determines whether additional knowledge retrieval is required.
3. If needed, the query is converted into embeddings using Sentence Transformers.
4. FAISS retrieves the most relevant information from the local knowledge base.
5. The retrieved context is sent to the locally running Mistral model through Ollama.
6. Mistral generates a response using both the user's question and the retrieved context.
7. The final response is displayed to the user.

---

# 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| **Programming Language** | Python |
| **Frontend** | Streamlit |
| **AI Model** | Mistral (via Ollama) |
| **LLM Runtime** | Ollama |
| **Retrieval-Augmented Generation (RAG)** | FAISS + Sentence Transformers |
| **Knowledge Base** | Local Text Knowledge Base (`knowledge.txt`) |
| **Vector Search** | FAISS |
| **Embeddings** | Sentence Transformers |
| **Session Management** | JSON-based Local Storage |
| **Version Control** | Git & GitHub |

---
# 📂 Project Structure

```text
Gruhini-AI/
│
├── app.py                  # Main Streamlit application
├── assistant.py            # AI assistant logic
├── backend.py              # Backend communication
├── text_assistant.py       # Text-based AI helper
│
├── assets/                 # CSS and UI assets
├── components/             # Reusable UI components
├── config/                 # Application configuration
├── prompts/                # AI prompts for different modules
├── rag/                    # Retrieval-Augmented Generation
├── utils/                  # Utility functions
├── views/                  # Dashboard and application pages
│
├── memory.json             # Local memory (planned for future migration)
├── profile_memory.json     # User profile (planned for future migration)
├── interview_scores.json   # Interview history (planned for future migration)
│
└── README.md
```

---
