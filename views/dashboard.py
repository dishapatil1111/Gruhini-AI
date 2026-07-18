import streamlit as st


def show():

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

    st.write("Choose the workspace you want to use.")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("💬 AI Chat", use_container_width=True):
            st.session_state.page = "AI Chat"
            st.rerun()

        st.caption("General AI Assistant")

        if st.button("📚 Study Hub", use_container_width=True):
            st.session_state.page = "Study Hub"
            st.rerun()

        st.caption("Learn concepts faster")

        if st.button("💼 Career Hub", use_container_width=True):
            st.session_state.page = "Career Hub"
            st.rerun()

        st.caption("Resume • LinkedIn • Career")

    with col2:

        if st.button("💻 Coding Hub", use_container_width=True):
            st.session_state.page = "Coding Hub"
            st.rerun()

        st.caption("Debug • Explain • Build")

        if st.button("🎤 Interview Hub", use_container_width=True):
            st.session_state.page = "Interview Hub"
            st.rerun()

        st.caption("Mock Interviews")

        if st.button("⚙ Settings", use_container_width=True):
            st.info("Coming Soon 🚀")

        st.caption("AI Configuration")