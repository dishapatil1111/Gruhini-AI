import streamlit as st
import pandas as pd

from utils.interview_history import (
    load_interview_history,
    clear_interview_history,
)

from utils.interview_analytics import (
    get_interview_analytics,
)


# ==================================================
# HELPERS
# ==================================================

def format_date(date_string):
    """
    Convert stored ISO date into a user-friendly format.
    """

    if not date_string:
        return "Unknown date"

    try:

        from datetime import datetime

        date = datetime.fromisoformat(
            date_string
        )

        return date.strftime(
            "%d %b %Y, %I:%M %p"
        )

    except ValueError:

        return date_string


# ==================================================
# INTERVIEW DETAILS
# ==================================================

def show_interview_details(interview):

    questions = interview.get(
        "questions",
        []
    )

    answers = interview.get(
        "answers",
        []
    )

    scores = interview.get(
        "scores",
        []
    )

    feedback = interview.get(
        "feedback",
        []
    )

    total = max(
        len(questions),
        len(answers),
        len(scores),
        len(feedback),
    )

    if total == 0:

        st.info(
            "No detailed question data is available "
            "for this interview."
        )

        return

    for index in range(total):

        question = (
            questions[index]
            if index < len(questions)
            else "Question unavailable."
        )

        answer = (
            answers[index]
            if index < len(answers)
            else "Answer unavailable."
        )

        score = (
            scores[index]
            if index < len(scores)
            else None
        )

        evaluation = (
            feedback[index]
            if index < len(feedback)
            else "Feedback unavailable."
        )

        st.markdown(
            f"### Question {index + 1}"
        )

        st.markdown(
            f"**Question:** {question}"
        )

        if score is not None:

            st.metric(
                "Score",
                f"{score:.1f}/10",
            )

        st.markdown(
            "**Your Answer**"
        )

        st.write(
            answer
        )

        st.markdown(
            "**AI Feedback**"
        )

        st.markdown(
            evaluation
        )

        if index < total - 1:

            st.divider()


# ==================================================
# ANALYTICS
# ==================================================

def show_analytics(history):

    analytics = get_interview_analytics(
        history
    )

    st.subheader(
        "📊 Interview Progress"
    )

    st.caption(
        "Track your interview performance and improvement over time."
    )

    # ==================================================
    # TOP METRICS
    # ==================================================

    total_interviews = analytics.get(
        "total_interviews",
        0
    )

    average_performance = analytics.get(
        "average_performance"
    )

    best_performance = analytics.get(
        "best_performance"
    )

    average_score = analytics.get(
        "average_score"
    )

    improvement = analytics.get(
        "improvement"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Interviews",
            total_interviews,
        )

    with col2:

        if average_performance is not None:

            st.metric(
                "Avg Performance",
                f"{average_performance:.1f}%",
            )

        else:

            st.metric(
                "Avg Performance",
                "N/A",
            )

    with col3:

        if best_performance is not None:

            st.metric(
                "Best Performance",
                f"{best_performance:.1f}%",
            )

        else:

            st.metric(
                "Best Performance",
                "N/A",
            )

    with col4:

        if average_score is not None:

            st.metric(
                "Avg Question Score",
                f"{average_score:.1f}/10",
            )

        else:

            st.metric(
                "Avg Question Score",
                "N/A",
            )

    # ==================================================
    # IMPROVEMENT
    # ==================================================

    if improvement is not None:

        if improvement > 0:

            st.success(
                f"📈 Your performance improved by "
                f"{improvement:.1f} percentage points "
                f"from your first recorded interview."
            )

        elif improvement < 0:

            st.warning(
                f"📉 Your performance decreased by "
                f"{abs(improvement):.1f} percentage points "
                f"from your first recorded interview."
            )

        else:

            st.info(
                "Your performance is unchanged compared "
                "with your first recorded interview."
            )

    else:

        st.info(
            "Complete at least two interviews to see "
            "your performance improvement."
        )

    st.divider()

    # ==================================================
    # PERFORMANCE TREND
    # ==================================================

    trend = analytics.get(
        "performance_trend",
        []
    )

    if trend:

        st.markdown(
            "### 📈 Performance Trend"
        )

        trend_data = pd.DataFrame(
            {
                "Interview": [
                    f"Interview {item['interview_number']}"
                    for item in trend
                ],
                "Performance": [
                    item["performance"]
                    for item in trend
                ],
            }
        )

        st.line_chart(
            trend_data,
            x="Interview",
            y="Performance",
        )

    # ==================================================
    # SCORE DISTRIBUTION
    # ==================================================

    distribution = analytics.get(
        "score_distribution",
        {}
    )

    if distribution:

        st.markdown(
            "### 🎯 Question Score Distribution"
        )

        distribution_data = pd.DataFrame(
            {
                "Score Range": list(
                    distribution.keys()
                ),
                "Questions": list(
                    distribution.values()
                ),
            }
        )

        st.bar_chart(
            distribution_data,
            x="Score Range",
            y="Questions",
        )

    # ==================================================
    # PERFORMANCE BY ROLE
    # ==================================================

    performance_by_role = analytics.get(
        "performance_by_role",
        {}
    )

    if performance_by_role:

        st.markdown(
            "### 💼 Performance by Role"
        )

        role_data = pd.DataFrame(
            {
                "Role": list(
                    performance_by_role.keys()
                ),
                "Performance": list(
                    performance_by_role.values()
                ),
            }
        )

        st.bar_chart(
            role_data,
            x="Role",
            y="Performance",
        )

    # ==================================================
    # PERFORMANCE BY INTERVIEW TYPE
    # ==================================================

    performance_by_type = analytics.get(
        "performance_by_interview_type",
        {}
    )

    if performance_by_type:

        st.markdown(
            "### 🎤 Performance by Interview Type"
        )

        type_data = pd.DataFrame(
            {
                "Interview Type": list(
                    performance_by_type.keys()
                ),
                "Performance": list(
                    performance_by_type.values()
                ),
            }
        )

        st.bar_chart(
            type_data,
            x="Interview Type",
            y="Performance",
        )

    # ==================================================
    # PERFORMANCE BY DIFFICULTY
    # ==================================================

    performance_by_difficulty = analytics.get(
        "performance_by_difficulty",
        {}
    )

    if performance_by_difficulty:

        st.markdown(
            "### ⚡ Performance by Difficulty"
        )

        difficulty_data = pd.DataFrame(
            {
                "Difficulty": list(
                    performance_by_difficulty.keys()
                ),
                "Performance": list(
                    performance_by_difficulty.values()
                ),
            }
        )

        st.bar_chart(
            difficulty_data,
            x="Difficulty",
            y="Performance",
        )


