USE caso1;

-- =========================================================
-- 0) LIMPIEZA (orden seguro por FKs)
-- =========================================================
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE detallesfactura;
TRUNCATE TABLE facturas;
TRUNCATE TABLE productos;

TRUNCATE TABLE contractscategoriafee;
TRUNCATE TABLE contracts;

TRUNCATE TABLE comercio;

TRUNCATE TABLE kioskos;
TRUNCATE TABLE mercados;
TRUNCATE TABLE buildings;

TRUNCATE TABLE addresses;
TRUNCATE TABLE cities;
TRUNCATE TABLE states;
TRUNCATE TABLE countries;

TRUNCATE TABLE owner;
TRUNCATE TABLE usuarios;

TRUNCATE TABLE categoriaproductos;
TRUNCATE TABLE categoriakiosko;
TRUNCATE TABLE tiposkiosko;
TRUNCATE TABLE estadoskiosko;
TRUNCATE TABLE tipoComercios;
TRUNCATE TABLE estadoComercio;

TRUNCATE TABLE metodosDePago;

SET FOREIGN_KEY_CHECKS = 1;

-- 1) DATOS GEOGRÁFICOS

INSERT INTO countries (countryName) VALUES ('Costa Rica');
SET @country := LAST_INSERT_ID();

INSERT INTO states (stateName, countryid) VALUES ('San José', @country);
SET @state := LAST_INSERT_ID();

INSERT INTO cities (cityName, stateid) VALUES ('San José Centro', @state);
SET @city := LAST_INSERT_ID();

INSERT INTO addresses (addressName, cityid, geolocation)
VALUES ('Av Central #123', @city, ST_GeomFromText('POINT(9.934 -84.082)'));
SET @addr := LAST_INSERT_ID();


-- 2) 4 EDIFICIOS y 4 "MERCADOS" (cada mercado en su edificio)
-- 4 edificios (puedes usar la misma dirección @addr sin problema)
INSERT INTO buildings (buildingName, addressid, created_by, updated_at, updated_by, deleted_at, maxAnchoTotal, maxLargoTotal)
VALUES ('Edificio Verduras', @addr, 1, NOW(), 1, NOW(), 50.00, 50.00);
SET @bld_verd := LAST_INSERT_ID();

INSERT INTO buildings (buildingName, addressid, created_by, updated_at, updated_by, deleted_at, maxAnchoTotal, maxLargoTotal)
VALUES ('Edificio Frutas', @addr, 1, NOW(), 1, NOW(), 50.00, 50.00);
SET @bld_frut := LAST_INSERT_ID();

INSERT INTO buildings (buildingName, addressid, created_by, updated_at, updated_by, deleted_at, maxAnchoTotal, maxLargoTotal)
VALUES ('Edificio Carnes', @addr, 1, NOW(), 1, NOW(), 50.00, 50.00);
SET @bld_carn := LAST_INSERT_ID();

INSERT INTO buildings (buildingName, addressid, created_by, updated_at, updated_by, deleted_at, maxAnchoTotal, maxLargoTotal)
VALUES ('Edificio Lácteos', @addr, 1, NOW(), 1, NOW(), 50.00, 50.00);
SET @bld_lact := LAST_INSERT_ID();

-- tipo de mercado
INSERT INTO tipoMercado (tipoMercadoName, deleted) VALUES ('Supermercado', b'0');
SET @tmerc := LAST_INSERT_ID();

-- 4 áreas/lugares, cada una en su edificio respectivo
INSERT INTO mercados (mercadoNombre, mercadoDescripcion, mercadoTelefono, created_by, addressid, tipoMercadoid, maxAncho, maxLargo, buildingid)
VALUES ('Pasillo Verduras', 'Zona de frutas y verduras', '2222-1111', 1, @addr, @tmerc, 25.00, 25.00, @bld_verd);
SET @m_verd := LAST_INSERT_ID();

INSERT INTO mercados (mercadoNombre, mercadoDescripcion, mercadoTelefono, created_by, addressid, tipoMercadoid, maxAncho, maxLargo, buildingid)
VALUES ('Pasillo Frutas', 'Zona de frutas nacionales', '2222-2222', 1, @addr, @tmerc, 25.00, 25.00, @bld_frut);
SET @m_frut := LAST_INSERT_ID();

INSERT INTO mercados (mercadoNombre, mercadoDescripcion, mercadoTelefono, created_by, addressid, tipoMercadoid, maxAncho, maxLargo, buildingid)
VALUES ('Sección Carnes', 'Carnes y embutidos', '2222-3333', 1, @addr, @tmerc, 25.00, 25.00, @bld_carn);
SET @m_carn := LAST_INSERT_ID();

