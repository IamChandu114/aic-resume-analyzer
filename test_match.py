from match_engine import calculate_skill_match, calculate_experience_match, generate_final_score

resume_data = {
    "skills": ["python", "sql", "machine learning"],
    "experience_years": 1
}

jd_data = {
    "skills": {
        "required_skills": ["python", "sql", "flask"],
        "preferred_skills": ["machine learning"]
    },
    "experience_required": 2
}

skill_score, missing_skills = calculate_skill_match(
    resume_data["skills"],
    jd_data["skills"]["required_skills"],
    jd_data["skills"]["preferred_skills"]
)

exp_score = calculate_experience_match(
    resume_data["experience_years"],
    jd_data["experience_required"]
)

final_score = generate_final_score(skill_score, exp_score)

print("Match %:", final_score)
print("Missing Skills:", missing_skills)
