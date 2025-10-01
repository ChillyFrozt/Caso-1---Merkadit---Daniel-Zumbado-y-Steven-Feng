from ..services.products_service import ProductsService
from ..services.sales_service  import SalesService


class SalesController:
    def __init__(self, service: SalesService | None = None):
        self.service = service or SalesService()

    def register_sale(self, db, payload: dict):
        return self.service.register_sale(db, payload)

    def settle_commerce(self, db, payload: dict):
        return self.service.settle_commerce(db, payload)
