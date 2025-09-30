from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, DECIMAL, VARCHAR, Date, Boolean, VARBINARY
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Owners(Base):
    __tablename__ = "owners"
    ownerid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    usuarioid = Column(Integer, ForeignKey("usuarios.usuarioid"), nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)

class MetodosDePago(Base):
    __tablename__ = "metodosDePago"
    metodoDePagoid = Column(Integer,primary_key=True, autoincrement=True, nullable=False)
    metodoDePagoName = Column(VARCHAR(45), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

class Facturas(Base):
    __tablename__="facturas"
    facturaid = Column(Integer, primary_key= True,nullable=False, autoincrement= True)
    posttime = Column(DateTime, server_default=func.now(),nullable=False)
    numeroFactura = Column(Integer, nullable=False)
    descuento = Column(DECIMAL(10,2),nullable=False)
    ivaTotal = Column(DECIMAL(12,2),nullable=False)
    metodoDePagoid = Column(Integer, ForeignKey("metodosDePago.metodoDePagoid"))
    usuarioid = Column(Integer,ForeignKey("usuarios.usuarioid"),nullable=False)
    subtotal = Column(DECIMAL(12,2),nullable=False)
    created_at = Column(DateTime,nullable=False)
    updated_at = Column(DateTime, nullable=False)
    comercioid = Column(Integer,ForeignKey("comercios.comercioid"), nullable=False)


class DetallesFactura(Base):
    __tablename__="detallesFactura"
    detalleFacturaid = Column(Integer, primary_key= True,nullable=False, autoincrement= True)
    facturaid = Column(Integer, ForeignKey("facturas.facturaid"), nullable=False)
    productoid = Column(Integer, ForeignKey("productos.productoid"),nullable=False)
    cantidad = Column(DECIMAL(10,2), nullable=False)
    subtotal = Column(DECIMAL(12,2),nullable=False)
    precioUnitario = Column(DECIMAL(12,2), nullable=False)
    deleted = Column(Boolean,default=False,nullable=False)
    ivaAplicado = Column(DECIMAL(12,2), nullable=False)

class Productos(Base):
    __tablename__ ="productos"
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
    __tablename__ = "estadoCuentas"
    estadoCuentaid = Column(Integer, primary_key= True, nullable=False, autoincrement= True)
    deleted = Column(Boolean, default=False)

class ContractsCategoriaFee(Base):
    __tablename__ = "contractsCategoriaFee"
    contractid = Column(Integer,primary_key= True, nullable=False, autoincrement= True)
    categoriaProductoid = Column(Integer, ForeignKey("categoriaProductos.categoriaProductoid"))
    fee = Column(DECIMAL(6,4),nullable=False)
    valid_from = Column(Date,nullable=False)
    valid_to = Column(Date, nullable=False)

class Mercados(Base):
    __tablename__ = "mercados"
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
    __tablename__ = "mercadoUsuarios"
    mercadoUsuarioid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    fechaIngreso = Column(DateTime, nullable=False, server_default=func.now())
    fechaSalida = Column (DateTime, nullable=False)
    usuarioid = Column(Integer, ForeignKey("usuarios.usuarioid"),nullable=False)
    rolid = Column(Integer, ForeignKey("roles.rolid"), nullable=False)
    mercadoid = Column(Integer, ForeignKey("mercados.mercadoid"))

class TipoTransacciones(Base):
    __tablename__ = "tipoTransacciones"
    tipoTransaccionid = Column(Integer,primary_key=True,autoincrement=True, nullable=False)
    tipoTransaccionName = Column(VARCHAR(100),nullable=False)
    deleted = Column(Boolean, default=False,nullable=False)

class Transacciones(Base):
    __tablename__ = "transacciones"
    transaccionid = Column(Integer, primary_key=True,autoincrement=True, nullable=False)
    tipoTransaccion = Column(Integer, ForeignKey("tipoTransacciones.tipoTransaccionid"))
    comercioid = Column(Integer, ForeignKey("comercios.comercioid"))
    monto = Column(DECIMAL(12,2),nullable=False)
    descripcion = Column(VARCHAR(200), nullable=False)
    posttime = Column(DateTime,nullable=False)
    deleted = Column(Boolean, default=False,nullable=False)

class PrecioProductos(Base):
    __tablename__ = "precioProductos"
    precioProductoid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    precio = Column(DECIMAL(10,2), nullable=False)
    posttime = Column(DateTime,nullable=False)
    productoid = Column(Integer, ForeignKey("productos.productoid"), nullable=False)

class Buildings(Base):
    __tablename__ = "buildings"
    buildingid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    buildingName = Column(VARCHAR(100), nullable=False)
    addressid = Column(Integer, ForeignKey("addresses.addressid"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=False)
    maxAncho = Column(DECIMAL(8,2), nullable=False)
    maxLargo = Column(DECIMAL(8,2), nullable=False)

class MercadoPorBuildings(Base):
    __tablename__ = "mercadoPorBuilding"
    mercadoPorBuildingsid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    mercadoid = Column(Integer, ForeignKey("mercados.mercadoid"))
    buildingid = Column(Integer, ForeignKey("buildings.buildingid"))
    deleted = Column(Boolean, default=False, nullable=False)
    postTime = Column(DateTime, nullable=False)

class Usuarios(Base):
    __tablename__ = "usuarios"
    usuarioid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    usuarioName = Column(VARCHAR(45), nullable=False)
    usuarioPassword = VARBINARY(128)
    enabled = Column(Boolean, nullable=False, default=True)
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Inversiones(Base):
    __tablename__ = "inversiones"
    inversionid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    buildingid = Column(Integer, ForeignKey("buildings.buildingid"), nullable=False)
    descripcion = Column(VARCHAR(100),nullable=False)
    posttime = Column(DateTime, nullable=False)
    monto = Column(DECIMAL(12,2), nullable=False)

class Comercios(Base):
    __tablename__ = "comercios"
    comercioid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer,nullable=False)
    tipoComercio = Column(Integer, ForeignKey("tipoComercios.tipoComercioid"), nullable=False)
    cedulaJuridica = Column(Integer, nullable=False)
    razonSocial = Column(Integer, nullable=False)
    contractid = Column(Integer, ForeignKey("contracts.contractid"))
    deleted = Column(Boolean, default=False, nullable=False)
    estadoComercio = Column(Integer, ForeignKey("estadoComercios.estadoComercioid"))

class EstadoComercio(Base):
    __tablename__ = "estadoComercios"
    estadoComercioid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    estadoComercioName = Column(VARCHAR(100), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

class TipoComercios(Base):
    __tablename__ = "tipoComercios"
    tipoComercioid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    tipoComercioName = Column(VARCHAR(45), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)


class comercioUsuarios(Base):
    __tablename__ = "comercioUsuarios"
    comercioUsuarioid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    fechaIngreso = Column(DateTime, nullable=False)
    fechaSalida = Column(DateTime, nullable=True)
    comercioid = Column(Integer, ForeignKey("comercios.comercioid"),nullable=False)
    rolid = Column(Integer, ForeignKey("roles.rolid"),nullable=False)
    usuarioid = Column(Integer, ForeignKey("usuarios.usuarioid"), nullable=False)
    comercio = relationship("Comercios",back_populates="usuarios")
    usuario = relationship("Usuario", back_populates="comercios")
    deleted = Column(Boolean, default=False, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

class UsuarioPorRol(Base):
    __tablename__ = "usuarioPorRol"
    usuarioPorRolid = Column(Integer,primary_key=True, nullable=False, autoincrement=True)
    rolid = Column(Integer, ForeignKey("roles.rolid"), nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date, nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)

class TipoMercados(Base):
    __tablename__ = "tipoMercados"
    tipoMercadoid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    tipoMercadoName = Column(VARCHAR(45), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

class CategoriaKiokos(Base):
    __tablename__ = "categoriaKioskos"
    categoriaKioskoid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    categoriaKioskoName = Column(VARCHAR(45), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)

class TipoKioskos(Base):
    __tablename__ = "tipoKioskos"
    tipoKioskoid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    tipoKioskoName = Column(VARCHAR(45), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

class Kioskos(Base):
    __tablename__ = "kioskos"
    kioskoid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    kioskoCost = Column(DECIMAL(12,2), nullable=False)
    categoriaKioskoid = Column(Integer, ForeignKey("categoriaKioskos.categoriaKioskoid"), nullable=False)
    estadoKioskoid = Column(Integer, ForeignKey("estadoKioskos.estadoKioskoid"), nullable=False)
    tipoKioskoid = Column(Integer,ForeignKey("tipoKioskos.tipoKioskoid"), nullable=False)
    ancho = Column(DECIMAL(6,2), nullable=False)
    largo = Column(DECIMAL(6,2), nullable=False)
    created_at = Column(DateTime, nullable=False)
    mercadoid = Column(Integer, ForeignKey("mercados.mercadoid"), nullable=False)

class PermisoPorRol(Base):
    __tablename__ = "permisoPorRol"
    permisoPorRolid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    rolid = Column(Integer, ForeignKey("roles.rolid"), nullable=False)
    permisoid = Column(Integer, ForeignKey("permisos.permisoid"), nullable=False)
    created_at = Column(DateTime,nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime)

class Permisos(Base):
    __tablename__ = "permisos"
    permisoid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombrePermiso = Column(VARCHAR(45), nullable=False) 
    codigo = Column(VARCHAR(45), nullable=False)

class Roles(Base):
    __tablename__ = "roles"
    rolid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombreRol = Column(VARCHAR(45), nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Contracts(Base):
    __tablename__ = "contracts"
    contractid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    posttime = Column(DateTime, nullable=False)
    fechaCobro = Column(DateTime, nullable=False)
    montoBase = Column(DECIMAL(12,2), nullable=False)
    fechaFinal = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, nullable=False)
    kioskoid = Column(Integer, ForeignKey("kioskos.kioskoid"), nullable=False)
    ownerid = Column(Integer, ForeignKey("owners.ownerid"), nullable=False)
    comercioid = Column(Integer, ForeignKey("comercios.comercioid"), nullable=False)

class ContractsKioskos(Base):
    __tablename__ = "contractsKioskos"
    contractKiosko = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    contractid = Column(Integer, ForeignKey("contracts.contractid"))
    kioskoid = Column(Integer, ForeignKey("kioskos.kioskoid"), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    posttime = Column(DateTime, nullable=False)

class PermisoPorUsuraio(Base):
    __tablename__ = "permisoPorUsuario"
    permisoPorUusarioid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    permisoid = Column(Integer, ForeignKey("permisos.permisoid"), nullable=False)
    usuarioid = Column(Integer, ForeignKey("usuarios.usuarioid"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    postTime = Column(DateTime, nullable=False)

class Addresses(Base):
    __tablename__ = "addresses"
    addressid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    addressName = Column(VARCHAR(150), nullable=False)
    cityid = Column(Integer, ForeignKey("cities.cityid"), nullable=False)
    geolocation = Column(Geometry(geometry_type='POINT', srid = 4326), nullable=False)
    codigoPostal = Column(VARCHAR(20), nullable=False)
    direccion1 = Column(VARCHAR(45), nullable=False)
    direccion2 = Column(VARCHAR(45))
    deleted = Column(Boolean,default=False, nullable=False)
    postTime = Column(DateTime, nullable=False)

class Cities(Base):
    __tablename__ = "cities"
    cityid = Column(Integer, primary_key= True, autoincrement=True, nullable=False)
    cityName = Column(VARCHAR(100), nullable=False)
    statedid = Column(Integer, ForeignKey("states.stateid"))

class States(Base):
    __tablename__ = "states"
    stateid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    stateName = Column(VARCHAR(100), nullable=False)
    countryid = Column(Integer, ForeignKey("countries.countryid"), nullable=False)

class Countries(Base):
    __tablename__ = "countries"
    countryid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    countryName = Column(VARCHAR(100), nullable=False)



class EstadoKioskos(Base):
    __tablename__ = "estadoKioskos"
    estadoKioskoid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    estadoKioskoName = Column(VARCHAR(45), nullable=False)

class CategoriaProductos(Base):
    __tablename__ = "categoriaProductos"
    categoriaProductoid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    categoriaProductoName = Column(VARCHAR(45), nullable=False)
    categoriaProductoDescripcion = Column(VARCHAR(200), nullable=False)