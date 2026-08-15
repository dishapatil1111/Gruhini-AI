import json
from pathlib import Path
from datetime import datetime


# ============================================================
# STORAGE
# ============================================================

DATA_DIR = (
    Path(__file__).resolve().parent.parent / "data"
)

HISTORY_FILE = DATA_DIR / "interview_history.json"


# ============================================================
# DEFAULT STORAGE
# ============================================================

def _default_history():
    """
    Return an empty interview history structure.
    """

    return []


# ============================================================
# ENSURE STORAGE
# ============================================================

def _ensure_storage():
    """
    Make sure the data directory and history file exist.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not HISTORY_FILE.exists():

        HISTORY_FILE.write_text(
            json.dumps(
                _default_history(),
                indent=2
            ),
            encoding="utf-8"
        )


# ============================================================
# LOAD HISTORY
# ============================================================

def load_interview_history():
    """
    Load all saved interview attempts.

    Returns:
        list: Interview history records.
    """

    _ensure_storage()

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):

            return data

        return _default_history()

    except (
        json.JSONDecodeError,
        OSError
    ):

        return _default_history()


# ============================================================
# SAVE HISTORY
# ============================================================

def save_interview_history(history):
    """
    Save the complete interview history.
    """

    _ensure_storage()

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=2,
            ensure_ascii=False
        )


# ============================================================
# ADD INTERVIEW
# ============================================================

def add_interview_record(
    role,
    interview_type,
    experience,
    difficulty,
    questions,
    answers,
    scores,
    feedback,
    average_score,
    performance
):
    """
    Add one completed interview attempt
    to persistent storage.
    """

    history = load_interview_history()

    record = {
        "id": datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        ),

        "date": datetime.now().isoformat(
            timespec="seconds"
        ),

        "role": role,

        "interview_type": interview_type,

        "experience": experience,

        "difficulty": difficulty,

        "total_questions": len(
            questions
        ),

        "questions": questions,

        "answers": answers,

        "scores": scores,

        "feedback": feedback,

        "average_score": average_score,

        "performance": performance,
    }

    history.append(record)

    save_interview_history(
        history
    )

    return record


# ============================================================
# GET LATEST INTERVIEW
# ============================================================

def get_latest_interview():
    """
    Return the most recent interview attempt.

    Returns:
        dict or None
    """

    history = load_interview_history()

    if not history:

        return None

    return history[-1]


# ============================================================
# GET INTERVIEW COUNT
# ============================================================

def get_interview_count():
    """
    Return the total number of completed interviews.
    """

    return len(
        load_interview_history()
    )


# ============================================================
# CLEAR HISTORY
# ============================================================

def clear_interview_history():
    """
    Delete all saved interview history.
    """

    save_interview_history(
        _default_history()
    )