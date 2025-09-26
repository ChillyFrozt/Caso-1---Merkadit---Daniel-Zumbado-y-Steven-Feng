# merkaditApi/controllers/products_controller.py
print(">> Cargando controllers/products_controller.py")  # debug

from services.products_service import ProductsService
from schemas import ProductoCreate, ProductoUpdate

class ProductsController:
    def __init__(self, service: ProductsService | None = None):
        self.service = service or ProductsService()

    def list(self, db):
        return self.service.list_products(db)

    def get(self, db, product_id: int):
        return self.service.get_product(db, product_id)

    def create(self, db, payload: ProductoCreate):
        return self.service.create_product(db, payload.model_dump())

    def update(self, db, product_id: int, payload: ProductoUpdate):
        return self.service.update_product(db, product_id, payload.model_dump(exclude_unset=True))

    def delete(self, db, product_id: int):
        return self.service.delete_product(db, product_id)
