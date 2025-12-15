from flask import Flask, render_template, request
from resume_parser import parse_resume
from jd_analyzer import parse_job_description
from match_engine import (
    calculate_skill_match,
    calculate_experience_match,
    generate_final_score
)
from explanation_engine import generate_explanation

import os
app = Flask(__name__, template_folder='index.html', static_folder='static')

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            # Validate inputs
            if "resume" not in request.files:
                error = "Please upload a resume PDF."
                return render_template("index.html", error=error)

            resume_file = request.files["resume"]
            jd_text = request.form.get("jd", "").strip()

            if resume_file.filename == "":
                error = "No resume file selected."
                return render_template("index.html", error=error)

            if not jd_text:
                error = "Job description cannot be empty."
                return render_template("index.html", error=error)

            # Save resume
            resume_path = "uploaded_resume.pdf"
            resume_file.save(resume_path)

            # Parse data
            resume_data = parse_resume(resume_path)
            jd_data = parse_job_description(jd_text)

            # Validate parsed data
            if not resume_data.get("skills"):
                error = "Could not extract skills from resume."
                return render_template("index.html", error=error)

            # Calculate scores
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

            explanation = generate_explanation(
                final_score,
                missing_skills,
                resume_data["experience_years"],
                jd_data["experience_required"]
            )

            result = {
                "score": final_score,
                "missing_skills": missing_skills,
                "explanation": explanation
            }

        except Exception as e:
            error = f"Something went wrong during analysis: {str(e)}"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
