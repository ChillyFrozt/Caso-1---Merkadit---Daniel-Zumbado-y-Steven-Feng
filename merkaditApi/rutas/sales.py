from fastapi import APIRouter

router = APIRouter()  # <-- esto es lo que está faltando

@router.get("/test")
def test_sales():
    return {"message": "Sales router funciona"}
