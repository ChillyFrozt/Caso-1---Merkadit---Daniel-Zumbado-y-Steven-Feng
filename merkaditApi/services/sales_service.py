
from typing import Any, Dict
from repositories.sales_repository import SalesRepository

class SalesService:
    def __init__(self, repo: SalesRepository | None = None):
        self.repo = repo or SalesRepository

    def register_sale(self, db, payload: Dict[str, Any]):
        for req in ("productoName","comercioName","cantidad","monto_pagado","medio_pago_name"):
            if req not in payload:
                raise ValueError(f"Falta campo requerido: {req}")
        return self.repo.call_register_sale(db, payload)

    def settle_commerce(self, db, payload: Dict[str, Any]):
        if "comercioName" not in payload:
            raise ValueError("Falta comercioName")
        return self.repo.call_settle_commerce(db, payload)
