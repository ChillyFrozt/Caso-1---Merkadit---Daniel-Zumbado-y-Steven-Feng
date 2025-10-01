from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db                     
from ..controllers.products_controller import ProductsController  
from ..schemas import ProductoCreate, ProductoUpdate, ProductoRead
from typing import List 


router = APIRouter()

router = APIRouter()

@router.get("/", response_model=List[ProductoRead])
def list_products(db = Depends(get_db)):
    return ProductsController().list(db)

@router.get("/{product_id}", response_model=ProductoRead)
def get_product(product_id: int, db = Depends(get_db)):
    try:
        return ProductsController().get(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductoCreate, db = Depends(get_db)):
    try:
        return ProductsController().create(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{product_id}", response_model=ProductoRead)
def update_product(product_id: int, payload: ProductoUpdate, db = Depends(get_db)):
    try:
        return ProductsController().update(db, product_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db = Depends(get_db)):
    try:
        ProductsController().delete(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


