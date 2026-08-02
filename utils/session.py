import streamlit as st
import uuid


def initialize_session():

    # -----------------------------
    # Chat Sessions
    # -----------------------------
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}

    if "mode" not in st.session_state:
        st.session_state.mode = "Chat"

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    if "chat_id" not in st.session_state:
        st.session_state.chat_id = str(uuid.uuid4())[:6]

    chat_key = f"{st.session_state.mode}_{st.session_state.chat_id}"

    if chat_key not in st.session_state.sessions:
        st.session_state.sessions[chat_key] = {
            "messages": []
        }

    # -----------------------------
    # Interview Hub State
    # -----------------------------
    if "mock_question" not in st.session_state:
        st.session_state.mock_question = ""

    if "mock_answer" not in st.session_state:
        st.session_state.mock_answer = ""

    if "mock_feedback" not in st.session_state:
        st.session_state.mock_feedback = ""

    if "mock_started" not in st.session_state:
        st.session_state.mock_started = False

    return chat_key