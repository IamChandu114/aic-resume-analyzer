import pdfplumber
import re
import json

# Load skill ontology
with open("skills.json", "r") as f:
    SKILLS_DB = json.load(f)


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.lower()


def extract_skills(text):
    found_skills = set()
    for skill, variants in SKILLS_DB.items():
        for variant in variants:
            pattern = r"\b" + re.escape(variant.lower()) + r"\b"
            if re.search(pattern, text):
                found_skills.add(skill)
    return list(found_skills)


def extract_experience(text):
    matches = re.findall(r"(\d+)\+?\s+years?", text)
    if matches:
        return max(int(x) for x in matches)
    return 0


def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)

    return {
        "skills": extract_skills(text),
        "experience_years": extract_experience(text),
        "raw_text": text[:800]
    }
