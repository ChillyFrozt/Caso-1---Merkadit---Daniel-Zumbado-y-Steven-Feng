USE caso1;

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS; 
SET UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS; 
SET FOREIGN_KEY_CHECKS=0;

INSERT INTO countries (countryName) VALUES ('Costa Rica')
  ON DUPLICATE KEY UPDATE countryName=VALUES(countryName);
SET @country := (SELECT countryid FROM countries WHERE countryName='Costa Rica');

INSERT INTO states (stateName, countryid) VALUES ('San José', @country)
  ON DUPLICATE KEY UPDATE stateName=VALUES(stateName), countryid=VALUES(countryid);
SET @state := (SELECT stateid FROM states WHERE stateName='San José');

INSERT INTO cities (cityName, stateid) VALUES ('San José', @state)
  ON DUPLICATE KEY UPDATE cityName=VALUES(cityName), stateid=VALUES(stateid);
SET @city := (SELECT cityid FROM cities WHERE cityName='San José');

INSERT INTO addresses (addressName, cityid, geolocation)
VALUES ('Centro', @city, ST_GeomFromText('POINT(-84.09 9.93)'))
ON DUPLICATE KEY UPDATE addressName=VALUES(addressName), cityid=VALUES(cityid), geolocation=VALUES(geolocation);
SET @address := (SELECT addressid FROM addresses WHERE addressName='Centro');

INSERT INTO usuarios (usuariosName, usuariosPassword, enabled, deleted, created_at, deleted_at, updated_at)
VALUES ('seed_admin', CAST('admin123' AS BINARY), b'1', b'0', NOW(), '1900-01-01 00:00:00', NOW())
ON DUPLICATE KEY UPDATE usuariosPassword=VALUES(usuariosPassword), updated_at=VALUES(updated_at);
SET @usr := (SELECT usuarioid FROM usuarios WHERE usuariosName='seed_admin');

INSERT INTO owner (usuarioid, enabled, created_at, updated_at, deleted_at, deleted)
VALUES (@usr, b'1', NOW(), NOW(), '1900-01-01 00:00:00', b'0')
ON DUPLICATE KEY UPDATE enabled=b'1', updated_at=NOW(), deleted=b'0';
SET @owner := (SELECT ownerid FROM owner WHERE usuarioid=@usr);

INSERT INTO buildings (buildingName, addressid, created_at, created_by, updated_at, updated_by, deleted_at, maxAnchoTotal, maxLargoTotal)
VALUES ('Edificio Central', @address, NOW(), @usr, NOW(), @usr, '1900-01-01 00:00:00', 100.00, 100.00)
ON DUPLICATE KEY UPDATE buildingName=VALUES(buildingName), updated_at=NOW(), updated_by=@usr;
SET @building := (SELECT buildingid FROM buildings WHERE buildingName='Edificio Central');

INSERT INTO tipoMercado (tipoMercadoName, deleted)
VALUES ('Municipal', b'0')
ON DUPLICATE KEY UPDATE tipoMercadoName=VALUES(tipoMercadoName), deleted=b'0';
SET @tipoMercado := (SELECT tipoMercadoid FROM tipoMercado WHERE tipoMercadoName='Municipal');

INSERT INTO mercados (mercadoNombre, mercadoDescripcion, mercadoTelefono, created_at, created_by, addressid, tipoMercadoid, maxAncho, maxLargo, buildingid)
VALUES ('Mercado Central','Mercado principal','2222-2222',NOW(),@usr,@address,@tipoMercado,100.00,100.00,@building)
ON DUPLICATE KEY UPDATE mercadoDescripcion=VALUES(mercadoDescripcion), buildingid=VALUES(buildingid);
SET @mercado := (SELECT mercadoid FROM mercados WHERE mercadoNombre='Mercado Central');

INSERT INTO categoriakiosko (categoriaKioskoName, deleted)
VALUES ('A', b'0')
ON DUPLICATE KEY UPDATE categoriaKioskoName=VALUES(categoriaKioskoName), deleted=b'0';
SET @catK := (SELECT categoriaKioskoid FROM categoriakiosko WHERE categoriaKioskoName='A');

INSERT INTO estadoskiosko (estadoKioskoName)
VALUES ('Disponible')
ON DUPLICATE KEY UPDATE estadoKioskoName=VALUES(estadoKioskoName);
SET @estK := (SELECT estadoKioskoid FROM estadoskiosko WHERE estadoKioskoName='Disponible');

INSERT INTO tiposkiosko (tipoKioskoName, deleted)
VALUES ('Stand', b'0')
ON DUPLICATE KEY UPDATE tipoKioskoName=VALUES(tipoKioskoName), deleted=b'0';
SET @tipoK := (SELECT tipoKioskoid FROM tiposkiosko WHERE tipoKioskoName='Stand');

