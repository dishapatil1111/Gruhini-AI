import json
from pathlib import Path


# --------------------------------------------------
# Memory Storage
# --------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROFILE_FILE = DATA_DIR / "profile.json"
CAREER_FILE = DATA_DIR / "career.json"
SKILLS_FILE = DATA_DIR / "skills.json"

# --------------------------------------------------
# Ensure Storage Exists
# --------------------------------------------------

def _ensure_storage():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not PROFILE_FILE.exists():
        PROFILE_FILE.write_text(
            json.dumps(
                {
                    "name": "",
                    "degree": "",
                    "branch": "",
                    "university": "",
                    "semester": "",
                    "location": ""
                },
                indent=2
            ),
            encoding="utf-8"
        )


# --------------------------------------------------
# Load Profile
# --------------------------------------------------

def load_profile():
    _ensure_storage()

    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {
            "name": "",
            "degree": "",
            "branch": "",
            "university": "",
            "semester": "",
            "location": ""
        }


# --------------------------------------------------
# Update Profile
# --------------------------------------------------

def update_profile(**updates):
    profile = load_profile()

    for key, value in updates.items():
        if value is not None:
            profile[key] = value

    _ensure_storage()

    with open(PROFILE_FILE, "w", encoding="utf-8") as file:
        json.dump(profile, file, indent=2)

    return profile



# --------------------------------------------------
# Load Career
# --------------------------------------------------

def load_career():
    _ensure_storage()

    if not CAREER_FILE.exists():
        CAREER_FILE.write_text(
            json.dumps(
                {
                    "target_role": "",
                    "career_goal": "",
                    "target_industry": ""
                },
                indent=2
            ),
            encoding="utf-8"
        )

    try:
        with open(CAREER_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {
            "target_role": "",
            "career_goal": "",
            "target_industry": ""
        }



    # --------------------------------------------------
# Update Career
# --------------------------------------------------

def update_career(**updates):
    career = load_career()

    for key, value in updates.items():
        if value is not None:
            career[key] = value

    with open(CAREER_FILE, "w", encoding="utf-8") as file:
        json.dump(career, file, indent=2)

    return career

# --------------------------------------------------
# Load Skills
# --------------------------------------------------

def load_skills():
    _ensure_storage()

    if not SKILLS_FILE.exists():
        SKILLS_FILE.write_text(
            json.dumps(
                {
                    "programming_languages": [],
                    "frameworks": [],
                    "tools": [],
                    "ai_ml": [],
                    "data_skills": []
                },
                indent=2
            ),
            encoding="utf-8"
        )

    try:
        with open(SKILLS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {
            "programming_languages": [],
            "frameworks": [],
            "tools": [],
            "ai_ml": [],
            "data_skills": []
        }

    # --------------------------------------------------
# Update Skills
# --------------------------------------------------

def update_skills(**updates):
    skills = load_skills()

    for key, value in updates.items():
        if value is not None:
            skills[key] = value

    with open(SKILLS_FILE, "w", encoding="utf-8") as file:
        json.dump(skills, file, indent=2)

    return skills