# ==================================================
# MAIN VIEW
# ==================================================

def show():

    st.title(
        "📜 Interview History"
    )

    st.write(
        "Review your previous interview attempts, "
        "scores, answers, and AI feedback."
    )

    history = load_interview_history()

    # ==================================================
    # EMPTY STATE
    # ==================================================

    if not history:

        st.info(
            "📭 No completed interviews yet."
        )

        st.write(
            "Complete an interview in Interview Hub "
            "and your results will automatically appear here."
        )

        if st.button(
            "🎤 Go to Interview Hub",
            type="primary",
            use_container_width=True,
        ):

            st.session_state.page = (
                "Interview Hub"
            )

            st.rerun()

        return

    # ==================================================
    # ANALYTICS
    # ==================================================

    show_analytics(
        history
    )

    st.divider()

    # ==================================================
    # HISTORY HEADER
    # ==================================================

    st.subheader(
        "🗂️ Previous Interviews"
    )

    st.caption(
        "Your most recent interview appears first."
    )

    # ==================================================
    # INTERVIEW LIST
    # ==================================================

    for index, interview in enumerate(
        reversed(history)
    ):

        role = interview.get(
            "role",
            "Unknown Role"
        )

        interview_type = interview.get(
            "interview_type",
            "Unknown"
        )

        experience = interview.get(
            "experience",
            "Unknown"
        )

        difficulty = interview.get(
            "difficulty",
            "Unknown"
        )

        total_questions = interview.get(
            "total_questions",
            0
        )

        average_score = interview.get(
            "average_score"
        )

        performance = interview.get(
            "performance"
        )

        date = format_date(
            interview.get(
                "date"
            )
        )

        interview_number = (
            len(history) - index
        )

        title = (
            f"Interview #{interview_number} — "
            f"{role}"
        )

        with st.expander(
            title,
            expanded=(index == 0),
        ):

            # ------------------------------------------
            # INTERVIEW INFORMATION
            # ------------------------------------------

            st.caption(
                f"📅 {date}"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.markdown(
                    f"**Type**  \n{interview_type}"
                )

            with col2:

                st.markdown(
                    f"**Experience**  \n{experience}"
                )

            with col3:

                st.markdown(
                    f"**Difficulty**  \n{difficulty}"
                )

            with col4:

                st.markdown(
                    f"**Questions**  \n{total_questions}"
                )

            st.divider()

            # ------------------------------------------
            # SCORE SUMMARY
            # ------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                if average_score is not None:

                    st.metric(
                        "Average Score",
                        f"{average_score:.1f}/10",
                    )

                else:

                    st.metric(
                        "Average Score",
                        "N/A",
                    )

            with col2:

                if performance is not None:

                    st.metric(
                        "Performance",
                        f"{performance:.0f}%",
                    )

                else:

                    st.metric(
                        "Performance",
                        "N/A",
                    )

            st.divider()

            # ------------------------------------------
            # DETAILS
            # ------------------------------------------

            show_interview_details(
                interview
            )

    # ==================================================
    # CLEAR HISTORY
    # ==================================================

    st.divider()

    st.subheader(
        "⚙️ History Management"
    )

    if "confirm_clear_interview_history" not in st.session_state:

        st.session_state.confirm_clear_interview_history = False

    if not st.session_state.confirm_clear_interview_history:

        if st.button(
            "🗑️ Clear Interview History",
            use_container_width=True,
        ):

            st.session_state.confirm_clear_interview_history = True

            st.rerun()

    else:

        st.warning(
            "This will permanently delete all saved "
            "interview history from local storage."
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Cancel",
                use_container_width=True,
            ):

                st.session_state.confirm_clear_interview_history = False

                st.rerun()

        with col2:

            if st.button(
                "Delete All History",
                type="primary",
                use_container_width=True,
            ):

                clear_interview_history()

                st.session_state.confirm_clear_interview_history = False

                st.success(
                    "Interview history cleared."
                )

                st.rerun()