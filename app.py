import streamlit as st
import uuid
from backend import ask_gruhini

st.set_page_config(page_title="Gruhini AI", layout="wide")

MODES = [
    "Chat",
    "Interview Trainer",
    "Aptitude Test",
    "Study Tutor",
    "Career Roadmap"
]

# ================= SESSION =================
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "mode" not in st.session_state:
    st.session_state.mode = "Chat"

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())[:6]


def get_key(mode, chat_id):
    return f"{mode}_{chat_id}"


chat_key = get_key(st.session_state.mode, st.session_state.chat_id)

# create session if not exists
if chat_key not in st.session_state.sessions:
    st.session_state.sessions[chat_key] = {
        "messages": []
    }

session = st.session_state.sessions[chat_key]
chat = session["messages"]

# ================= SIDEBAR =================
st.sidebar.title("🧠 Control Panel")

selected_mode = st.sidebar.radio(
    "Mode",
    MODES,
    index=MODES.index(st.session_state.mode)
)

if selected_mode != st.session_state.mode:
    st.session_state.mode = selected_mode
    st.rerun()

if st.sidebar.button("➕ New Chat"):
    st.session_state.chat_id = str(uuid.uuid4())[:6]
    st.rerun()

# ================= HISTORY =================
st.sidebar.markdown("### 💬 Conversations")

for key in st.session_state.sessions.keys():
    if st.sidebar.button(key):
        mode, cid = key.split("_")
        st.session_state.mode = mode
        st.session_state.chat_id = cid
        st.rerun()

# ================= HEADER =================
st.title("🎓 Gruhini – Career & Academic AI")
st.caption(f"{st.session_state.mode} | Chat: {st.session_state.chat_id}")

# ================= DISPLAY =================
for msg in chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= INPUT =================
user_input = st.chat_input("Ask Gruhini...")

if user_input:

    # add user msg
    chat.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # 🔥 CALL NEW BACKEND (CORRECT)
    response = ask_gruhini(user_input, chat, st.session_state.mode)

    # add bot msg
    chat.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)