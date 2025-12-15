from explanation_engine import generate_explanation

final_score = 67.5
missing_skills = ["flask"]
resume_exp = 1
jd_exp = 2

result = generate_explanation(final_score, missing_skills, resume_exp, jd_exp)
print(result)