INSERT INTO mercados (mercadoNombre, mercadoDescripcion, mercadoTelefono, created_by, addressid, tipoMercadoid, maxAncho, maxLargo, buildingid)
VALUES ('Sección Lácteos', 'Lácteos y huevos', '2222-4444', 1, @addr, @tmerc, 25.00, 25.00, @bld_lact);
SET @m_lact := LAST_INSERT_ID();

-- 3) CAT/KIOSKO/ESTADOS/TIPOS COMERCIO
INSERT INTO estadoskiosko (estadoKioskoName)
SELECT 'Activo'
FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM estadoskiosko WHERE estadoKioskoName = 'Activo'
);
-- Guardar id en @ek
SELECT estadoKioskoid INTO @ek
FROM estadoskiosko
WHERE estadoKioskoName = 'Activo'
LIMIT 1;

-- Categoría de kiosko "Pequeño" (idempotente)
INSERT INTO categoriakiosko (categoriaKioskoName, deleted)
SELECT 'Pequeño', b'0'
FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM categoriakiosko WHERE categoriaKioskoName = 'Pequeño'
);
SELECT categoriaKioskoid INTO @ck
FROM categoriakiosko
WHERE categoriaKioskoName = 'Pequeño'
LIMIT 1;

-- Tipo de kiosko "Puesto" (idempotente) 
INSERT INTO tiposkiosko (tipoKioskoName, deleted)
SELECT 'Puesto', b'0'
FROM DUAL
WHERE NOT EXISTS (
  SELECT 1 FROM tiposkiosko WHERE tipoKioskoName = 'Puesto'
);
SELECT tipoKioskoid INTO @tk
FROM tiposkiosko
WHERE tipoKioskoName = 'Puesto'
LIMIT 1;

-- 4) USUARIO y OWNER
INSERT INTO usuarios (usuariosName, usuariosPassword, enabled, deleted, created_at, deleted_at, updated_at)
VALUES ('admin', CAST('admin123' AS BINARY), b'1', b'0', NOW(), NOW(), NOW());
SET @usr := LAST_INSERT_ID();

INSERT INTO owner (usuarioid, enabled, created_at, updated_at, deleted_at, deleted)
VALUES (@usr, b'1', NOW(), NOW(), NOW(), b'0');
SET @own := LAST_INSERT_ID();


-- 5) 4 KIOSKOS (IDs distintos y en mercados distintos)
INSERT INTO kioskos (kioskoCost, categoriaKiosko, estadoKioskoid, tipoKioskoid, ancho, largo, mercadoid)
VALUES (120000.00, @ck, @ek, @tk, 2.50, 2.50, @m_verd);
SET @k1 := LAST_INSERT_ID();

-- Kiosko 2 - Frutas 
INSERT INTO kioskos (kioskoCost, categoriaKiosko, estadoKioskoid, tipoKioskoid, ancho, largo, mercadoid)
VALUES (130000.00, @ck, @ek, @tk, 2.50, 3.00, @m_frut);
SET @k2 := LAST_INSERT_ID();

-- Kiosko 3 - Carnes 
INSERT INTO kioskos (kioskoCost, categoriaKiosko, estadoKioskoid, tipoKioskoid, ancho, largo, mercadoid)
VALUES (200000.00, @ck, @ek, @tk, 3.00, 3.00, @m_carn);
SET @k3 := LAST_INSERT_ID();

-- Kiosko 4 - Lácteos 
INSERT INTO kioskos (kioskoCost, categoriaKiosko, estadoKioskoid, tipoKioskoid, ancho, largo, mercadoid)
VALUES (150000.00, @ck, @ek, @tk, 2.50, 2.80, @m_lact);
SET @k4 := LAST_INSERT_ID();

-- 6) CONTRATOS + COMERCIOS (resolver FK circular)
--    Para cada comercio: contrato -> comercio -> actualizar contrato

SET FOREIGN_KEY_CHECKS = 0;

-- Verduras Mary  (K1)
INSERT INTO contracts (fechaCobro, montoBase, fechaFinal, created_by, kioskoid, ownerid, comercioid)
VALUES (CURDATE(), 50000.00, DATE_ADD(CURDATE(), INTERVAL 1 YEAR), @usr, @k1, @own, 0);
SET @c_verd := LAST_INSERT_ID();

