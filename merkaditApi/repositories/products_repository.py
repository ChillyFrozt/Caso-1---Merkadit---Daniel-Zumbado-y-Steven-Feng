# merkaditApi/repositories/products_repository.py
print(">> Cargando repositories/products_repository.py")  # debug

from typing import List, Optional, Dict, Any

class ProductsRepository:
    @staticmethod
    def get_all(db) -> List[Dict[str, Any]]:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM productos WHERE deleted = 0;")
            return cur.fetchall()

    @staticmethod
    def get_by_id(db, product_id: int) -> Optional[Dict[str, Any]]:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM productos WHERE productoid = %s AND deleted = 0;", (product_id,))
            return cur.fetchone()

    @staticmethod
    def create(db, data: Dict[str, Any]) -> Dict[str, Any]:
        with db.cursor() as cur:
            cur.execute("""
                INSERT INTO productos
                (productoName, productoPrecio, productoCantidad, fechaLlegada, descripcion,
                 comercioid, categoriaProductoid, updated_by, enabled, deleted)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """, (
                data["productoName"], data["productoPrecio"], data["productoCantidad"],
                data["fechaLlegada"], data["descripcion"], data["comercioid"],
                data["categoriaProductoid"], data["updated_by"],
                data.get("enabled", True), data.get("deleted", False),
            ))
            new_id = cur.lastrowid
        return ProductsRepository.get_by_id(db, new_id)

    @staticmethod
    def update(db, product_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not data:
            return ProductsRepository.get_by_id(db, product_id)
        fields = []
        values = []
        for k, v in data.items():
            fields.append(f"{k} = %s")
            values.append(v)
        values.append(product_id)
        set_clause = ", ".join(fields)
        sql = f"UPDATE productos SET {set_clause}, updated_at = NOW() WHERE productoid = %s AND deleted = 0;"
        with db.cursor() as cur:
            cur.execute(sql, tuple(values))
        return ProductsRepository.get_by_id(db, product_id)

    @staticmethod
    def delete(db, product_id: int) -> bool:
        with db.cursor() as cur:
            cur.execute("UPDATE productos SET deleted = 1 WHERE productoid = %s AND deleted = 0;", (product_id,))
            return cur.rowcount > 0
