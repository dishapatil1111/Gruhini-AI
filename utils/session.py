import streamlit as st
import uuid


def initialize_session():

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

    return chat_key