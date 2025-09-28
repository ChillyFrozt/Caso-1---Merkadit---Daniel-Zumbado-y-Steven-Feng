USE `caso1`;

CREATE TABLE IF NOT EXISTS `operations_log` (
  `logid`        BIGINT AUTO_INCREMENT PRIMARY KEY,
  `oper_name`    VARCHAR(64) NOT NULL,
  `oper_status`  VARCHAR(16) NOT NULL,        
  `mensaje`      VARCHAR(255) NULL,
  `details_json` JSON NULL,
  `computer`     VARCHAR(128) NULL,
  `usuario_app`  VARCHAR(128) NULL,
  `checksum_md5` CHAR(32) NULL,
  `created_at`   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS liquidaciones (
  liquidacionid  BIGINT AUTO_INCREMENT PRIMARY KEY,
  comercioid     INT NOT NULL,
  kioskoid       INT NULL,
  anio           INT NOT NULL,
  mes            INT NOT NULL,
  total_ventas   DECIMAL(14,2) NOT NULL DEFAULT 0,
  total_fee      DECIMAL(14,2) NOT NULL DEFAULT 0,
  total_comercio DECIMAL(14,2) NOT NULL DEFAULT 0,
  created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_liq (comercioid, kioskoid, anio, mes)
) ENGINE=InnoDB;

DROP PROCEDURE IF EXISTS `registerSale`;
DELIMITER //
CREATE PROCEDURE `registerSale`(
    IN p_productoName        VARCHAR(150),
    IN p_comercioName        VARCHAR(150),
    IN p_cantidad            DECIMAL(10,2),
    IN p_monto_pagado        DECIMAL(12,2),
    IN p_medio_pago_name     VARCHAR(50),
    IN p_confirmaciones_pago JSON,
    IN p_numeros_referencia  JSON,
    IN p_numero_factura      INT,
    IN p_cliente             VARCHAR(150),
    IN p_descuentos_aplic    JSON,
    IN p_usuario_app         VARCHAR(128),
    IN p_computer            VARCHAR(128)
)
BEGIN
    DECLARE v_comercioid INT;
    DECLARE v_productoid INT;
    DECLARE v_metodoPagoId INT;
    DECLARE v_precioUnit DECIMAL(12,2);
    DECLARE v_subtotal DECIMAL(12,2);
    DECLARE v_iva DECIMAL(6,2);
    DECLARE v_descuento_monto DECIMAL(12,2);
    DECLARE v_total DECIMAL(12,2);
    DECLARE v_facturaid BIGINT;
    DECLARE v_tipoTransVenta INT;
    DECLARE v_checksum CHAR(32);
    DECLARE v_msg VARCHAR(255);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET v_msg = CONCAT('Error SQL en registerSale (factura ', IFNULL(p_numero_factura,0), ')');
        INSERT INTO `operations_log`(oper_name, oper_status, mensaje, details_json, computer, usuario_app, checksum_md5)
        VALUES ('registerSale','ERROR', v_msg,
                JSON_OBJECT(
                    'producto', p_productoName,
                    'comercio', p_comercioName,
                    'cantidad', p_cantidad,
                    'monto', p_monto_pagado
                ),
                p_computer, p_usuario_app, v_checksum);
        RESIGNAL;
    END;

    START TRANSACTION;

    SET v_checksum = MD5(CONCAT_WS('|', p_productoName, p_comercioName, p_cantidad, p_monto_pagado, p_medio_pago_name, p_numero_factura, p_cliente));

    SELECT c.comercioid
      INTO v_comercioid
      FROM `comercio` c
     WHERE c.comercioName = p_comercioName
     LIMIT 1;
    IF v_comercioid IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Comercio no encontrado';
    END IF;

    SELECT p.productoid, COALESCE(p.productoIVA, 0)
      INTO v_productoid, v_iva
      FROM `productos` p
     WHERE p.comercioid = v_comercioid
       AND p.productoName = p_productoName
       AND p.deleted = b'0'
     LIMIT 1;
    IF v_productoid IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Producto no encontrado en el comercio';
    END IF;

    -- Método de pago
    SELECT mp.metodoDePagoid
      INTO v_metodoPagoId
      FROM `metodosDePago` mp
     WHERE mp.metodoDePagoName = p_medio_pago_name
     LIMIT 1;
    IF v_metodoPagoId IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Método de pago inválido';
    END IF;

    SELECT pp.precio
      INTO v_precioUnit
      FROM `precioProductos` pp
     WHERE pp.productoid = v_productoid
     ORDER BY pp.posttime DESC
     LIMIT 1;

    IF v_precioUnit IS NULL THEN
        SELECT productoPrecio INTO v_precioUnit
          FROM `productos`
         WHERE productoid = v_productoid;
    END IF;

    IF p_monto_pagado IS NOT NULL AND p_cantidad > 0 AND (ROUND(p_monto_pagado / p_cantidad,2) <> v_precioUnit) THEN
        SET v_precioUnit = ROUND(p_monto_pagado / p_cantidad, 2);
    END IF;

    SET v_subtotal = ROUND(v_precioUnit * p_cantidad, 2);

    SET v_descuento_monto = 0;
    IF p_descuentos_aplic IS NOT NULL THEN
        IF JSON_EXTRACT(p_descuentos_aplic, '$.monto') IS NOT NULL THEN
            SET v_descuento_monto = CAST(JSON_UNQUOTE(JSON_EXTRACT(p_descuentos_aplic, '$.monto')) AS DECIMAL(12,2));
        ELSEIF JSON_EXTRACT(p_descuentos_aplic, '$.porcentaje') IS NOT NULL THEN
            SET v_descuento_monto = ROUND(v_subtotal * (CAST(JSON_UNQUOTE(JSON_EXTRACT(p_descuentos_aplic, '$.porcentaje')) AS DECIMAL(6,2)) / 100), 2);
        END IF;
    END IF;

    SET v_total = ROUND((v_subtotal - v_descuento_monto) * (1 + (v_iva/100)), 2);

    INSERT INTO `facturas` (postTime, total, numeroFactura, descuento, ivaAplicado, metodosDePagoid, usuarioid, subtotal, created_at, updated_at, comercioid)
    VALUES (NOW(), v_total, p_numero_factura, v_descuento_monto, v_iva, v_metodoPagoId, NULL, v_subtotal, NOW(), NOW(), v_comercioid);
    SET v_facturaid = LAST_INSERT_ID();

    INSERT INTO `detallesfactura` (facturaid, productoid, cantidad, subtotal, precioUnitario, deleted)
    VALUES (v_facturaid, v_productoid, p_cantidad, v_subtotal, v_precioUnit, b'0');


    UPDATE `productos`
       SET productoCantidad = productoCantidad - p_cantidad,
           updated_at       = NOW()
     WHERE productoid = v_productoid;

    SELECT tt.tipoTransaccionid
      INTO v_tipoTransVenta
      FROM `tipoTransacciones` tt
     WHERE tt.tipoTransaccionName = 'VENTA'
     LIMIT 1;
    IF v_tipoTransVenta IS NULL THEN
        INSERT INTO `tipoTransacciones` (tipoTransaccionName, deleted) VALUES ('VENTA', b'0');
        SET v_tipoTransVenta = LAST_INSERT_ID();
    END IF;

    INSERT INTO `transacciones` (tipoTransaccionesid, comercioid, monto, descripcion, posttime, deleted)
    VALUES (v_tipoTransVenta, v_comercioid, v_total,
            CONCAT('Venta factura #', IFNULL(p_numero_factura,0), ' cliente: ', IFNULL(p_cliente,'')),
            NOW(), b'0');

    INSERT INTO `operations_log`(oper_name, oper_status, mensaje, details_json, computer, usuario_app, checksum_md5)
    VALUES ('registerSale','OK','Venta registrada',
            JSON_OBJECT(
                'facturaid', v_facturaid,
                'producto', p_productoName,
                'comercio', p_comercioName,
                'cantidad', p_cantidad,
                'montoTotal', v_total,
                'medioPago', p_medio_pago_name,
                'confirmacionesPago', p_confirmaciones_pago,
                'numerosReferencia', p_numeros_referencia,
                'cliente', p_cliente,
                'descuentos', p_descuentos_aplic
            ),
            p_computer, p_usuario_app, v_checksum);

    COMMIT;
END//
DELIMITER ;