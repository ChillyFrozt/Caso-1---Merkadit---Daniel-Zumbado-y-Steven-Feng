from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, DECIMAL, VARCHAR, Date, Boolean, VARBINARY
from geoalchemy2 import Geometry
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

class GastosOperativos(Base):
    _tablename_ = "gastosOperativos"
    gastoOperativoid = Column(Integer, primary_key= True, autoincrement=True, nullable=False)
    monto = Column(DECIMAL(12,2), nullable=False)
    posttime = Column(DateTime, nullable=False)
    buildingid = Column(Integer, ForeignKey("buildings.buildingid"), nullable=False)

class PrecioProductos(Base):
    _tablename_ = "precioProductos"
    precioProductoid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    precio = Column(DECIMAL(10,2), nullable=False)
    posttime = Column(DateTime,nullable=False)
    productoid = Column(Integer, ForeignKey("productos.productoid"), nullable=False)

class Buildings(Base):
    _tablename_ = "buildings"
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
    _tablename_ = "mercadoPorBuilding"
    mercadoid = Column(Integer, ForeignKey("mercados.mercadoid"))
    buildingid = Column(Integer, ForeignKey("buildings.buildingid"))

class Usuarios(Base):
    _tablename_ = "usuarios"
    usuarioid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    usuarioName = Column(VARCHAR(45), nullable=False)
    usuarioPassword = VARBINARY(128)
    enabled = Column(Boolean, nullable=False, default=True)
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Owner(Base):
    _tablename_ = "owner"
    ownerid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    usuarioid = Column(Integer, ForeignKey("usuarios.usuarioid"), nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)

class Inversiones(Base):
    _tablename_ = "inversiones"
    inversionid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    buildingid = Column(Integer, ForeignKey("buildings.buildingid"), nullable=False)
    descripcion = Column(VARCHAR(100),nullable=False)
    posttime = Column(DateTime, nullable=False)
    monto = Column(DECIMAL(12,2), nullable=False)

class Comercios(Base):
    _tablename_ = "comercios"
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
    _tablename_ = "estadoComercios"
    estadoComercioid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    estadoComercioName = Column(VARCHAR)
    deleted = Column(Boolean, default=False, nullable=False)

class TipoComercios(Base):
    _tablename_ = "tipoComercios"
    tipoComercioid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    tipoComercioName = Column(VARCHAR(45), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

class OwnerPorComercios(Base):
    _tablename_ = "ownerPorComercios"
    ownerPorComercioid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    comercioid = Column(Integer, ForeignKey("comercios.comercioid"), nullable=False)
    ownerid = Column(Integer, ForeignKey("owners.ownerid"), nullable=False)
    fechaIngreso = Column(DateTime, nullable=False)
    fechaSalida = Column(DateTime, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class comercioUsuarios(Base):
    _tablename_ = "comercioUsuarios"
    comercioUsuarioid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    fechaIngreso = Column(DateTime, nullable=False)
    fechaSalida = Column(DateTime, nullable=False)
    comercioid = Column(Integer, ForeignKey("comercios.comercioid"),nullable=False)
    rolid = Column(Integer, ForeignKey("roles.rolid"),nullable=False)
    usuarioid = Column(Integer, ForeignKey("usuarios.usuarioid"), nullable=False)

class UsuarioPorRol(Base):
    _tablename_ = "usuarioPorRol"
    usuarioPorRolid = Column(Integer,primary_key=True, nullable=False, autoincrement=True)
    rolid = Column(Integer, ForeignKey("roles.rolid"), nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date, nullable=False)

class TipoMercados(Base):
    _tablename_ = "tipoMercados"
    tipoMercadoid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    tipoMercadoName = Column(VARCHAR(45), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

class CategoriaKiokos(Base):
    _tablename_ = "categoriaKioskos"
    categoriaKioskoid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    categoriaKioskoName = Column(VARCHAR(45), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)

class TipoKioskos(Base):
    _tablename_ = "tipoKioskos"
    tipoKioskoid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    tipoKioskoName = Column(VARCHAR(45), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

class Kioskos(Base):
    _tablename_ = "kioskos"
    kioskoid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    kioskoCost = Column(DECIMAL(12,2), nullable=False)
    categoriaKioskoid = Column(Integer, ForeignKey("categoriaKioskos.categoriaKioskoid"), nullable=False)
    estadoKioskoid = Column(Integer, ForeignKey("estadoKioskos.estadoKioskoid"), nullable=False)
    tipoKioskoid = Column(Integer,ForeignKey("tipoKioskos.tipoKioskoid"), nullable=False)
    ancho = Column(DECIMAL(6,2), nullable=False)
    largo = Column(DECIMAL(6,2), nullable=False)
    created_at = Column(DateTime, nullable=False)
    mercadoid = Column(Integer, ForeignKey("mercados.mercadoid"), nullable=False)

class Addresses(Base):
    _tablename_ = "addresses"
    addressid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    addressName = Column(VARCHAR(150), nullable=False)
    cityid = Column(Integer, ForeignKey("cities.cityid"), nullable=False)
    geolocation = Column(Geometry(geometry_type='POINT', strid = 4326), nullable=False)

class PermisoPorRol(Base):
    _tablename_ = "permisoPorRol"
    permisoPorRolid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    rolid = Column(Integer, ForeignKey("roles.rolid"), nullable=False)
    permisoid = Column(Integer, ForeignKey("permisos.permisoid"), nullable=False)

class Permisos(Base):
    _tablename_ = "permisos"
    permisoid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombrePermiso = Column(VARCHAR(45), nullable=False) 
    codigo = Column(VARCHAR(45), nullable=False)

class Roles(Base):
    _tablename_ = "roles"
    rolid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nombreRol = Column(VARCHAR(45), nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Contracts(Base):
    _tablename_ = "contracts"
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

class PermisoPorUsuraio(Base):
    _tablename_ = "permisoPorUsuario"
    permisoPorUusarioid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    permisoid = Column(Integer, ForeignKey("permisos.permisoid"), nullable=False)
    usuarioid = Column(Integer, ForeignKey("usuarios.usuarioid"), nullable=False)

class Cities(Base):
    _tablename_ = "cities"
    cityid = Column(Integer, primary_key= True, autoincrement=True, nullable=False)
    cityName = Column(VARCHAR(100), nullable=False)
    statedid = Column(Integer, ForeignKey("states.stateid"))

class States(Base):
    _tablename_ = "states"
    stateid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    stateName = Column(VARCHAR(100), nullable=False)
    countryid = Column(Integer, ForeignKey("countries.countryid"), nullable=False)

class Countries(Base):
    _tablename_ = "countries"
    countryid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    countryName = Column(VARCHAR(100), nullable=False)

class CategoriaGastos(Base):
    _tablename_ = "categoriaGastos"
    categoriaGastoid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    categoriaGastoName = Column(VARCHAR(45), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

class EstadoKioskos(Base):
    _tablename_ = "estadoKioskos"
    estadoKioskoid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    estadoKioskoName = Column(VARCHAR(45), nullable=False)

class CategoriaProductos(Base):
    _tablename_ = "categoriaProductos"
    categoriaProductoid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    categoriaProductoName = Column(VARCHAR(45), nullable=False)
    categoriaProductoDescripcion = Column(VARCHAR(200), nullable=False)