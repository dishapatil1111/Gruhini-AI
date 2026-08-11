import streamlit as st

from utils.memory_manager import (
    load_profile,
    load_career,
    load_skills,
    update_profile,
    update_career,
    update_skills,
)


# ==================================================
# MEMORY MANAGEMENT PAGE
# ==================================================

def show():

    st.title("🧠 My Memory")

    st.caption(
        "View and manage the information Gruhini has "
        "saved about you."
    )

    st.info(
        "🔒 Your memory is stored locally on your computer. "
        "You can edit or clear it at any time."
    )

    # ==================================================
    # LOAD CURRENT MEMORY
    # ==================================================

    profile = load_profile()
    career = load_career()
    skills = load_skills()

    # ==================================================
    # PROFILE
    # ==================================================

    st.subheader("👤 Profile")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Name",
            value=profile.get("name", ""),
        )

        degree = st.text_input(
            "Degree",
            value=profile.get("degree", ""),
        )

        branch = st.text_input(
            "Branch",
            value=profile.get("branch", ""),
        )

    with col2:

        university = st.text_input(
            "University",
            value=profile.get("university", ""),
        )

        semester = st.text_input(
            "Semester",
            value=profile.get("semester", ""),
        )

        location = st.text_input(
            "Location",
            value=profile.get("location", ""),
        )

    st.divider()

    # ==================================================
    # CAREER
    # ==================================================

    st.subheader("🎯 Career")

    target_role = st.text_input(
        "Target Role",
        value=career.get("target_role", ""),
        placeholder="Example: Data Scientist",
    )

    career_goal = st.text_area(
        "Career Goal",
        value=career.get("career_goal", ""),
        placeholder="Example: Build a career in Data Science",
    )

    target_industry = st.text_input(
        "Target Industry",
        value=career.get("target_industry", ""),
        placeholder="Example: Technology",
    )

    st.divider()

    # ==================================================
    # SKILLS
    # ==================================================

    st.subheader("🛠 Skills")

    st.caption(
        "Separate multiple skills with commas."
    )

    programming_languages = st.text_input(
        "Programming Languages",
        value=", ".join(
            skills.get("programming_languages", [])
        ),
        placeholder="Python, Java, C++",
    )

    frameworks = st.text_input(
        "Frameworks",
        value=", ".join(
            skills.get("frameworks", [])
        ),
        placeholder="Streamlit, React, Django",
    )

    tools = st.text_input(
        "Tools",
        value=", ".join(
            skills.get("tools", [])
        ),
        placeholder="Git, Docker, Ollama",
    )

    ai_ml = st.text_input(
        "AI / ML",
        value=", ".join(
            skills.get("ai_ml", [])
        ),
        placeholder="Machine Learning, Deep Learning",
    )

    data_skills = st.text_input(
        "Data Skills",
        value=", ".join(
            skills.get("data_skills", [])
        ),
        placeholder="SQL, Pandas, Data Analysis",
    )

    st.divider()

    # ==================================================
    # BUTTONS
    # ==================================================

    col_save, col_clear = st.columns(2)

    # ==================================================
    # SAVE
    # ==================================================

    with col_save:

        if st.button(
            "💾 Save Changes",
            use_container_width=True,
        ):

            update_profile(
                name=name.strip(),
                degree=degree.strip(),
                branch=branch.strip(),
                university=university.strip(),
                semester=semester.strip(),
                location=location.strip(),
            )

            update_career(
                target_role=target_role.strip(),
                career_goal=career_goal.strip(),
                target_industry=target_industry.strip(),
            )

            update_skills(
                programming_languages=[
                    x.strip()
                    for x in programming_languages.split(",")
                    if x.strip()
                ],
                frameworks=[
                    x.strip()
                    for x in frameworks.split(",")
                    if x.strip()
                ],
                tools=[
                    x.strip()
                    for x in tools.split(",")
                    if x.strip()
                ],
                ai_ml=[
                    x.strip()
                    for x in ai_ml.split(",")
                    if x.strip()
                ],
                data_skills=[
                    x.strip()
                    for x in data_skills.split(",")
                    if x.strip()
                ],
            )

            st.success(
                "✅ Your memory has been updated."
            )

            st.rerun()

    # ==================================================
    # CLEAR MEMORY
    # ==================================================

    with col_clear:

        if st.button(
            "🗑 Clear All Memory",
            use_container_width=True,
        ):

            st.session_state[
                "confirm_clear_memory"
            ] = True

    # ==================================================
    # CONFIRMATION
    # ==================================================

    if st.session_state.get(
        "confirm_clear_memory",
        False,
    ):

        st.warning(
            "⚠️ This will permanently clear your "
            "saved profile, career information, and skills."
        )

        confirm_col, cancel_col = st.columns(2)

        with confirm_col:

            if st.button(
                "Yes, Clear Everything",
                type="primary",
                use_container_width=True,
            ):

                update_profile(
                    name="",
                    degree="",
                    branch="",
                    university="",
                    semester="",
                    location="",
                )

                update_career(
                    target_role="",
                    career_goal="",
                    target_industry="",
                )

                update_skills(
                    programming_languages=[],
                    frameworks=[],
                    tools=[],
                    ai_ml=[],
                    data_skills=[],
                )

                st.session_state[
                    "confirm_clear_memory"
                ] = False

                st.success(
                    "🗑 All saved memory has been cleared."
                )

                st.rerun()

        with cancel_col:

            if st.button(
                "Cancel",
                use_container_width=True,
            ):

                st.session_state[
                    "confirm_clear_memory"
                ] = False

                st.rerun()