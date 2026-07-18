import streamlit as st

from utils.session import initialize_session
from components.sidebar import show_sidebar

from views.dashboard import show as show_dashboard
from views.ai_chat import show as show_ai_chat
from views.study_hub import show as show_study_hub
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
    with open("assets/css/style.css") as f:
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

else:
    st.title("🚧")
    st.info(f"{page} is under development.")