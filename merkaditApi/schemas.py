
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ProductoBase(BaseModel):
    productoName: Optional[str] = None
    productoPrecio: Optional[float] = None
    productoCantidad: Optional[float] = None
    fechaLlegada: Optional[date] = None
    descripcion: Optional[str] = None
    comercioid: Optional[int] = None
    categoriaProductoid: Optional[int] = None
    updated_by: Optional[int] = None
    enabled: Optional[bool] = True
    deleted: Optional[bool] = False

class ProductoCreate(ProductoBase):
    productoName: str
    productoPrecio: float
    productoCantidad: float
    fechaLlegada: date
    descripcion: str
    comercioid: int
    categoriaProductoid: int
    updated_by: int

class ProductoUpdate(ProductoBase):
    pass  

class ProductoRead(ProductoBase):
    productoid: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class SaleIn(BaseModel):
    nombreProducto: str
    nombreTienda: str
    cantidad: float
    cantidadPagada: float
    metodoPago: str
    confirmacionesPago: str
    numeroReferencia: str
    numerFactura: int
    cliente: str
    descuentoAplicado: Optional[float] = 0.0