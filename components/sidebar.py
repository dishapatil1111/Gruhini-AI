import streamlit as st
import uuid


MODES = [
    "Chat",
    "Interview Trainer",
    "Aptitude Test",
    "Study Tutor",
    "Career Roadmap",
]


def show_sidebar():

    # ==========================================
    # HEADER
    # ==========================================

    st.sidebar.title("🎓 Gruhini AI")

    # ==========================================
    # AI MODE
    # ==========================================

    selected_mode = st.sidebar.radio(
        "AI Mode",
        MODES,
        index=MODES.index(st.session_state.mode),
    )

    if selected_mode != st.session_state.mode:

        st.session_state.mode = selected_mode

        st.rerun()

    st.sidebar.divider()

    # ==========================================
    # MAIN NAVIGATION
    # ==========================================

    if st.sidebar.button(
        "🏠 Dashboard",
        use_container_width=True,
    ):

        st.session_state.page = "Dashboard"

        st.rerun()

    if st.sidebar.button(
        "💬 AI Chat",
        use_container_width=True,
    ):

        st.session_state.page = "AI Chat"

        st.rerun()

    if st.sidebar.button(
        "📚 Study Hub",
        use_container_width=True,
    ):

        st.session_state.page = "Study Hub"

        st.rerun()

    if st.sidebar.button(
        "💻 Coding Hub",
        use_container_width=True,
    ):

        st.session_state.page = "Coding Hub"

        st.rerun()

    if st.sidebar.button(
        "🎤 Interview Hub",
        use_container_width=True,
    ):

        st.session_state.page = "Interview Hub"

        st.rerun()
    if st.sidebar.button(
        "📜 Interview History",
        use_container_width=True,
    ):

        st.session_state.page = "Interview History"

        st.rerun()

    if st.sidebar.button(
        "💼 Career Hub",
        use_container_width=True,
    ):

        st.session_state.page = "Career Hub"

        st.rerun()

    # ==========================================
    # MEMORY
    # ==========================================

    if st.sidebar.button(
        "🧠 My Memory",
        use_container_width=True,
    ):

        st.session_state.page = "My Memory"

        st.rerun()

    st.sidebar.divider()

    # ==========================================
    # NEW CHAT
    # ==========================================

    if st.sidebar.button(
        "➕ New Chat",
        use_container_width=True,
    ):

        st.session_state.chat_id = uuid.uuid4().hex[:6]

        st.session_state.page = "AI Chat"

        st.rerun()

    # ==========================================
    # CONVERSATIONS
    # ==========================================

    st.sidebar.markdown("### 💬 Conversations")

    for key in st.session_state.sessions.keys():

        if st.sidebar.button(
            key,
            use_container_width=True,
        ):

            mode, cid = key.split("_", 1)

            st.session_state.mode = mode
            st.session_state.chat_id = cid
            st.session_state.page = "AI Chat"

            st.rerun()