INSERT INTO kioskos (kioskoCost, categoriaKiosko, estadoKioskoid, tipoKioskoid, ancho, largo, created_at, mercadoid)
VALUES (0.00, @catK, @estK, @tipoK, 5.00, 5.00, NOW(), @mercado)
ON DUPLICATE KEY UPDATE estadoKioskoid=VALUES(estadoKioskoid), ancho=VALUES(ancho), largo=VALUES(largo);
SET @kiosko := (SELECT kioskoid FROM kioskos ORDER BY kioskoid LIMIT 1);

INSERT INTO tipoComercios (tipoComercioName, deleted)
VALUES ('Minorista', b'0')
ON DUPLICATE KEY UPDATE tipoComercioName=VALUES(tipoComercioName), deleted=b'0';
SET @tipoCom := (SELECT tipoComercioid FROM tipoComercios WHERE tipoComercioName='Minorista');

INSERT INTO estadoComercio (estadoComercioName, deleted)
VALUES ('Activo', b'0')
ON DUPLICATE KEY UPDATE estadoComercioName=VALUES(estadoComercioName), deleted=b'0';
SET @estCom := (SELECT estadoComercioid FROM estadoComercio WHERE estadoComercioName='Activo');

INSERT INTO comercio (comercioName, created_at, created_by, tipoComercioid, cedulaJuridica, razonSocial, contractid, deleted, estadoComercioid)
VALUES ('Verduras Mary', NOW(), @usr, @tipoCom, '3011111111', 'Verduras Mary S.A.', 0, '0', @estCom)
ON DUPLICATE KEY UPDATE tipoComercioid=VALUES(tipoComercioid), estadoComercioid=VALUES(estadoComercioid);

SET @comercio := (SELECT comercioid FROM comercio WHERE comercioName='Verduras Mary');

INSERT INTO contracts (posttime, fechaCobro, montoBase, fechaFinal, created_at, created_by, kioskoid, ownerid, comercioid)
VALUES (NOW(), NOW(), 0.00, '2099-12-31 00:00:00', NOW(), @usr, @kiosko, @owner, @comercio);

SET @contract := (
  SELECT contractid FROM contracts WHERE comercioid=@comercio ORDER BY posttime DESC LIMIT 1
);

UPDATE comercio SET contractid=@contract WHERE comercioid=@comercio;

INSERT INTO categoriaproductos (categoriaProductosName, categoriaProductosDescripcion)
VALUES ('Verduras','Categoría de verduras y hortalizas')
ON DUPLICATE KEY UPDATE categoriaProductosDescripcion=VALUES(categoriaProductosDescripcion);
SET @cat := (SELECT categoriaProductoid FROM categoriaproductos WHERE categoriaProductosName='Verduras');

INSERT INTO productos (
  productoName, productoPrecio, productoCantidad, productoIVA, fechaLlegada,
  descripcion, deleted, enabled, comercioid, categoriaProductoid,
  created_at, created_by, updated_at, updated_by
) VALUES (
  'Tomate', 1500.00, 100.00, 13.00, CURDATE(),
  'Tomate rojo', b'0', b'1', @comercio, @cat,
  NOW(), @usr, NOW(), @usr
)
ON DUPLICATE KEY UPDATE productoPrecio=VALUES(productoPrecio), productoCantidad=VALUES(productoCantidad), updated_at=NOW(), updated_by=@usr;

SET @prod := (SELECT productoid FROM productos WHERE comercioid=@comercio AND productoName='Tomate' LIMIT 1);

INSERT INTO precioproductos (precio, posttime, productoid)
VALUES (1500.00, NOW(), @prod);

INSERT INTO metodosDePago (metodoDePagoName, deleted)
VALUES ('SINPE', b'0')
ON DUPLICATE KEY UPDATE metodoDePagoName=VALUES(metodoDePagoName), deleted=b'0';

INSERT IGNORE INTO tipoTransacciones (tipoTransaccionName, deleted)
VALUES ('VENTA', b'0'), ('FEE_ADMIN', b'0'), ('LIQUIDACION', b'0');


INSERT INTO contractscategoriafee (contractid, categoriaProductoid, fee, valid_from, valid_to)
VALUES (@contract, @cat, 0.1000, CURDATE(), '2099-12-31')
ON DUPLICATE KEY UPDATE fee=VALUES(fee), valid_from=VALUES(valid_from), valid_to=VALUES(valid_to);

SELECT 'usuario', @usr AS usuarioid;
SELECT 'owner', @owner AS ownerid;
SELECT 'building', @building AS buildingid;
SELECT 'mercado', @mercado AS mercadoid;
SELECT 'kiosko', @kiosko AS kioskoid;
SELECT 'comercio', @comercio AS comercioid;
SELECT 'contract', @contract AS contractid;
SELECT 'producto', @prod AS productoid;

-- Reactivar checks
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;



