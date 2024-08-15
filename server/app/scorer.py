import pandas as pd
import os

def load_keywords(job_type):
    """Load keywords from the relevant CSV file based on the job type."""
    if job_type == "SWE":
        file_path = "data/SWE.csv"
    elif job_type == "Business":
        file_path = "data/Business.csv"
    else:
        return []

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df.iloc[:, 0].tolist()  
    else:
        return []

def score_resume(resume_data, job_description, job_type):
    weights = {
        "skills": 40,
        "experience": 30,
        "education": 20,
        "keywords": 10
    }
    
    score = 0

    required_skills = load_keywords(job_type)
    skills_score = sum([1 for skill in resume_data["skills"] if skill.lower() in map(str.lower, required_skills)])
    max_skills_score = len(required_skills)
    if max_skills_score > 0:
        score += (skills_score / max_skills_score) * weights["skills"]

    experience_score = sum([1 for exp in resume_data["experience"] if any(kw.lower() in exp.lower() for kw in required_skills)])
    max_experience_score = 5  
    if max_experience_score > 0:
        score += min(experience_score, max_experience_score) / max_experience_score * weights["experience"]

    required_education = ["BSc", "MSc", "PhD"]
    education_score = sum([1 for edu in resume_data["education"] if any(req.lower() in edu.lower() for req in required_education)])
    max_education_score = len(required_education)
    if max_education_score > 0:
        score += (education_score / max_education_score) * weights["education"]

    job_keywords = load_keywords(job_type)  
    keyword_score = sum([1 for keyword in resume_data["keywords"] if keyword.lower() in map(str.lower, job_keywords)])
    max_keyword_score = len(job_keywords)
    if max_keyword_score > 0:
        score += (keyword_score / max_keyword_score) * weights["keywords"]

    final_score = min(max(score, 0), 100)

    return final_score
