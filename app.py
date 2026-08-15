import streamlit as st

from utils.session import initialize_session
from components.sidebar import show_sidebar

from views.coding_hub import show as show_coding_hub
from views.dashboard import show as show_dashboard
from views.ai_chat import show as show_ai_chat
from views.study_hub import show as show_study_hub
from views.interview_hub import show as show_interview_hub
from views.interview_history import show as show_interview_history
from views.career_hub import show as show_career_hub
from views.memory import show as show_memory


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Gruhini AI",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# CSS
# ==========================================

def load_css():

    with open(
        "assets/css/style.css",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# ==========================================
# SESSION
# ==========================================

initialize_session()


# ==========================================
# SIDEBAR
# ==========================================

show_sidebar()


# ==========================================
# ROUTER
# ==========================================

page = st.session_state.page


if page == "Dashboard":

    show_dashboard()


elif page == "AI Chat":

    show_ai_chat()


elif page == "Study Hub":

    show_study_hub()


elif page == "Coding Hub":

    show_coding_hub()


elif page == "Interview Hub":

    show_interview_hub()

elif page == "Interview History":

    show_interview_history()


elif page == "Career Hub":

    show_career_hub()


elif page == "My Memory":

    show_memory()


else:

    st.title("🚧")
    st.info(
        f"{page} is under development."
    )