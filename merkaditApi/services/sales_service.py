from ..repositories.products_repository import ProductsRepository
from ..repositories.sales_repository    import SalesRepository


class SalesService:
    def __init__(self, repo: SalesRepository | None = None):
        self.repo = repo or SalesRepository()

    def register_sale(self, db, payload: dict):
        return self.repo.call_register_sale(db, payload)

    def settle_commerce(self, db, payload: dict):
        return self.repo.call_settle_commerce(db, payload)


