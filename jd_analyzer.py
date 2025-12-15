import re
import json

# Load skill ontology
with open("skills.json", "r") as f:
    SKILLS_DB = json.load(f)


def extract_jd_skills(text):
    text = text.lower()
    required = set()
    preferred = set()

    for skill, variants in SKILLS_DB.items():
        for variant in variants:
            if re.search(r"\b" + re.escape(variant) + r"\b", text):
                if "preferred" in text or "nice to have" in text:
                    preferred.add(skill)
                else:
                    required.add(skill)

    return {
        "required_skills": list(required),
        "preferred_skills": list(preferred)
    }


def extract_experience_level(text):
    match = re.search(r"(\d+)\+?\s+years?", text.lower())
    return int(match.group(1)) if match else 0


def parse_job_description(jd_text):
    return {
        "skills": extract_jd_skills(jd_text),
        "experience_required": extract_experience_level(jd_text)
    }
