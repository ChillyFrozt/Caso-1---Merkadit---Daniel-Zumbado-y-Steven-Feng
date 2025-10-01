from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

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

class RegisterSalePayload(BaseModel):
    productoName: str
    comercioName: str
    cantidad: float
    monto_pagado: float
    medio_pago_name: str
    confirmaciones_pago_json: Optional[Any] = None  # puede ser dict/list
    numeros_referencia_json: Optional[Any] = None
    numero_factura: Optional[int] = None
    cliente: Optional[str] = None
    descuentos_aplic_json: Optional[Any] = None
    usuario_app: Optional[str] = Field(default="apiuser")
    computer: Optional[str] = Field(default="apihost")

class SettleCommercePayload(BaseModel):
    comercioName: str
    localName: Optional[str] = ""
    usuario_app: Optional[str] = Field(default="apiuser")
    computer: Optional[str] = Field(default="apihost")

class SaleIn(BaseModel):
    productoName: str
    comercioName: str
    cantidad: float
    monto_pagado: float
    medio_pago_name: str
    confirmaciones_pago: Optional[List[Dict]] = None
    numeros_referencia: Optional[List[str]] = None
    numero_factura: Optional[str] = None
    cliente: Optional[str] = None
    descuentos_aplic: Optional[Dict] = None
    usuario_app: Optional[str] = "apiuser"
    computer: Optional[str] = "apihost"
