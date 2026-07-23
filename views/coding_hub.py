import streamlit as st
from backend import call_llm

from prompts.coding import (
    EXPLAIN_CODE_PROMPT,
    DEBUG_CODE_PROMPT,
    OPTIMIZE_CODE_PROMPT,
    GENERATE_CODE_PROMPT,
)

def show():

    st.title("💻 Coding Hub")

    st.write(
        "Write, understand, debug, and generate code with AI."
    )

    language = st.selectbox(
        "Programming Language",
        [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "TypeScript",
    "Go",
    "Rust",
    "PHP",
    "SQL",
    "HTML/CSS",
    "R",
    "MATLAB"
]
    )

    action = st.selectbox(
        "Choose Action",
        [
            "Explain Code",
            "Debug Code",
            "Optimize Code",
            "Generate Code"
        ]
    )

    if action == "Generate Code":
        placeholder = "Describe what you want to build..."
    else:
        placeholder = "Paste your code here..."

    user_input = st.text_area(
        "Code / Requirement",
        height=300,
        placeholder=placeholder
    )

    button_labels = {
        "Explain Code": "📖 Explain Code",
        "Debug Code": "🐞 Debug Code",
        "Optimize Code": "⚡ Optimize Code",
        "Generate Code": "✨ Generate Code"
    }

    if st.button(
        button_labels[action],
        use_container_width=True
):

        if not user_input.strip():
           st.warning("Please enter code or a requirement.")
           st.stop()

        if action == "Explain Code":
           prompt = EXPLAIN_CODE_PROMPT.format(
               language=language,
               code=user_input
           )

        elif action == "Debug Code":
           prompt = DEBUG_CODE_PROMPT.format(
               language=language,
               code=user_input
           )

        elif action == "Optimize Code":
           prompt = OPTIMIZE_CODE_PROMPT.format(
               language=language,
               code=user_input
           )

        else:
           prompt = GENERATE_CODE_PROMPT.format(
               language=language,
               requirement=user_input
           )

        with st.spinner("🧠 Gruhini AI is thinking..."):
            response = call_llm(prompt)

        result = st.container()

        with result:
            st.divider()
            st.subheader("🤖 AI Response")
            st.markdown(response)