INSERT INTO comercio (comercioName, created_at, created_by, tipoComercioid, cedulaJuridica, razonSocial, contractid, deleted, estadoComercioid)
VALUES ('Verduras Mary', NOW(), @usr, @tcom, '301020304', 'Verduras Mary S.A.', @c_verd, '0', @ecom);
SET @com1 := LAST_INSERT_ID();

UPDATE contracts SET comercioid = @com1 WHERE contractid = @c_verd;

-- Frutas Juan   (K2)
INSERT INTO contracts (fechaCobro, montoBase, fechaFinal, created_by, kioskoid, ownerid, comercioid)
VALUES (CURDATE(), 50000.00, DATE_ADD(CURDATE(), INTERVAL 1 YEAR), @usr, @k2, @own, 0);
SET @c_frut := LAST_INSERT_ID();

INSERT INTO comercio (comercioName, created_at, created_by, tipoComercioid, cedulaJuridica, razonSocial, contractid, deleted, estadoComercioid)
VALUES ('Frutas Juan', NOW(), @usr, @tcom, '301020305', 'Frutas Juan S.A.', @c_frut, '0', @ecom);
SET @com2 := LAST_INSERT_ID();

UPDATE contracts SET comercioid = @com2 WHERE contractid = @c_frut;

-- Carnes Pepe   (K3)
INSERT INTO contracts (fechaCobro, montoBase, fechaFinal, created_by, kioskoid, ownerid, comercioid)
VALUES (CURDATE(), 60000.00, DATE_ADD(CURDATE(), INTERVAL 1 YEAR), @usr, @k3, @own, 0);
SET @c_carn := LAST_INSERT_ID();

INSERT INTO comercio (comercioName, created_at, created_by, tipoComercioid, cedulaJuridica, razonSocial, contractid, deleted, estadoComercioid)
VALUES ('Carnes Pepe', NOW(), @usr, @tcom, '301020306', 'Carnes Pepe S.A.', @c_carn, '0', @ecom);
SET @com3 := LAST_INSERT_ID();

UPDATE contracts SET comercioid = @com3 WHERE contractid = @c_carn;

-- Lácteos Ana   (K4)
INSERT INTO contracts (fechaCobro, montoBase, fechaFinal, created_by, kioskoid, ownerid, comercioid)
VALUES (CURDATE(), 50000.00, DATE_ADD(CURDATE(), INTERVAL 1 YEAR), @usr, @k4, @own, 0);
SET @c_lact := LAST_INSERT_ID();

INSERT INTO comercio (comercioName, created_at, created_by, tipoComercioid, cedulaJuridica, razonSocial, contractid, deleted, estadoComercioid)
VALUES ('Lácteos Ana', NOW(), @usr, @tcom, '301020307', 'Lácteos Ana S.A.', @c_lact, '0', @ecom);
SET @com4 := LAST_INSERT_ID();

UPDATE contracts SET comercioid = @com4 WHERE contractid = @c_lact;

SET FOREIGN_KEY_CHECKS = 1;

-- 7) CAT. PRODUCTOS + FEE (10% para todos)

INSERT INTO categoriaproductos (categoriaProductosName, categoriaProductosDescripcion)
VALUES ('Verduras', 'Verduras y hortalizas');
SET @cat := LAST_INSERT_ID();

-- Fee activo todo el año para cada contrato
INSERT INTO contractscategoriafee (contractid, categoriaProductoid, fee, valid_from, valid_to)
VALUES 
(@c_verd, @cat, 0.10, DATE_FORMAT(CURDATE(), '%Y-01-01'), DATE_FORMAT(CURDATE(), '%Y-12-31')),
(@c_frut, @cat, 0.10, DATE_FORMAT(CURDATE(), '%Y-01-01'), DATE_FORMAT(CURDATE(), '%Y-12-31')),
(@c_carn, @cat, 0.10, DATE_FORMAT(CURDATE(), '%Y-01-01'), DATE_FORMAT(CURDATE(), '%Y-12-31')),
(@c_lact, @cat, 0.10, DATE_FORMAT(CURDATE(), '%Y-01-01'), DATE_FORMAT(CURDATE(), '%Y-12-31'));

-- 8) MÉTODO DE PAGO
INSERT INTO metodosDePago (metodoDePagoName, deleted) VALUES ('SINPE', b'0');
SET @mp := LAST_INSERT_ID();

-- 9) PRODUCTOS + FACTURAS + DETALLES (uno por negocio)
--    Todas las fechas caen en el mes actual => aparecerán en el reporte mensual.
-- Verduras Mary
INSERT INTO productos (productoName, productoPrecio, productoCantidad, productoIVA, fechaLlegada, descripcion,
                       deleted, enabled, comercioid, categoriaProductoid, created_at, created_by, updated_at, updated_by)
