from fastapi import FastAPI
from .rutas import sales, commerce, users, reports, products, sales_sp
from fastapi import APIRouter, HTTPException
import json
from .database import db_cursor
from .schemas import SaleIn


router = APIRouter()
app = FastAPI(title="Merkadit API")

app.include_router(sales.router,    prefix="/sales",    tags=["Sales"])
app.include_router(commerce.router, prefix="/commerce", tags=["Commerce"])
app.include_router(users.router,    prefix="/users",    tags=["Users"])
app.include_router(reports.router,  prefix="/reports",  tags=["Reports"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(sales_sp.router, tags=["Settlements & Sales SP"])

@app.get("/")
def root():
    return {"message": "API Merkadit funcionando"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

import pprint
print(">>> RUTAS REGISTRADAS:")
pprint.pprint([ (r.path, [m for m in r.methods]) for r in app.routes ])

@router.post("/register-sale")
def register_sale(sale: SaleIn):
    try:
        with db_cursor() as (conn, cursor):
            cursor.execute(
                """
                CALL registerSale(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    sale.productoName,
                    sale.comercioName,
                    sale.cantidad,
                    sale.monto_pagado,
                    sale.medio_pago_name,
                    json.dumps(sale.confirmaciones_pago),
                    json.dumps(sale.numeros_referencia),
                    sale.numero_factura,
                    sale.cliente,  
                    json.dumps(sale.descuentos_aplic) if sale.descuentos_aplic else None
                )
            )
            result = cursor.fetchone()  
            return {"status": "success", "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))