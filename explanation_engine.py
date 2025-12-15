def generate_explanation(final_score, missing_skills, resume_exp, jd_exp):
    explanation = []

    if final_score >= 80:
        explanation.append("Strong match for the role with most required skills satisfied.")
    elif final_score >= 60:
        explanation.append("Moderate match. Some key areas need improvement.")
    else:
        explanation.append("Low match. Significant skill gaps detected.")

    if missing_skills:
        explanation.append(
            f"Missing required skills: {', '.join(missing_skills)}."
        )

    if resume_exp < jd_exp:
        explanation.append(
            f"Experience gap: Required {jd_exp} years, but resume shows {resume_exp} year(s)."
        )

    explanation.append("Improving the missing skills and adding measurable achievements can increase the match score.")

    return " ".join(explanation)
