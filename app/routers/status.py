from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/status")
def get_status():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0"
    }
