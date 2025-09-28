from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from controllers.sales_controller import SalesController

router = APIRouter()

@router.post("/sales/register")
def register_sale(payload: dict, db = Depends(get_db)):
    try:
        return SalesController().register_sale(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/commerce/settle")
def settle_commerce(payload: dict, db = Depends(get_db)):
    try:
        return SalesController().settle_commerce(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
