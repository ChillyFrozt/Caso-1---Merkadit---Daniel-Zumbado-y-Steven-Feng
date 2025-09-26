from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, DECIMAL, VARCHAR, Date, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Facturas(Base):
    _tablename_="facturas"
    facturaid = Column(Integer, primary_key= True,nullable=False, autoincrement= True)
    posttime = Column(DateTime, server_default=func.now(),nullable=False)
    numeroFactura = Column(Integer, nullable=False)
    descuento = Column(DECIMAL(10,2),nullable=False)
    ivaAplicado = Column(DECIMAL(5,2),nullable=False)

class DetallesFactura(Base):
    _tablename_="detallesFactura"
    detalleFacturaid = Column(Integer, primary_key= True,nullable=False, autoincrement= True)
    productoid = Column(Integer, ForeignKey("productos.productoid"),nullable=False)
    cantidad = Column(DECIMAL(10,2), nullable=False)
    subtotal = Column(DECIMAL(12,2),nullable=False)

class Productos(Base):
    _tablename_ ="productos"
    productoid = Column(Integer, primary_key= True, nullable=False, autoincrement= True)
    productoName = Column(VARCHAR(45), nullable=False)
    productoPrecio = Column(DECIMAL(10,2),nullable=False)
    productoCantidad = Column(DECIMAL(10,2),nullable=False)
    fechaLlegada = Column(Date, nullable= False)
    descripcion = Column(VARCHAR(200),nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    comercioid = Column(Integer, ForeignKey("comercios.comercioid"),nullable=False)
    categoriaProductoid = Column(Integer, ForeignKey("categoriaProductos.categoriaProductoid"),nullable=False)
    created_at = Column(DateTime, server_default=func.now(),nullable=False)
    updated_at = Column(DateTime, server_default=func.now(),nullable=False)
    updated_by = Column(Integer, nullable=False)

class EstadoCuentas(Base):
    _tablename_ = "estadoCuentas"
    estadoCuentaid = Column(Integer, primary_key= True, nullable=False, autoincrement= True)
    deleted = Column(Boolean, default=False)

class ContractsCategoriaFee(Base):
    _tablename_ = "contractsCategoriaFee"
    contractid = Column(Integer,primary_key= True, nullable=False, autoincrement= True)
    categoriaProductoid = Column(Integer, ForeignKey("categoriaProductos.categoriaProductoid"))
    fee = Column(DECIMAL(6,4),nullable=False)
    valid_from = Column(Date,nullable=False)
    valid_to = Column(Date, nullable=False)

class Mercados(Base):
    _tablename_ = "mercados"
    mercadoid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    mercadoName = Column(VARCHAR(45), nullable=False)
    mercadoDescripcion = Column(VARCHAR(200), nullable=False)
    mercadoTelefono = Column(VARCHAR(45),nullable=False)
    created_at = Column(DateTime, server_default=func.now(),nullable=False)
    created_by = Column(Integer, nullable=False)
    addressid = Column(Integer, ForeignKey("addresses.addressid"), nullable=False)
    tipoMercado = Column(Integer, ForeignKey("tipoMercados.tipoMercadoid"),nullable=False)
    maxAncho = Column(DECIMAL(8,2), nullable=False)
    maxLargo = Column(DECIMAL(8,2), nullable=False)
    buildingid = Column(Integer,ForeignKey("buildings.buildingid"),nullable=False)

class MercadoUsuarios(Base):
    _tablename_ = "mercadoUsuarios"
    mercadoUsuarioid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    fechaIngreso = Column(DateTime, nullable=False, server_default=func.now)
    fechaSalida = Column (DateTime, nullable=False)
    usuarioid = Column(Integer, ForeignKey("usuarios.usuarioid"),nullable=False)
    rolid = Column(Integer, ForeignKey("roles.rolid"), nullable=False)
    mercadoid = Column(Integer, ForeignKey("mercados.mercadoid"))
