from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_sales():
    return {"message": "Sales router funciona"}