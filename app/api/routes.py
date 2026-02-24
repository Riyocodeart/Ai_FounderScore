from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_route():
    return {"message": "API working"}

from app.schemas.request_schema import StartupInput

@router.post("/analyze")
def analyze_startup(data: StartupInput):
    return {
        "message": "Received",
        "idea": data.idea_description
    }