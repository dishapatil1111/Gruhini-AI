import re

from utils.memory_manager import (
    update_profile,
    update_career,
    update_skills,
)


# ==================================================
# HELPERS
# ==================================================

def clean_value(value):
    """Clean extracted text before saving it."""

    value = value.strip()

    value = re.sub(
        r"\s+",
        " ",
        value,
    )

    value = value.rstrip(
        ".,!?"
    )

    return value.strip()


# ==================================================
# CAREER MEMORY
# ==================================================

def detect_career_memory(text):
    """
    Detect explicit career statements.

    Examples:

    - I'm preparing for Data Scientist roles.
    - My target role is Data Scientist.
    - I want to become a Machine Learning Engineer.
    - I want to work as a Data Scientist.

    General mentions of careers are NOT saved.
    """

    text = text.strip()

    patterns = [

        # I am preparing for Data Scientist roles
        r"\b(?:i am|i'm|im)\s+"
        r"(?:preparing|prepping)\s+for\s+"
        r"(.+?)(?:\s+roles?)?\.?$",

        # My target role is Data Scientist
        r"\bmy\s+target\s+role\s+is\s+(.+?)\.?$",

        # I want to become a Data Scientist
        r"\bi\s+want\s+to\s+become\s+"
        r"(?:a|an)?\s*(.+?)\.?$",

        # I want to work as a Data Scientist
        r"\bi\s+want\s+to\s+work\s+as\s+"
        r"(?:a|an)?\s*(.+?)\.?$",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if not match:
            continue

        role = clean_value(
            match.group(1)
        )

        role = re.sub(
            r"\s+roles?$",
            "",
            role,
            flags=re.IGNORECASE,
        ).strip()

        if (
            role
            and len(role) <= 100
        ):
            return {
                "target_role": role
            }

    return {}


# ==================================================
# PROFILE MEMORY
# ==================================================

def detect_profile_memory(text):
    """
    Detect explicit profile information.

    Examples:

    - My name is Pooja.
    - I am studying Computer Science.
    - I'm doing MSc Data Science.

    General mentions are NOT saved.
    """

    text = text.strip()

    memory = {}

    # ------------------------------------------------
    # NAME
    # ------------------------------------------------

    name_match = re.search(
        r"\bmy\s+name\s+is\s+"
        r"([A-Za-z][A-Za-z\s'-]{1,50})"
        r"\s*[.!?]?$",
        text,
        re.IGNORECASE,
    )

    if name_match:

        memory["name"] = clean_value(
            name_match.group(1)
        )

    # ------------------------------------------------
    # DEGREE / STUDY
    # ------------------------------------------------

    degree_match = re.search(
        r"\b(?:i am|i'm|im)\s+"
        r"(?:studying|doing)\s+"
        r"(.+?)"
        r"\s*[.!?]?$",
        text,
        re.IGNORECASE,
    )

    if degree_match:

        value = clean_value(
            degree_match.group(1)
        )

        if len(value) <= 100:

            memory["degree"] = value

    return memory


# ==================================================
# SKILL CATEGORIES
# ==================================================

PROGRAMMING_LANGUAGES = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "go",
    "golang",
    "rust",
    "ruby",
    "php",
    "swift",
    "kotlin",
    "r",
}


FRAMEWORKS = {
    "streamlit",
    "django",
    "flask",
    "fastapi",
    "react",
    "angular",
    "vue",
    "spring",
    "spring boot",
    "tensorflow",
    "keras",
    "scikit-learn",
}


TOOLS = {
    "git",
    "github",
    "docker",
    "kubernetes",
    "ollama",
    "jupyter",
    "jupyter notebook",
    "anaconda",
    "vscode",
}


AI_ML = {
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "ai",
    "nlp",
    "natural language processing",
    "computer vision",
    "pytorch",
    "tensorflow",
    "keras",
    "scikit-learn",
    "transformers",
    "hugging face",
    "huggingface",
}


DATA_SKILLS = {
    "sql",
    "mysql",
    "postgresql",
    "postgres",
    "mongodb",
    "pandas",
    "numpy",
    "data analysis",
    "data analytics",
    "data visualization",
    "statistics",
    "power bi",
    "tableau",
    "excel",
    "data cleaning",
    "exploratory data analysis",
    "eda",
    "feature engineering",
}


# ==================================================
# SKILL CLASSIFICATION
# ==================================================

def classify_skill(skill):
    """
    Classify one explicitly provided skill.
    """

    normalized = clean_value(
        skill
    ).lower()

    if normalized in PROGRAMMING_LANGUAGES:
        return "programming_languages"

    if normalized in FRAMEWORKS:
        return "frameworks"

    if normalized in TOOLS:
        return "tools"

    if normalized in AI_ML:
        return "ai_ml"

    if normalized in DATA_SKILLS:
        return "data_skills"

    return None


# ==================================================
# EXPLICIT SKILL STATEMENT DETECTION
# ==================================================

