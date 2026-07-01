def compare_skills(resume_skills, jd_skills):

    matched = []
    missing = []

    # Compare Resume Skills with JD Skills
    for skill in jd_skills:

        if skill in resume_skills:
            matched.append(skill)

        else:
            missing.append(skill)

    # Prevent division by zero
    if len(jd_skills) == 0:
        score = 0

    else:
        score = (len(matched) / len(jd_skills)) * 100

    return {
        "matched": matched,
        "missing": missing,
        "score": round(score, 2)
    }