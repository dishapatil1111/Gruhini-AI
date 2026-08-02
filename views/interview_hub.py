import streamlit as st
from backend import call_llm

from prompts.interview import (
    GENERATE_QUESTIONS_PROMPT,
    EVALUATE_ANSWER_PROMPT,
    MOCK_INTERVIEW_PROMPT,
)


def show():

    st.title("🎤 Interview Hub")

    st.write(
        "Practice interviews, generate questions, and improve your interview skills with Gruhini AI."
    )

    role = st.selectbox(
        "Job Role",
        [
            "Software Engineer",
            "Data Scientist",
            "Data Analyst",
            "Machine Learning Engineer",
            "Frontend Developer",
            "Backend Developer",
            "DevOps Engineer",
            "Cybersecurity Engineer",
            "Custom"
        ]
    )

    if role == "Custom":
        role = st.text_input(
            "Enter Job Role",
            placeholder="Example: AI Research Engineer"
        )

    interview_type = st.selectbox(
        "Interview Type",
        [
            "Technical",
            "HR",
            "Behavioral",
            "Mixed"
        ]
    )

    experience = st.selectbox(
        "Experience Level",
        [
            "Fresher",
            "0–2 Years",
            "2–5 Years",
            "5+ Years"
        ]
    )

    action = st.selectbox(
        "Choose Action",
        [
            "Generate Questions",
            "Evaluate Answer",
            "Mock Interview"
        ]
    )

    if action == "Evaluate Answer":

        question = st.text_area(
            "Interview Question",
            height=120,
            placeholder="Paste the interview question..."
        )

        answer = st.text_area(
            "Your Answer",
            height=220,
            placeholder="Write your answer here..."
        )

    else:

        question = ""
        answer = ""

    button_labels = {
        "Generate Questions": "📝 Generate Questions",
        "Evaluate Answer": "📊 Evaluate Answer",
        "Mock Interview": "🎤 Start Mock Interview"
    }

    if st.button(
        button_labels[action],
        use_container_width=True
    ):

        if not role.strip():
            st.warning("Please enter a job role.")
            st.stop()

        if action == "Generate Questions":

            prompt = GENERATE_QUESTIONS_PROMPT.format(
                role=role,
                interview_type=interview_type,
                experience=experience,
            )

        elif action == "Evaluate Answer":

            if not question.strip() or not answer.strip():
                st.warning("Please enter both the interview question and your answer.")
                st.stop()

            prompt = EVALUATE_ANSWER_PROMPT.format(
                role=role,
                interview_type=interview_type,
                experience=experience,
                question=question,
                answer=answer,
            )

        else:

            prompt = MOCK_INTERVIEW_PROMPT.format(
                role=role,
                interview_type=interview_type,
                experience=experience,
            )

        with st.spinner("🧠 Gruhini AI is preparing your interview..."):
            response = call_llm(prompt)

        result = st.container()

        with result:
            st.divider()
            st.subheader("🤖 AI Response")
            st.markdown(response)