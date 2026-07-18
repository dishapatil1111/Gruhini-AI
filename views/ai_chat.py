import streamlit as st
from backend import ask_gruhini


def show():

    chat_key = f"{st.session_state.mode}_{st.session_state.chat_id}"

    chat = st.session_state.sessions[chat_key]["messages"]

    st.title("💬 Gruhini AI Chat")

    st.caption(
        f"Mode: {st.session_state.mode} | Chat: {st.session_state.chat_id}"
    )

    # Show previous messages
    for msg in chat:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
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