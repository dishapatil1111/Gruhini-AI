import streamlit as st
import uuid
from backend import ask_gruhini

st.set_page_config(
    page_title="Gruhini AI",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# MODES
# ==========================================

MODES = [
    "Chat",
    "Interview Trainer",
    "Aptitude Test",
    "Study Tutor",
    "Career Roadmap"
]

# ==========================================
# SESSION
# ==========================================

if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "mode" not in st.session_state:
    st.session_state.mode = "Chat"

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())[:6]


def get_key(mode, chat_id):
    return f"{mode}_{chat_id}"


chat_key = get_key(
    st.session_state.mode,
    st.session_state.chat_id
)

if chat_key not in st.session_state.sessions:
    st.session_state.sessions[chat_key] = {
        "messages": []
    }

chat = st.session_state.sessions[chat_key]["messages"]

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🎓 Gruhini AI")

selected_mode = st.sidebar.radio(
    "AI Mode",
    MODES,
    index=MODES.index(st.session_state.mode)
)

if selected_mode != st.session_state.mode:
    st.session_state.mode = selected_mode
    st.rerun()

st.sidebar.divider()

if st.sidebar.button("🏠 Dashboard", use_container_width=True):
    st.session_state.page = "Dashboard"
    st.rerun()

if st.sidebar.button("💬 AI Chat", use_container_width=True):
    st.session_state.page = "AI Chat"
    st.rerun()

st.sidebar.divider()

if st.sidebar.button("➕ New Chat", use_container_width=True):
    st.session_state.chat_id = str(uuid.uuid4())[:6]
    st.rerun()

st.sidebar.markdown("### 💬 Conversations")

for key in st.session_state.sessions.keys():

    if st.sidebar.button(key, use_container_width=True):
        mode, cid = key.split("_")

        st.session_state.mode = mode
        st.session_state.chat_id = cid
        st.session_state.page = "AI Chat"

        st.rerun()

# ==========================================
# DASHBOARD
# ==========================================

if st.session_state.page == "Dashboard":

    st.markdown(
        """
        <div style="text-align:center;padding:30px;">
            <h1>🎓 Gruhini AI</h1>
            <h3>AI Platform for Engineering Students</h3>
            <p style="font-size:18px;color:gray;">
                Learn • Build • Practice • Get Hired
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 👋 Welcome")

    st.write(
        "Choose the workspace you want to use."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💬 AI Chat",
            use_container_width=True
        ):
            st.session_state.page = "AI Chat"
            st.rerun()

        st.caption("General AI Assistant")

        if st.button(
            "📚 Study Hub",
            use_container_width=True
        ):
            st.info("Coming Soon 🚀")

        st.caption("Learn concepts faster")

        if st.button(
            "💼 Career Hub",
            use_container_width=True
        ):
            st.info("Coming Soon 🚀")

        st.caption("Resume • LinkedIn • Career")

    with col2:

        if st.button(
            "💻 Coding Hub",
            use_container_width=True
        ):
            st.info("Coming Soon 🚀")

        st.caption("Debug • Explain • Build")

        if st.button(
            "🎤 Interview Hub",
            use_container_width=True
        ):
            st.info("Coming Soon 🚀")

        st.caption("Mock Interviews")

        if st.button(
            "⚙ Settings",
            use_container_width=True
        ):
            st.info("Coming Soon 🚀")

        st.caption("AI Configuration")

# ==========================================
# AI CHAT
# ==========================================

elif st.session_state.page == "AI Chat":

    st.title("💬 Gruhini AI Chat")

    st.caption(
        f"Mode: {st.session_state.mode} | Chat: {st.session_state.chat_id}"
    )

    for msg in chat:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask Gruhini...")

    if user_input:

        chat.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        response = ask_gruhini(
            user_input,
            chat,
            st.session_state.mode
        )

        chat.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message("assistant"):
            st.markdown(response)