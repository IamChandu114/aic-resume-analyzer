def calculate_skill_match(resume_skills, jd_required, jd_preferred):
    resume_skills = set(resume_skills)
    required = set(jd_required)
    preferred = set(jd_preferred)

    required_match = resume_skills.intersection(required)
    preferred_match = resume_skills.intersection(preferred)

    required_score = len(required_match) / max(len(required), 1)
    preferred_score = len(preferred_match) / max(len(preferred), 1)

    skill_score = (0.8 * required_score) + (0.2 * preferred_score)
    return skill_score, list(required - required_match)


def calculate_experience_match(resume_exp, jd_exp):
    if jd_exp == 0:
        return 1.0
    return min(resume_exp / jd_exp, 1.0)


def generate_final_score(skill_score, exp_score):
    return round((skill_score * 0.6 + exp_score * 0.25) * 100, 2)
