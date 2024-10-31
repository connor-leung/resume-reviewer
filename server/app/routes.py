from fastapi import APIRouter, HTTPException
from app.services.parser import parse_resume
from app.services.scorer import score_resume
from app.schemas.models import ResumeRequest, ResumeResponse

router = APIRouter()

@router.get("/status")
async def get_status():
    return {"status": "API is running"}

@router.post("/parse_resume", response_model=ResumeResponse)
async def parse_resume_endpoint(request: ResumeRequest):
    try:
        parsed_data = parse_resume(request.resume_text, request.job_type, request.job_description)
        return parsed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/score")
async def score_endpoint(data: dict):
    try:
        score = score_resume(data)
        return {"score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
