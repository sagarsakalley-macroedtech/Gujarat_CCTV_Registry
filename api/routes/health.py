from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def health_check():

    return {
        "status": "healthy",
        "service": "Gujarat CCTV Registry API",
        "model": "Model 01",
        "message": "API is running successfully"
    }