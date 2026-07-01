from fastapi import FastAPI, UploadFile, File, Form
from resume_parser import extract_text
from skill_extractor import extract_skills
from matcher import compare_skills
from ai_services import analyze_resume

import shutil
import os

app = FastAPI()

# Create uploads folder if it doesn't exist
os.makedirs("uploads", exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Resume Analyzer"
    }


@app.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # Save uploaded resume
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract Resume Text
    resume_text = extract_text(file_path)

    # Extract Skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    # Compare Skills
    result = compare_skills(
        resume_skills,
        jd_skills
    )

    # AI Analysis using Gemini
    ai_response = analyze_resume(
        resume_text=resume_text,
        job_description=job_description,
        matched=result["matched"],
        missing=result["missing"],
        score=result["score"]
    )

    # Delete uploaded resume
    os.remove(file_path)

    # Print everything in terminal
    print("\n========== RESUME TEXT ==========\n")
    print(resume_text)

    print("\n========== RESUME SKILLS ==========\n")
    print(resume_skills)

    print("\n========== JD SKILLS ==========\n")
    print(jd_skills)

    print("\n========== MATCH RESULT ==========\n")
    print(result)

    print("\n========== AI RESPONSE ==========\n")
    print(ai_response)

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": result["matched"],
        "missing_skills": result["missing"],
        "match_score": result["score"],
        "ai_analysis": ai_response
    }