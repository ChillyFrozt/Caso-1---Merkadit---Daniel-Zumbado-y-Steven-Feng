from fastapi import FastAPI
from rutas import sales, commerce, users, reports, products

app = FastAPI(title="Merkadit API")

app.include_router(sales.router,    prefix="/sales",    tags=["Sales"])
app.include_router(commerce.router, prefix="/commerce", tags=["Commerce"])
app.include_router(users.router,    prefix="/users",    tags=["Users"])
app.include_router(reports.router,  prefix="/reports",  tags=["Reports"])
app.include_router(products.router, prefix="/products", tags=["Products"])

@app.get("/")
def root():
    return {"message": "API Merkadit funcionando"}

import pprint
print(">>> RUTAS REGISTRADAS:")
pprint.pprint([ (r.path, [m for m in r.methods]) for r in app.routes ])
