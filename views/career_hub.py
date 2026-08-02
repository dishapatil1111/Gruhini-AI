import streamlit as st
from backend import call_llm

from prompts.career import (
    ROADMAP_PROMPT,
    SKILL_GAP_PROMPT,
    RESUME_REVIEW_PROMPT,
    LINKEDIN_PROMPT,
)


def show():

    st.title("💼 Career Hub")

    st.write(
        "Plan your career, improve your resume, optimize LinkedIn, and identify skill gaps with Gruhini AI."
    )

    # ==========================================
    # FEATURE SELECTION
    # ==========================================

    feature = st.radio(
        "Choose a Career Tool",
        [
            "🛣 Career Roadmap",
            "🎯 Skill Gap Analysis",
            "📄 Resume Review",
            "🌐 LinkedIn Optimizer"
        ],
        horizontal=True
    )

    st.divider()

    # ==========================================
    # CAREER ROADMAP
    # ==========================================

    if feature == "🛣 Career Roadmap":

        role = st.selectbox(
            "Target Role",
            [
                "Software Engineer",
                "Data Scientist",
                "Data Analyst",
                "Machine Learning Engineer",
                "Backend Developer",
                "Frontend Developer",
                "DevOps Engineer",
                "Cybersecurity Engineer",
                "Custom"
            ]
        )

        if role == "Custom":
            role = st.text_input(
                "Enter Target Role"
            )

        level = st.selectbox(
            "Current Level",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

        duration = st.selectbox(
            "Learning Duration",
            [
                "3 Months",
                "6 Months",
                "12 Months"
            ]
        )

        if st.button(
            "🚀 Generate Career Roadmap",
            use_container_width=True
        ):

            if not role.strip():
                st.warning("Please enter a target role.")
                st.stop()

            prompt = ROADMAP_PROMPT.format(
                role=role,
                level=level,
                duration=duration
            )

            with st.spinner("Generating roadmap..."):
                response = call_llm(prompt)

            st.divider()
            st.subheader("🤖 Gruhini AI")
            st.markdown(response)

    # ==========================================
    # SKILL GAP
    # ==========================================

    elif feature == "🎯 Skill Gap Analysis":

        role = st.text_input(
            "Target Role",
            placeholder="Example: Machine Learning Engineer"
        )

        skills = st.text_area(
            "Current Skills",
            height=180,
            placeholder="Python, SQL, Pandas..."
        )

        if st.button(
            "🎯 Analyze Skill Gap",
            use_container_width=True
        ):

            if not role.strip() or not skills.strip():
                st.warning("Please enter both target role and current skills.")
                st.stop()

            prompt = SKILL_GAP_PROMPT.format(
                role=role,
                skills=skills
            )

            with st.spinner("Analyzing skills..."):
                response = call_llm(prompt)

            st.divider()
            st.subheader("🤖 Gruhini AI")
            st.markdown(response)

    # ==========================================
    # RESUME REVIEW
    # ==========================================

    elif feature == "📄 Resume Review":

        resume = st.text_area(
            "Paste Resume",
            height=350,
            placeholder="Paste your resume here..."
        )

        if st.button(
            "📄 Review Resume",
            use_container_width=True
        ):

            if not resume.strip():
                st.warning("Please paste your resume.")
                st.stop()

            prompt = RESUME_REVIEW_PROMPT.format(
                resume=resume
            )

            with st.spinner("Reviewing resume..."):
                response = call_llm(prompt)

            st.divider()
            st.subheader("🤖 Gruhini AI")
            st.markdown(response)

    # ==========================================
    # LINKEDIN
    # ==========================================

    else:

        headline = st.text_input(
            "Headline"
        )

        about = st.text_area(
            "About Section",
            height=250
        )

        if st.button(
            "🌐 Optimize LinkedIn",
            use_container_width=True
        ):

            if not headline.strip() or not about.strip():
                st.warning("Please enter both headline and About section.")
                st.stop()

            prompt = LINKEDIN_PROMPT.format(
                headline=headline,
                about=about
            )

            with st.spinner("Optimizing profile..."):
                response = call_llm(prompt)

            st.divider()
            st.subheader("🤖 Gruhini AI")
            st.markdown(response)