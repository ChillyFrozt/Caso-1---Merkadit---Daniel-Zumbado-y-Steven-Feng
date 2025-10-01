from typing import List, Dict, Any
from ..repositories.products_repository import ProductsRepository
from ..repositories.sales_repository    import SalesRepository


class ProductsService:
    def __init__(self, repo: ProductsRepository | None = None):
        self.repo = repo or ProductsRepository

    def list_products(self, db) -> List[Dict[str, Any]]:
        return self.repo.get_all(db)

    def get_product(self, db, product_id: int) -> Dict[str, Any]:
        row = self.repo.get_by_id(db, product_id)
        if not row:
            raise ValueError("Producto no encontrado")
        return row

    def create_product(self, db, data: Dict[str, Any]) -> Dict[str, Any]:
        if data.get("productoPrecio", 0) < 0:
            raise ValueError("precio inválido")
        if data.get("productoCantidad", 0) < 0:
            raise ValueError("cantidad inválida")
        return self.repo.create(db, data)

    def update_product(self, db, product_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        if "productoPrecio" in data and data["productoPrecio"] is not None and data["productoPrecio"] < 0:
            raise ValueError("precio inválido")
        if "productoCantidad" in data and data["productoCantidad"] is not None and data["productoCantidad"] < 0:
            raise ValueError("cantidad inválida")
        row = self.repo.update(db, product_id, data)
        if not row:
            raise ValueError("Producto no encontrado")
        return row

    def delete_product(self, db, product_id: int) -> None:
        ok = self.repo.delete(db, product_id)
        if not ok:
            raise ValueError("Producto no encontrado o ya eliminado")
