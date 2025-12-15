from resume_parser import parse_resume

print("Starting resume parsing...")

resume_data = parse_resume("sample resume.pdf")

print("Parsing completed.")
print(resume_data)
