import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# ===== YOUR EXISTING IMPORTS =====
from resume_parser import parse_resume
from jd_analyzer import parse_job_description
from match_engine import (
    calculate_skill_match,
    calculate_experience_match,
    generate_final_score
)
from explanation_engine import generate_explanation

# ===== DATABASE IMPORT =====
from models import db, User

# ===== APP CONFIG =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.secret_key = "super-secret-key"  # change later

# ===== DATABASE CONFIG =====
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ===== LOGIN MANAGER =====
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ===== CREATE DB =====
with app.app_context():
    db.create_all()

# =========================
# 🔐 AUTH ROUTES
# =========================

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        hashed_pw = generate_password_hash(request.form["password"])
        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=hashed_pw,
            role="user"
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# =========================
# 📊 DASHBOARD
# =========================

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "recruiter":
        return render_template("dashboard_recruiter.html")
    elif current_user.role == "admin":
        return "Admin Panel"
    return render_template("dashboard_user.html")

# =========================
# 🧠 RESUME ANALYZER (YOUR CORE)
# =========================

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
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

            resume_path = "uploaded_resume.pdf"
            resume_file.save(resume_path)

            resume_data = parse_resume(resume_path)
            jd_data = parse_job_description(jd_text)

            if not resume_data.get("skills"):
                error = "Could not extract skills from resume."
                return render_template("index.html", error=error)

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

# =========================
# 🚀 RUN
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

