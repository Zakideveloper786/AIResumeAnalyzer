import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Read API Key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found!")

# Configure Gemini
genai.configure(api_key=api_key)

# Load Model
model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are a Senior Technical HR Recruiter.

Analyze the candidate's resume against the given Job Description exactly like an ATS system.

Resume
----------------------------

{resume_text}

----------------------------

Job Description

----------------------------

{job_description}

----------------------------

Instructions

1. Understand the meaning of the resume instead of comparing only keywords.

2. If the Job Description says ".NET Developer", understand that these skills are related:

- C#
- .NET Core
- ASP.NET
- SQL Server
- Web API
- Visual Studio

3. Similarly,

Python Developer means

- Python
- Flask
- FastAPI
- Django
- REST APIs

Cloud means

- AWS
- Azure
- GCP

4. Evaluate

• Technical Skills

• Projects

• Education

• Resume Quality

• Overall Suitability

5. Calculate your own ATS Match Score between 0 and 100.

6. Explain WHY you assigned that score.

7. Extract ALL technical skills from the resume.

8. Return ONLY valid JSON.

Do NOT return markdown.

Do NOT write explanations.

Return exactly this format.

{{
    "match_score": 0,

    "summary": "",

    "technical_skills": [],

    "strengths": [],

    "missing_skills": [],

    "suggestions": [],

    "interview_ready": "",

    "score_reason": ""
}}
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        print("\n========== GEMINI ERROR ==========")
        print(e)
        print("==================================\n")

        return json.dumps({
        "match_score": 0,
        "summary": "Unable to analyze the resume.",
        "technical_skills": [],
        "strengths": [],
        "missing_skills": [],
        "suggestions": [
            "Gemini API Error."
        ],
        "interview_ready": "Unknown",
        "score_reason": str(e)
    })