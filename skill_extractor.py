KNOWN_SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "SQL",
    "SQL Server",
    "MySQL",
    "PostgreSQL",
    "FastAPI",
    "Flask",
    "Django",
    "React",
    "Flutter",
    ".NET",
    ".NET Core",
    "AWS",
    "Docker",
    "Kubernetes",
    "Git",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Deep Learning",
    "HTML",
    "CSS",
    "JavaScript"
]


def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in KNOWN_SKILLS:

        if skill.lower() in text:

            found_skills.append(skill)

    return found_skills