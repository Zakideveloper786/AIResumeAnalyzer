from flask import Flask, render_template, request
import os
import json

from resume_parser import extract_text
from ai_services import analyze_resume

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # ==========================
    # Get Resume & JD
    # ==========================

    resume = request.files["resume"]
    job_description = request.form["job_description"]

    # ==========================
    # Save Resume
    # ==========================

    file_path = os.path.join(
        UPLOAD_FOLDER,
        resume.filename
    )

    resume.save(file_path)

    # ==========================
    # Read Resume
    # ==========================

    resume_text = extract_text(file_path)

    # ==========================
    # Gemini AI Analysis
    # ==========================

    ai_response = analyze_resume(
        resume_text=resume_text,
        job_description=job_description
    )

    # ==========================
    # Delete uploaded file
    # ==========================

    if os.path.exists(file_path):
        os.remove(file_path)

    print("\n========== GEMINI RESPONSE ==========\n")
    print(ai_response)
    print("\n=====================================\n")

    # ==========================
    # Clean JSON
    # ==========================

    cleaned_response = ai_response.strip()

    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response.replace(
            "```json",
            ""
        )

    if cleaned_response.endswith("```"):
        cleaned_response = cleaned_response.replace(
            "```",
            ""
        )

    cleaned_response = cleaned_response.strip()

    # ==========================
    # Parse JSON
    # ==========================

    try:

        ai_data = json.loads(cleaned_response)
        ai_data.setdefault("match_score", 0)
        ai_data.setdefault("summary", "No summary generated.")
        ai_data.setdefault("technical_skills", [])
        ai_data.setdefault("strengths", [])
        ai_data.setdefault("missing_skills", [])
        ai_data.setdefault("suggestions", [])
        ai_data.setdefault("interview_ready", "Unknown")
        ai_data.setdefault("score_reason", "No explanation available.")

    except Exception as e:

        print("JSON Parsing Error:", e)

        ai_data = {}

    # ==========================
    # Default Values
    # ==========================

    ai_data.setdefault("match_score", 0)

    ai_data.setdefault(
        "summary",
        "No summary generated."
    )

    ai_data.setdefault(
        "technical_skills",
        []
    )

    ai_data.setdefault(
        "strengths",
        []
    )

    ai_data.setdefault(
        "missing_skills",
        []
    )

    ai_data.setdefault(
        "suggestions",
        []
    )

    ai_data.setdefault(
        "interview_ready",
        "Unknown"
    )

    ai_data.setdefault(
        "score_reason",
        "No explanation available."
    )

    # ==========================
    # Render Result
    # ==========================

    return render_template(

        "result.html",

        ai_data=ai_data

    )


if __name__ == "__main__":
    app.run(debug=True)