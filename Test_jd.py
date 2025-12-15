from jd_analyzer import parse_job_description

jd_text = """
We are looking for a Backend Developer with 2+ years of experience.
Required skills: Python, Flask, SQL.
Nice to have: Machine Learning, Docker.
"""

jd_data = parse_job_description(jd_text)
print(jd_data)
