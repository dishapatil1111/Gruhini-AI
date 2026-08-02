import streamlit as st


def navigate(page):
    st.session_state.page = page
    st.rerun()


def show():

    # ==========================================================
    # HERO SECTION
    # ==========================================================

    st.markdown(
        """
        <div style="text-align:center;padding:25px 10px;">
            <h1>🎓 Gruhini AI</h1>
            <h3>Offline AI Career & Academic Mentor</h3>
            <p style="font-size:18px;color:#7f8c8d;">
                Learn • Build • Practice • Get Hired
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Gruhini guides engineering students from learning → building → interviewing → getting hired."
    )

    st.divider()

    # ==========================================================
    # TODAY'S MISSION
    # ==========================================================

    st.subheader("🎯 Today's Mission")

    mission = st.container()

    with mission:

        st.success(
            """
**Today's Goal**

📚 Learn one new concept.

⏱ Estimated Time: **30 Minutes**

⭐ Difficulty: **Beginner**

Focus on completing **one meaningful task** instead of trying to learn everything today.
"""
        )

        if st.button(
            "▶ Continue Learning",
            use_container_width=True
        ):
            navigate("Study Hub")

    st.divider()

    # ==========================================================
    # LEARNING JOURNEY
    # ==========================================================

    st.subheader("🚀 Your Engineering Journey")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("📚\n\nStudy")

    with col2:
        st.info("💻\n\nBuild")

    with col3:
        st.info("🎤\n\nInterview")

    with col4:
        st.info("💼\n\nCareer")

    st.caption(
        "Master concepts → Build projects → Practice interviews → Land your dream job."
    )

    st.divider()

    # ==========================================================
    # QUICK ACCESS
    # ==========================================================

    st.subheader("⚡ Quick Access")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📚 Study Hub",
            use_container_width=True
        ):
            navigate("Study Hub")

        if st.button(
            "💻 Coding Hub",
            use_container_width=True
        ):
            navigate("Coding Hub")

        if st.button(
            "🎤 Interview Hub",
            use_container_width=True
        ):
            navigate("Interview Hub")

    with col2:

        if st.button(
            "💼 Career Hub",
            use_container_width=True
        ):
            navigate("Career Hub")

        if st.button(
            "💬 AI Chat",
            use_container_width=True
        ):
            navigate("AI Chat")

        if st.button(
            "⚙ Settings",
            use_container_width=True
        ):
            st.info("Coming Soon 🚀")

    st.divider()

    # ==========================================================
    # GRUHINI TIP
    # ==========================================================

    st.subheader("💡 Gruhini Tip of the Day")

    st.info(
        """
**Projects get interviews.**

Certificates help, but recruiters are far more interested in seeing what you have actually built.

Aim to complete one meaningful project for every major skill you learn.
"""
    )

    st.divider()

    # ==========================================================
    # PRODUCT VISION
    # ==========================================================

    # ==========================================================
# PRODUCT JOURNEY
# ==========================================================

st.subheader("🌟 Your Journey with Gruhini")

st.info(
    """
📚 **Study Hub**

⬇

💻 **Coding Hub**

⬇

🎤 **Interview Hub**

⬇

💼 **Career Hub**

⬇

🚀 **Get Hired**
"""
)