from fastapi import FastAPI
from rutas import sales, commerce, users, reports


app = FastAPI(title="Merkadit API")

app.include_router(sales.router, prefix= "/sales", tags=["Sales"])
app.include_router(commerce.router, prefix="/commerce", tags=["Commerce"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])

@app.get("/")
def read_root():
    return {"message": "API Merkadit funcionando"}