import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read API Key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=api_key)

# Load Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_resume(
    resume_text,
    job_description,
    matched,
    missing,
    score
):

    prompt = f"""
You are an experienced HR Recruiter.

Analyze the following resume against the given Job Description.

Resume:
{resume_text}

Job Description:
{job_description}

Matched Skills:
{matched}

Missing Skills:
{missing}

Current Match Score:
{score}%

Instructions:

1. Explain why the candidate received this score.
2. Mention the candidate's strengths.
3. Mention missing skills.
4. Give practical suggestions to improve the resume.
5. Tell whether the candidate is Interview Ready.
6. Return ONLY valid JSON.

Expected JSON Format:

{{
    "match_score": {score},
    "strengths": [],
    "missing_skills": [],
    "suggestions": [],
    "interview_ready": ""
}}
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return str(e)