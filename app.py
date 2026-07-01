from flask import Flask, render_template, request
import os

from resume_parser import extract_text
from skill_extractor import extract_skills
from matcher import compare_skills
from ai_services import analyze_resume

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # Get uploaded resume
    resume = request.files["resume"]

    # Get Job Description
    job_description = request.form["job_description"]

    # Save uploaded resume
    file_path = os.path.join(UPLOAD_FOLDER, resume.filename)
    resume.save(file_path)

    # ==========================
    # Read Resume
    # ==========================

    resume_text = extract_text(file_path)

    # ==========================
    # Extract Skills
    # ==========================

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    # ==========================
    # Compare Skills
    # ==========================

    result = compare_skills(
        resume_skills,
        jd_skills
    )

    # ==========================
    # AI Analysis
    # ==========================

    ai_response = analyze_resume(
        resume_text=resume_text,
        job_description=job_description,
        matched=result["matched"],
        missing=result["missing"],
        score=result["score"]
    )

    # Delete uploaded resume
    os.remove(file_path)

    # Print in terminal (for debugging)
    print("\n========== RESUME SKILLS ==========")
    print(resume_skills)

    print("\n========== JD SKILLS ==========")
    print(jd_skills)

    print("\n========== MATCH RESULT ==========")
    print(result)

    print("\n========== AI RESPONSE ==========")
    print(ai_response)

    # Clean and parse AI response if possible
    import json
    ai_data = None
    cleaned_response = ai_response.strip()
    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response[7:]
    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response[:-3]
    cleaned_response = cleaned_response.strip()

    try:
        ai_data = json.loads(cleaned_response)
    except Exception as e:
        print(f"Error parsing AI response JSON: {e}")
        ai_data = {
            "match_score": result["score"],
            "strengths": ["Could not parse structured strengths automatically."],
            "missing_skills": result["missing"],
            "suggestions": ["Could not parse structured suggestions automatically."],
            "interview_ready": "Please review the raw AI feedback below."
        }

    # Send data to HTML page
    return render_template(
        "result.html",
        score=result["score"],
        matched=result["matched"],
        missing=result["missing"],
        ai_response=ai_response,
        ai_data=ai_data
    )


if __name__ == "__main__":
    app.run(debug=True)