VALUES ('Tomate', 500.00, 100.00, 0.13, CURDATE(), 'Tomate rojo fresco',
        b'0', b'1', @com1, @cat, NOW(), @usr, NOW(), @usr);
SET @p1 := LAST_INSERT_ID();

INSERT INTO facturas (total, numeroFactura, descuento, ivaAplicado, metodosDePagoid, usuarioid, subtotal, created_at, updated_at, comercioid)
VALUES (5000.00, 1001, 0.00, 13.00, @mp, @usr, 4500.00, NOW(), NOW(), @com1);
SET @f1 := LAST_INSERT_ID();

INSERT INTO detallesfactura (facturaid, productoid, cantidad, subtotal, precioUnitario, deleted)
VALUES (@f1, @p1, 10.00, 4500.00, 450.00, b'0');

-- Frutas Juan
INSERT INTO productos (productoName, productoPrecio, productoCantidad, productoIVA, fechaLlegada, descripcion,
                       deleted, enabled, comercioid, categoriaProductoid, created_at, created_by, updated_at, updated_by)
VALUES ('Banano', 200.00, 300.00, 0.13, CURDATE(), 'Banano criollo',
        b'0', b'1', @com2, @cat, NOW(), @usr, NOW(), @usr);
SET @p2 := LAST_INSERT_ID();

INSERT INTO facturas (total, numeroFactura, descuento, ivaAplicado, metodosDePagoid, usuarioid, subtotal, created_at, updated_at, comercioid)
VALUES (6000.00, 2001, 0.00, 13.00, @mp, @usr, 5300.00, NOW(), NOW(), @com2);
SET @f2 := LAST_INSERT_ID();

INSERT INTO detallesfactura (facturaid, productoid, cantidad, subtotal, precioUnitario, deleted)
VALUES (@f2, @p2, 30.00, 5300.00, 176.67, b'0');

-- Carnes Pepe
INSERT INTO productos (productoName, productoPrecio, productoCantidad, productoIVA, fechaLlegada, descripcion,
                       deleted, enabled, comercioid, categoriaProductoid, created_at, created_by, updated_at, updated_by)
VALUES ('Carne molida', 3500.00, 80.00, 0.13, CURDATE(), 'Carne molida 90/10',
        b'0', b'1', @com3, @cat, NOW(), @usr, NOW(), @usr);
SET @p3 := LAST_INSERT_ID();

INSERT INTO facturas (total, numeroFactura, descuento, ivaAplicado, metodosDePagoid, usuarioid, subtotal, created_at, updated_at, comercioid)
VALUES (35000.00, 3001, 0.00, 13.00, @mp, @usr, 31000.00, NOW(), NOW(), @com3);
SET @f3 := LAST_INSERT_ID();

INSERT INTO detallesfactura (facturaid, productoid, cantidad, subtotal, precioUnitario, deleted)
VALUES (@f3, @p3, 10.00, 31000.00, 3100.00, b'0');

-- Lácteos Ana
INSERT INTO productos (productoName, productoPrecio, productoCantidad, productoIVA, fechaLlegada, descripcion,
                       deleted, enabled, comercioid, categoriaProductoid, created_at, created_by, updated_at, updated_by)
VALUES ('Leche entera', 900.00, 200.00, 0.13, CURDATE(), 'Leche 1L',
        b'0', b'1', @com4, @cat, NOW(), @usr, NOW(), @usr);
SET @p4 := LAST_INSERT_ID();

INSERT INTO facturas (total, numeroFactura, descuento, ivaAplicado, metodosDePagoid, usuarioid, subtotal, created_at, updated_at, comercioid)
VALUES (9000.00, 4001, 0.00, 13.00, @mp, @usr, 8000.00, NOW(), NOW(), @com4);
SET @f4 := LAST_INSERT_ID();

INSERT INTO detallesfactura (facturaid, productoid, cantidad, subtotal, precioUnitario, deleted)
VALUES (@f4, @p4, 10.00, 8000.00, 800.00, b'0');

SELECT negocio, kiosko, edificio, primera_venta_mes, ultima_venta_mes,
       cantidad_total_vendida, total_ventas,
       CONCAT(porcentaje_dueno, '%') AS porcentaje_dueno,
       monto_dueno, renta_a_pagar
FROM reporte_negocios_mensual
ORDER BY negocio;

