from typing import Any, Dict

class SalesRepository:
    @staticmethod
    def call_register_sale(db, payload: Dict[str, Any]) -> Dict[str, Any]:
        args = (
            payload["productoName"],
            payload["comercioName"],
            payload["cantidad"],
            payload["monto_pagado"],
            payload["medio_pago_name"],
            payload.get("confirmaciones_pago_json"),
            payload.get("numeros_referencia_json"),
            payload.get("numero_factura"),
            payload.get("cliente"),
            payload.get("descuentos_aplic_json"),
            payload.get("usuario_app", "apiuser"),
            payload.get("computer", "apihost"),
        )
        with db.cursor() as cur:
            cur.callproc("registerSale", args)
        return {"status": "ok"}

    @staticmethod
    def call_settle_commerce(db, payload: Dict[str, Any]) -> Dict[str, Any]:
        args = (
            payload["comercioName"],
            payload.get("localName", ""),
            payload.get("usuario_app", "apiuser"),
            payload.get("computer", "apihost"),
        )
        with db.cursor() as cur:
            cur.callproc("settleCommerce", args)
        return {"status": "ok"}
