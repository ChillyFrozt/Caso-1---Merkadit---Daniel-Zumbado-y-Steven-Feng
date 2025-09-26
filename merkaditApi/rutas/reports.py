from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_reports():
    return {"message": "reports router funciona"}