def extract_explicit_skill_text(text):
    """
    Extract the skill portion ONLY when the user
    explicitly claims knowledge or experience.

    Examples accepted:

    I know Python.
    I know Python and SQL.
    I use Git and Docker.
    I work with Python, Pandas and SQL.
    I have experience with Machine Learning.
    I am skilled in Python and SQL.

    Examples rejected:

    What is Python?
    Should I learn Python?
    Python is popular.
    Java is used for backend development.
    Can you explain SQL?
    """
    
    text = text.strip()

    explicit_patterns = [

        # I know Python
        r"^\s*i\s+know\s+(.+?)\s*[.!?]?\s*$",

        # I use Python
        r"^\s*i\s+use\s+(.+?)\s*[.!?]?\s*$",

        # I work with Python
        r"^\s*i\s+work\s+with\s+(.+?)\s*[.!?]?\s*$",

        # I have experience with Python
        r"^\s*i\s+have\s+experience\s+with\s+"
        r"(.+?)\s*[.!?]?\s*$",

        # I am skilled in Python
        r"^\s*i\s+am\s+skilled\s+in\s+"
        r"(.+?)\s*[.!?]?\s*$",

        # I'm skilled in Python
        r"^\s*i'm\s+skilled\s+in\s+"
        r"(.+?)\s*[.!?]?\s*$",

        # I am experienced with Python
        r"^\s*i\s+am\s+experienced\s+with\s+"
        r"(.+?)\s*[.!?]?\s*$",

        # I'm experienced with Python
        r"^\s*i'm\s+experienced\s+with\s+"
        r"(.+?)\s*[.!?]?\s*$",
    ]

    for pattern in explicit_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:

            return clean_value(
                match.group(1)
            )

    return ""


# ==================================================
# SPLIT SKILL LIST
# ==================================================

def split_skill_list(raw_skills):
    """
    Convert natural-language skill lists into
    individual skill strings.

    Examples:

    Python, SQL and Pandas

    Python and SQL

    Python, Streamlit, Git
    """

    raw_skills = clean_value(
        raw_skills
    )

    # Convert " and " into commas
    raw_skills = re.sub(
        r"\s+\band\b\s+",
        ",",
        raw_skills,
        flags=re.IGNORECASE,
    )

    # Split by commas
    parts = raw_skills.split(",")

    skills = []

    for part in parts:

        skill = clean_value(
            part
        )

        if not skill:
            continue

        # Avoid very long suspicious values
        if len(skill) > 50:
            continue

        skills.append(skill)

    return skills


# ==================================================
# SKILL MEMORY
# ==================================================

def detect_skill_memory(text):
    """
    Detect skills ONLY from explicit ownership/
    experience statements.

    A skill being mentioned in a question or general
    sentence is NOT enough to save it.
    """

    raw_skills = extract_explicit_skill_text(
        text
    )

    if not raw_skills:
        return {}

    skills = split_skill_list(
        raw_skills
    )

    if not skills:
        return {}

    categorized = {
        "programming_languages": [],
        "frameworks": [],
        "tools": [],
        "ai_ml": [],
        "data_skills": [],
    }

    for skill in skills:

        category = classify_skill(
            skill
        )

        if category:

            categorized[
                category
            ].append(skill)

    # Remove empty categories
    categorized = {
        key: value
        for key, value in categorized.items()
        if value
    }

    if categorized:
        return categorized

    return {}


# ==================================================
# MAIN MEMORY EXTRACTION
# ==================================================

def extract_memory(text):
    """
    Extract ONLY explicit user information.

    This function does not write anything to disk.
    """

    if not isinstance(text, str):
        return {
            "profile": {},
            "career": {},
            "skills": {},
        }

    text = text.strip()

    if not text:
        return {
            "profile": {},
            "career": {},
            "skills": {},
        }

    return {
        "profile": detect_profile_memory(text),
        "career": detect_career_memory(text),
        "skills": detect_skill_memory(text),
    }


# ==================================================
# SAVE EXTRACTED MEMORY
# ==================================================

def save_extracted_memory(memory):
    """
    Save ONLY explicitly detected memory.
    """

    if not isinstance(
        memory,
        dict,
    ):
        return

    profile = memory.get(
        "profile",
        {},
    )

    career = memory.get(
        "career",
        {},
    )

    skill_data = memory.get(
        "skills",
        {},
    )

    # ------------------------------------------------
    # PROFILE
    # ------------------------------------------------

    if profile:

        update_profile(
            **profile
        )

    # ------------------------------------------------
    # CAREER
    # ------------------------------------------------

    if career:

        update_career(
            **career
        )

    # ------------------------------------------------
    # SKILLS
    # ------------------------------------------------

    if skill_data:

        from utils.memory_manager import load_skills

        current = load_skills()

        for category, detected_skills in skill_data.items():

            if category not in current:
                current[category] = []

            existing = current.get(
                category,
                [],
            )

            for skill in detected_skills:

                # Case-insensitive duplicate check
                already_exists = any(
                    existing_skill.lower()
                    == skill.lower()
                    for existing_skill in existing
                )

                if not already_exists:

                    existing.append(
                        skill
                    )

            current[category] = existing

        update_skills(
            **current
        )