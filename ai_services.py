import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Read API Key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    )


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are a Senior HR Recruiter and ATS Resume Expert.

Analyze the following resume against the job description.

==========================
RESUME
==========================

{resume_text}

==========================
JOB DESCRIPTION
==========================

{job_description}

==========================

Instructions:

1. Understand the meaning of the resume instead of only matching keywords.
2. Calculate an ATS Match Score (0-100).
3. Write a short professional summary.
4. Extract all technical skills from the resume.
5. Mention strengths.
6. Mention missing skills.
7. Give practical suggestions.
8. Decide whether the candidate is Interview Ready ("Yes" or "No").
9. Explain why the score was assigned.

Return ONLY valid JSON.

JSON Format:

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

Do NOT return markdown.
Do NOT return explanations.
Return ONLY JSON.
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": "You are an ATS Resume Analyzer that always returns valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        print("OpenAI Error:", e)

        return json.dumps(
            {
                "match_score": 0,
                "summary": "Unable to analyze the resume.",
                "technical_skills": [],
                "strengths": [],
                "missing_skills": [],
                "suggestions": [
                    "Unable to contact the AI service."
                ],
                "interview_ready": "Unknown",
                "score_reason": str(e)
            }
        )