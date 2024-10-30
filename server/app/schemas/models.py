from pydantic import BaseModel

class ResumeRequest(BaseModel):
    resume_text: str
    job_type: str
    job_description: str

class ResumeResponse(BaseModel):
    name: str = None
    email: str = None
    phone: str = None
    skills: list = []
    education: list = []
    experience: list = []
    keywords: list = []
    linkedin: str = None
    github: str = None
    portfolio: str = None
    job_description_keywords: list = []
