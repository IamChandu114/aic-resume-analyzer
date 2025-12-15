import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_feedback(resume_skills, jd_skills, score):
    prompt = f"""
You are an AI career coach.

Resume Skills: {resume_skills}
Job Required Skills: {jd_skills}
Match Score: {score}%

Explain:
1. Why this score occurred
2. What skills are missing
3. How to improve resume for better shortlisting
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response.choices[0].message.content
