from fastapi import APIRouter
from app.utils.functions import metrics1


# Create an instance of APIRouter
router = APIRouter()


@router.get("/metrics")
def metrics():
    return metrics1()
