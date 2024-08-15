import spacy
import pandas as pd
import re


nlp = spacy.load("en_core_web_sm")

def parse_resume(resume_text, job_type, job_description):

    job_type = job_type.strip()

 
    swe_csv_path = "data/SWE.csv"
    business_csv_path = "data/Business.csv"

    skills = []

    if job_type == "SWE":
        skills = pd.read_csv(swe_csv_path).iloc[:, 0].tolist()  
    elif job_type == "Business":
        skills = pd.read_csv(business_csv_path).iloc[:, 0].tolist()  

    parsed_data = {
        "name": None,
        "email": None,
        "phone": None,
        "skills": [],
        "education": [],
        "experience": [],
        "keywords": [],  
        "linkedin": None,
        "github": None,
        "portfolio": None,
        "job_description_keywords": [] 
    }

    doc = nlp(resume_text)
    job_doc = nlp(job_description)

    for ent in doc.ents:
        if ent.label_ == "PERSON" and not parsed_data["name"]:
            parsed_data["name"] = ent.text

    for token in doc:
        if token.like_email:
            parsed_data["email"] = token.text

    for token in doc:
        if token.like_num and len(token.text) >= 10:
            parsed_data["phone"] = token.text

    for token in doc:
        if token.text.lower() in [skill.lower() for skill in skills]: 
            parsed_data["skills"].append(token.text)

    degrees = ["BSc", "MSc", "PhD", "Bachelor", "Master", "Doctorate"]
    for ent in doc.ents:
        if ent.label_ in ["ORG", "GPE"]:
            if any(degree in ent.text for degree in degrees):
                parsed_data["education"].append(ent.text)
        elif ent.label_ in ["PERSON", "ORG", "GPE"] and ent.text not in parsed_data["education"]:
            parsed_data["education"].append(ent.text)

    for ent in doc.ents:
        if ent.label_ in ["ORG", "GPE"]:
            parsed_data["experience"].append(ent.text)

    job_keywords = ["development", "leadership", "management"]
    for token in doc:
        if token.text.lower() in job_keywords:
            parsed_data["keywords"].append(token.text.lower())

    linkedin_pattern = re.compile(r'https?://(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?')
    github_pattern = re.compile(r'https?://(www\.)?github\.com/[A-Za-z0-9_-]+/?')
    portfolio_pattern = re.compile(r'https?://[A-Za-z0-9_-]+\.[A-Za-z]{2,}/?')

    for token in doc:
        url = token.text
        if re.match(linkedin_pattern, url):
            parsed_data["linkedin"] = url
        elif re.match(github_pattern, url):
            parsed_data["github"] = url
        elif re.match(portfolio_pattern, url) and not re.match(linkedin_pattern, url) and not re.match(github_pattern, url):
            parsed_data["portfolio"] = url

    for token in job_doc:
        if token.is_alpha and len(token.text) > 2:  
            parsed_data["job_description_keywords"].append(token.text.lower())

    return parsed_data
