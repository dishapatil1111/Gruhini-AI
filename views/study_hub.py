import streamlit as st
from backend import ask_gruhini


def show():

    st.title("📚 Study Hub")

    st.write(
        "Learn any engineering topic with AI."
    )

    topic = st.text_input(
        "Enter a topic",
        placeholder="Example: Binary Search Trees"
    )

    if st.button(
        "Explain Topic",
        use_container_width=True
    ):

        if not topic.strip():
            st.warning("Please enter a topic.")
            return

        prompt = f"""
You are Gruhini AI, an expert engineering tutor.

Explain the topic: {topic}

Rules:
- Respond directly.
- Do NOT mention prompts or instructions.
- Do NOT write things like "If the user asks..."
- Do NOT include follow-up instructions.
- Use Markdown headings.

Format exactly like this:

# Definition

# Why it is Important

# Simple Explanation

# Real-world Example

# Interview Tip

Explain in simple language suitable for engineering students.
"""

        with st.spinner("Generating explanation..."):

            response = ask_gruhini(
                prompt,
                [],
                "Study Tutor"
            )

        st.markdown(response)