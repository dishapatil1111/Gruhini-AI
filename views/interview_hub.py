import streamlit as st

from backend import call_llm
from utils.memory_manager import load_career, load_skills
from utils.interview_history import (
    add_interview_record,
    load_interview_history,
)

from prompts.interview import (
    GENERATE_QUESTIONS_PROMPT,
    EVALUATE_ANSWER_PROMPT,
    MOCK_INTERVIEW_PROMPT,
)


# ==================================================
# SESSION HELPERS
# ==================================================

def initialize_interview_state():

    defaults = {
        "interview_started": False,
        "interview_finished": False,
        "interview_role": "",
        "interview_type": "Technical",
        "interview_experience": "Fresher",
        "interview_difficulty": "Medium",
        "interview_total_questions": 5,
        "interview_current_question": 0,
        "interview_questions": [],
        "interview_answers": [],
        "interview_scores": [],
        "interview_feedback": [],
        "interview_current_answer": "",
        "interview_history_saved": False,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


def reset_interview():

    keys = [
        "interview_started",
        "interview_finished",
        "interview_role",
        "interview_type",
        "interview_experience",
        "interview_difficulty",
        "interview_total_questions",
        "interview_current_question",
        "interview_questions",
        "interview_answers",
        "interview_scores",
        "interview_feedback",
        "interview_current_answer",
        "interview_history_saved",
    ]

    for key in keys:

        if key in st.session_state:
            del st.session_state[key]

    initialize_interview_state()


# ==================================================
# MEMORY CONTEXT
# ==================================================

def get_candidate_context():

    career = load_career()
    skills = load_skills()

    return {
        "career": career,
        "skills": skills,
    }


def format_skills(skills):

    categories = {
        "Programming Languages": "programming_languages",
        "Frameworks": "frameworks",
        "Tools": "tools",
        "AI/ML": "ai_ml",
        "Data Skills": "data_skills",
    }

    lines = []

    for label, key in categories.items():

        values = skills.get(
            key,
            []
        )

        if values:

            lines.append(
                f"{label}: {', '.join(values)}"
            )

    if not lines:
        return "No saved skills."

    return "\n".join(lines)


# ==================================================
# ADAPTIVE INTERVIEW CONTEXT
# ==================================================

def get_adaptive_interview_context(
    role,
    interview_type,
):
    """
    Build adaptive context from previous interviews
    for the same role and interview type.

    Previous question scores are classified into:

        < 7.0       -> Needs Practice
        7.0 - 7.9   -> Developing
        8.0 - 8.9   -> Solid
        9.0 - 10.0  -> Strong

    The classification is evidence-based and does not
    invent weaknesses when the history does not support them.
    """

    history = load_interview_history()

    if not history:

        return {
            "has_history": False,
            "context": "",
        }

    matching_interviews = []

    normalized_role = (
        role.strip().lower()
    )

    normalized_type = (
        interview_type.strip().lower()
    )

    # --------------------------------------------------
    # FIND MATCHING ROLE + INTERVIEW TYPE
    # --------------------------------------------------

    for interview in history:

        previous_role = str(
            interview.get(
                "role",
                ""
            )
        ).strip().lower()

        previous_type = str(
            interview.get(
                "interview_type",
                ""
            )
        ).strip().lower()

        if (
            previous_role == normalized_role
            and previous_type == normalized_type
        ):

            matching_interviews.append(
                interview
            )

    if not matching_interviews:

        return {
            "has_history": False,
            "context": "",
        }

    # --------------------------------------------------
    # USE MOST RECENT THREE MATCHING INTERVIEWS
    # --------------------------------------------------

    matching_interviews = (
        matching_interviews[-3:]
    )

    context_lines = [
        "Previous interview performance for "
        f"{role} ({interview_type}):"
    ]

    previous_questions = []

    needs_practice = []
    developing = []
    solid = []
    strong = []

    # ==================================================
    # ANALYZE PREVIOUS INTERVIEWS
    # ==================================================

    for index, interview in enumerate(
        matching_interviews,
        start=1,
    ):

        average_score = interview.get(
            "average_score"
        )

        performance = interview.get(
            "performance"
        )

        date = interview.get(
            "date",
            "Unknown date"
        )

        if average_score is not None:

            if performance is not None:

                performance_text = (
                    f"{performance:.1f}%"
                )

            else:

                performance_text = "Unavailable"

            context_lines.append(
                f"- Interview {index}: "
                f"Average score "
                f"{average_score:.1f}/10, "
                f"Performance "
                f"{performance_text} "
                f"({date})"
            )

        questions = interview.get(
            "questions",
            []
        )

        scores = interview.get(
            "scores",
            []
        )

        for question_index, question in enumerate(
            questions
        ):

            if not question:
                continue

            question_text = str(
                question
            ).strip()

            previous_questions.append(
                question_text
            )

            score = None

            if question_index < len(scores):

                score = scores[
                    question_index
                ]

            if score is None:
                continue

            try:

                score = float(score)

            except (
                TypeError,
                ValueError
            ):

                continue

            question_entry = (
                f"- {question_text} "
                f"[Score: {score:.1f}/10]"
            )

            # ------------------------------------------
            # SCORE CLASSIFICATION
            # ------------------------------------------

            if score < 7:

                needs_practice.append(
                    question_entry
                )

            elif score < 8:

                developing.append(
                    question_entry
                )

            elif score < 9:

                solid.append(
                    question_entry
                )

            else:

                strong.append(
                    question_entry
                )

    # ==================================================
    # PERFORMANCE AREAS
    # ==================================================

    if needs_practice:

        context_lines.extend(
            [
                "",
                "Areas needing additional practice "
                "based on previous scores:",
            ]
        )

        for item in needs_practice[-5:]:

            context_lines.append(
                item
            )

    if developing:

        context_lines.extend(
            [
                "",
                "Developing areas:",
            ]
        )

        for item in developing[-5:]:

            context_lines.append(
                item
            )

    if solid:

        context_lines.extend(
            [
                "",
                "Solid areas:",
            ]
        )

        for item in solid[-5:]:

            context_lines.append(
                item
            )

    if strong:

        context_lines.extend(
            [
                "",
                "Strong demonstrated areas:",
            ]
        )

        for item in strong[-8:]:

            context_lines.append(
                item
            )

    # ==================================================
    # PREVIOUS QUESTIONS
    # ==================================================

    if previous_questions:

        context_lines.extend(
            [
                "",
                "Questions that have already "
                "been asked and must NOT be repeated:",
            ]
        )

        for question in previous_questions[-15:]:

            context_lines.append(
                f"- {question}"
            )

    # ==================================================
    # ADAPTIVE STRATEGY
    # ==================================================

    context_lines.extend(
        [
            "",
            "Adaptive strategy:",
        ]
    )

    if needs_practice:

        context_lines.extend(
            [
                "- Prioritize additional practice "
                "around concepts represented by "
                "lower-scoring previous questions.",
                "- Do not repeat the original question.",
                "- Ask a fresh question testing the "
                "same underlying concept or skill.",
            ]
        )

    elif developing:

        context_lines.extend(
            [
                "- Include some additional practice "
                "for developing areas.",
                "- Use a fresh question and explore "
                "the concept from a different angle.",
            ]
        )

    elif solid:

        context_lines.extend(
            [
                "- The candidate has demonstrated "
                "solid performance.",
                "- Introduce fresh application-based "
                "or reasoning-oriented questions.",
            ]
        )

    else:

        context_lines.extend(
            [
                "- No weak areas are supported by "
                "the available history.",
                "- Do not invent weaknesses.",
                "- Focus on fresh questions that "
                "progressively test deeper understanding, "
                "practical application, trade-offs, "
                "debugging, or scenario-based reasoning.",
            ]
        )

    context_lines.extend(
        [
            "- Respect the difficulty selected by "
            "the candidate.",
            "- Do not automatically increase "
            "difficulty.",
            "- Do not claim the candidate is weak "
            "or strong in a topic unless the previous "
            "scores support that conclusion.",
        ]
    )

    return {
        "has_history": True,
        "context": "\n".join(
            context_lines
        ),
    }


# ==================================================
# QUESTION GENERATION
# ==================================================

def generate_interview_questions(
    role,
    interview_type,
    experience,
    difficulty,
    number_of_questions,
    skills,
):

    skill_context = format_skills(
        skills
    )

    adaptive_data = get_adaptive_interview_context(
        role=role,
        interview_type=interview_type,
    )

    adaptive_context = adaptive_data[
        "context"
    ]

    if not adaptive_context:

        adaptive_context = (
            "No previous interview history is available "
            "for this role and interview type. "
            "Generate a fresh interview normally."
        )

    prompt = f"""
You are Gruhini AI's professional interview engine.

Generate exactly {number_of_questions} interview questions.

Candidate information:

Job Role:
{role}

Interview Type:
{interview_type}

Experience Level:
{experience}

Difficulty:
{difficulty}

Candidate's Saved Skills:
{skill_context}

Previous Interview Context:
{adaptive_context}

Rules:

1. Generate exactly {number_of_questions} questions.

2. Questions must be relevant to the selected job role.

3. Questions must match the interview type.

4. Match the requested difficulty.

5. For Technical interviews, prioritize the candidate's
   actual saved skills when appropriate.

6. Do not claim that the candidate knows a skill that is
   not listed above.

7. Use previous interview context to personalize
   the new interview.

8. Do not repeat any previous interview question.

9. If previous questions scored below 7/10, provide
   additional practice around the underlying concepts,
   but ask a new question rather than repeating the
   original question.

10. If previous questions scored 7.0–7.9/10, include
    some additional practice while approaching the
    concept from a different angle.

11. If previous questions scored 8.0/10 or higher,
    treat the area as demonstrated competence and
    prioritize fresh application, reasoning, practical
    scenarios, trade-offs, debugging, or deeper
    understanding while respecting the selected
    difficulty.

12. Never invent a weakness when the previous scores
    do not support one.

13. Do not automatically increase the selected
    interview difficulty.

14. NEVER mention previous interviews, previous
    questions, previous scores, interview history,
    demonstrated proficiency, demonstrated ability,
    or the adaptive process in the generated question.

15. NEVER use introductions such as:
    "You've demonstrated..."
    "You've shown..."
    "Based on your previous answer..."
    "Since you performed well..."
    "Let's dive deeper into this topic based on..."
    "As you previously demonstrated..."

16. The candidate must see only the interview question,
    not the reasoning behind why the question was chosen.

17. Do not provide answers.

18. Do not number the questions with additional
    commentary.

19. Return one question per line.

20. Keep questions concise and realistic.

21. Do not mention previous interview scores in
    the questions.

22. Avoid asking the same underlying question in
    slightly different wording.

23. Do not include labels such as:
    "Adaptive Question:"
    "Follow-up Question:"
    "Based on your performance:"
    or "Personalized Question:"

24. Output ONLY the interview questions.

QUESTIONS:
"""

    response = call_llm(
        prompt
    )

    questions = []

    for line in response.splitlines():

        line = line.strip()

        if not line:
            continue

        # Remove common numbering.
        line = line.lstrip(
            "0123456789.-) "
        ).strip()

        if len(line) > 10:

            questions.append(
                line
            )

    # ==================================================
    # REMOVE EXACT DUPLICATES
    # ==================================================

    unique_questions = []

    seen = set()

    for question in questions:

        normalized = (
            question
            .strip()
            .lower()
        )

        if normalized in seen:
            continue

        seen.add(
            normalized
        )

        unique_questions.append(
            question
        )

    return unique_questions[
        :number_of_questions
    ]


# ==================================================
# ANSWER EVALUATION
# ==================================================

def evaluate_answer(
    role,
    interview_type,
    experience,
    difficulty,
    question,
    answer,
):

    prompt = f"""
You are an expert technical interviewer.

Evaluate the candidate's answer.

Job Role:
{role}

Interview Type:
{interview_type}

Experience Level:
{experience}

Difficulty:
{difficulty}

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer using this exact format:

Score: X/10
Rating: Excellent/Good/Average/Poor
Strengths: short
Weaknesses: short
Feedback: short
Ideal Answer: short

Rules:

- Score based on correctness, relevance,
  clarity, and completeness.
- Do not invent facts about the candidate.
- Be constructive.
- Keep the evaluation concise.
"""

    return call_llm(
        prompt
    )


# ==================================================
# SCORE EXTRACTION
# ==================================================

def extract_score(response):

    import re

    match = re.search(
        r"Score\s*:\s*(\d+(?:\.\d+)?)\s*/\s*10",
        response,
        re.IGNORECASE,
    )

    if not match:
        return None

    try:

        score = float(
            match.group(1)
        )

        return max(
            0,
            min(
                10,
                score
            )
        )

    except ValueError:

        return None


# ==================================================
# FINAL REPORT
# ==================================================

def generate_final_report():

    scores = (
        st.session_state.interview_scores
    )

    if not scores:

        return (
            "No scored answers are available."
        )

    valid_scores = [
        score
        for score in scores
        if score is not None
    ]

    if valid_scores:

        average = (
            sum(valid_scores)
            / len(valid_scores)
        )

        average_text = (
            f"{average:.1f}/10"
        )

    else:

        average_text = "Unavailable"

    role = (
        st.session_state.interview_role
    )

    feedback_text = "\n\n".join(
        [
            f"Question {index + 1}:\n{feedback}"
            for index, feedback
            in enumerate(
                st.session_state.interview_feedback
            )
        ]
    )

    prompt = f"""
You are Gruhini AI's interview coach.

Create a concise final interview performance report.

Job Role:
{role}

Average Score:
{average_text}

Individual Evaluations:
{feedback_text}

Use this format:

## Overall Performance
Short assessment.

## Strong Areas
- ...
- ...

## Areas to Improve
- ...
- ...

## Recommended Next Steps
- ...
- ...
- ...

Rules:

- Base the report only on the evaluations provided.
- Do not invent candidate skills.
- Be practical and constructive.
"""

    return call_llm(
        prompt
    )


# ==================================================
# SAVE COMPLETED INTERVIEW
# ==================================================

def save_completed_interview():

    # Prevent duplicate saves caused by Streamlit reruns.
    if st.session_state.interview_history_saved:

        return

    scores = (
        st.session_state.interview_scores
    )

    valid_scores = [
        score
        for score in scores
        if score is not None
    ]

    if valid_scores:

        average_score = (
            sum(valid_scores)
            / len(valid_scores)
        )

        performance = (
            average_score * 10
        )

    else:

        average_score = None
        performance = None

    add_interview_record(
        role=(
            st.session_state
            .interview_role
        ),
        interview_type=(
            st.session_state
            .interview_type
        ),
        experience=(
            st.session_state
            .interview_experience
        ),
        difficulty=(
            st.session_state
            .interview_difficulty
        ),
        questions=(
            st.session_state
            .interview_questions
        ),
        answers=(
            st.session_state
            .interview_answers
        ),
        scores=(
            st.session_state
            .interview_scores
        ),
        feedback=(
            st.session_state
            .interview_feedback
        ),
        average_score=average_score,
        performance=performance,
    )

    # Mark as saved only after successful persistence.
    st.session_state.interview_history_saved = True


# ==================================================
# MAIN VIEW
# ==================================================

def show():

    initialize_interview_state()

    st.title(
        "🎤 Interview Hub"
    )

    st.write(
        "Practice realistic interviews and receive "
        "AI-powered feedback based on your role and skills."
    )

    # ==================================================
    # ACTIVE INTERVIEW
    # ==================================================

    if st.session_state.interview_started:

        role = (
            st.session_state
            .interview_role
        )

        current_index = (
            st.session_state
            .interview_current_question
        )

        total_questions = (
            st.session_state
            .interview_total_questions
        )

        # ----------------------------------------------
        # FINAL REPORT
        # ----------------------------------------------

        if (
            st.session_state.interview_finished
            or current_index >= total_questions
        ):

            st.session_state.interview_finished = True

            # ------------------------------------------
            # SAVE COMPLETED INTERVIEW ONCE
            # ------------------------------------------

            save_completed_interview()

            st.success(
                "🎉 Interview completed!"
            )

            st.subheader(
                "🏆 Final Performance Report"
            )

            with st.spinner(
                "🧠 Analyzing your interview..."
            ):

                report = (
                    generate_final_report()
                )

            st.markdown(
                report
            )

            st.divider()

            scores = (
                st.session_state
                .interview_scores
            )

            valid_scores = [
                score
                for score in scores
                if score is not None
            ]

            if valid_scores:

                average = (
                    sum(valid_scores)
                    / len(valid_scores)
                )

                col1, col2, col3 = (
                    st.columns(3)
                )

                with col1:

                    st.metric(
                        "Questions",
                        total_questions,
                    )

                with col2:

                    st.metric(
                        "Average Score",
                        f"{average:.1f}/10",
                    )

                with col3:

                    percentage = (
                        average * 10
                    )

                    st.metric(
                        "Performance",
                        f"{percentage:.0f}%",
                    )

            if st.button(
                "🔄 Start New Interview",
                use_container_width=True,
            ):

                reset_interview()

                st.rerun()

            return

        # ----------------------------------------------
        # INTERVIEW HEADER
        # ----------------------------------------------

        st.info(
            f"🎯 {role} | "
            f"{st.session_state.interview_type} | "
            f"{st.session_state.interview_difficulty}"
        )

        progress = (
            current_index
            / total_questions
        )

        st.progress(
            progress
        )

        st.caption(
            f"Question {current_index + 1} "
            f"of {total_questions}"
        )

        # ----------------------------------------------
        # CURRENT QUESTION
        # ----------------------------------------------

        question = (
            st.session_state
            .interview_questions[current_index]
        )

        st.subheader(
            f"❓ {question}"
        )

        answer = st.text_area(
            "Your Answer",
            key=f"answer_{current_index}",
            height=220,
            placeholder=(
                "Type your interview answer here..."
            ),
        )

        if st.button(
            "📊 Submit Answer",
            type="primary",
            use_container_width=True,
        ):

            if not answer.strip():

                st.warning(
                    "Please enter your answer before submitting."
                )

                st.stop()

            with st.spinner(
                "🧠 Evaluating your answer..."
            ):

                evaluation = evaluate_answer(
                    role=role,
                    interview_type=(
                        st.session_state
                        .interview_type
                    ),
                    experience=(
                        st.session_state
                        .interview_experience
                    ),
                    difficulty=(
                        st.session_state
                        .interview_difficulty
                    ),
                    question=question,
                    answer=answer,
                )

            score = extract_score(
                evaluation
            )

            st.session_state.interview_answers.append(
                answer
            )

            st.session_state.interview_scores.append(
                score
            )

            st.session_state.interview_feedback.append(
                evaluation
            )

            st.session_state.interview_current_question += 1

            st.rerun()

        # ----------------------------------------------
        # PREVIOUS RESULTS
        # ----------------------------------------------

        if st.session_state.interview_feedback:

            st.divider()

            st.subheader(
                "📊 Previous Feedback"
            )

            last_index = (
                len(
                    st.session_state
                    .interview_feedback
                )
                - 1
            )

            last_feedback = (
                st.session_state
                .interview_feedback[
                    last_index
                ]
            )

            last_score = (
                st.session_state
                .interview_scores[
                    last_index
                ]
            )

            if last_score is not None:

                st.metric(
                    "Latest Score",
                    f"{last_score:.1f}/10",
                )

            with st.expander(
                "View latest feedback",
                expanded=True,
            ):

                st.markdown(
                    last_feedback
                )

        return

    # ==================================================
    # INTERVIEW SETUP
    # ==================================================

    st.subheader(
        "⚙️ Interview Setup"
    )

    career = load_career()

    skills = load_skills()

    saved_role = career.get(
        "target_role",
        "",
    ).strip()

    # ----------------------------------------------
    # ROLE
    # ----------------------------------------------

    role_options = [
        "Software Engineer",
        "Data Scientist",
        "Data Analyst",
        "Machine Learning Engineer",
        "Frontend Developer",
        "Backend Developer",
        "DevOps Engineer",
        "Cybersecurity Engineer",
        "Custom",
    ]

    default_index = 0

    if saved_role:

        for index, option in enumerate(
            role_options
        ):

            if (
                option.lower()
                == saved_role.lower()
            ):

                default_index = index

                break

    role = st.selectbox(
        "Job Role",
        role_options,
        index=default_index,
    )

    if role == "Custom":

        role = st.text_input(
            "Enter Job Role",
            placeholder=(
                "Example: AI Research Engineer"
            ),
        )

    elif saved_role:

        st.caption(
            f"🧠 Using your saved career goal: "
            f"{saved_role}"
        )

    # ----------------------------------------------
    # INTERVIEW TYPE
    # ----------------------------------------------

    interview_type = st.selectbox(
        "Interview Type",
        [
            "Technical",
            "HR",
            "Behavioral",
            "Mixed",
        ],
    )

    # ----------------------------------------------
    # EXPERIENCE
    # ----------------------------------------------

    experience = st.selectbox(
        "Experience Level",
        [
            "Fresher",
            "0–2 Years",
            "2–5 Years",
            "5+ Years",
        ],
    )

    # ----------------------------------------------
    # DIFFICULTY
    # ----------------------------------------------

    difficulty = st.select_slider(
        "Difficulty",
        options=[
            "Easy",
            "Medium",
            "Hard",
        ],
        value="Medium",
    )

    # ----------------------------------------------
    # QUESTION COUNT
    # ----------------------------------------------

    number_of_questions = st.slider(
        "Number of Questions",
        min_value=3,
        max_value=10,
        value=5,
    )

    # ----------------------------------------------
    # CURRENT SKILLS
    # ----------------------------------------------

    with st.expander(
        "🧠 Your saved skills",
        expanded=False,
    ):

        st.markdown(
            format_skills(
                skills
            )
        )

    # ----------------------------------------------
    # START
    # ----------------------------------------------

    if st.button(
        "🎤 Start Interview",
        type="primary",
        use_container_width=True,
    ):

        if not role.strip():

            st.warning(
                "Please enter a job role."
            )

            st.stop()

        with st.spinner(
            "🧠 Gruhini is preparing your interview..."
        ):

            questions = (
                generate_interview_questions(
                    role=role,
                    interview_type=interview_type,
                    experience=experience,
                    difficulty=difficulty,
                    number_of_questions=(
                        number_of_questions
                    ),
                    skills=skills,
                )
            )

        if not questions:

            st.error(
                "I couldn't generate interview questions. "
                "Please try again."
            )

            st.stop()

        if len(questions) < number_of_questions:

            st.warning(
                f"Generated {len(questions)} "
                f"questions instead of "
                f"{number_of_questions}."
            )

        st.session_state.interview_started = True

        st.session_state.interview_finished = False

        st.session_state.interview_history_saved = False

        st.session_state.interview_role = role

        st.session_state.interview_type = (
            interview_type
        )

        st.session_state.interview_experience = (
            experience
        )

        st.session_state.interview_difficulty = (
            difficulty
        )

        st.session_state.interview_total_questions = (
            len(questions)
        )

        st.session_state.interview_current_question = 0

        st.session_state.interview_questions = (
            questions
        )

        st.session_state.interview_answers = []

        st.session_state.interview_scores = []

        st.session_state.interview_feedback = []

        st.rerun()