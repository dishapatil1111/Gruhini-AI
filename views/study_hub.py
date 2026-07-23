import streamlit as st
from backend import ask_gruhini
from prompts.study import EXPLAIN_TOPIC_PROMPT


def show():

    st.title("📚 Study Hub")

    st.write("Learn any engineering topic with AI.")

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

        prompt = EXPLAIN_TOPIC_PROMPT.format(
            topic=topic
        )

        with st.spinner("Generating explanation..."):

            response = ask_gruhini(
                prompt,
                [],
                "Study Tutor"
            )

        st.markdown(response)