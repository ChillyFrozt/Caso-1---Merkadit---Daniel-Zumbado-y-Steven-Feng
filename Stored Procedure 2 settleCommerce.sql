USE caso1;

DROP PROCEDURE IF EXISTS settleCommerce;
DELIMITER //

CREATE PROCEDURE settleCommerce(
    IN p_comercioName VARCHAR(150),
    IN p_localName    VARCHAR(150),   
    IN p_usuario_app  VARCHAR(128),
    IN p_computer     VARCHAR(128)
)
proc: BEGIN
    DECLARE v_comercioid INT;
    DECLARE v_kioskoid INT;
    DECLARE v_anio INT;
    DECLARE v_mes  INT;
    DECLARE v_already INT;
    DECLARE v_total_ventas DECIMAL(14,2);
    DECLARE v_total_fee DECIMAL(14,2);
    DECLARE v_total_comercio DECIMAL(14,2);
    DECLARE v_checksum CHAR(32);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        INSERT INTO operations_log(oper_name, oper_status, mensaje, details_json, computer, usuario_app, checksum_md5)
        VALUES ('settleCommerce','ERROR','Error SQL en liquidación',
                JSON_OBJECT('comercio', p_comercioName, 'local', p_localName),
                p_computer, p_usuario_app, v_checksum);
        RESIGNAL;
    END;

    SET v_anio = YEAR(CURDATE());
    SET v_mes  = MONTH(CURDATE());
    SET v_checksum = MD5(CONCAT_WS('|', p_comercioName, p_localName, v_anio, v_mes));

    START TRANSACTION;

    -- 1) Comercio
    SELECT c.comercioid
      INTO v_comercioid
      FROM comercio c
     WHERE c.comercioName = p_comercioName
     LIMIT 1;
    IF v_comercioid IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Comercio no encontrado';
    END IF;

    SELECT ct.kioskoid
      INTO v_kioskoid
      FROM contracts ct
     WHERE ct.comercioid = v_comercioid
       AND (ct.fechaFinal IS NULL OR ct.fechaFinal >= CURDATE())
     ORDER BY ct.posttime DESC
     LIMIT 1;

    SELECT COUNT(*)
      INTO v_already
      FROM liquidaciones l
     WHERE l.comercioid = v_comercioid
       AND IFNULL(l.kioskoid,0) = IFNULL(v_kioskoid,0)
       AND l.anio = v_anio AND l.mes = v_mes;

    IF v_already > 0 THEN
        INSERT INTO operations_log(oper_name, oper_status, mensaje, details_json, computer, usuario_app, checksum_md5)
        VALUES ('settleCommerce','OK','Mes ya liquidado',
                JSON_OBJECT('comercio', p_comercioName, 'anio', v_anio, 'mes', v_mes),
                p_computer, p_usuario_app, v_checksum);
        ROLLBACK;
        LEAVE proc;      
    END IF;

    -- 4) Totales del mes
    SELECT IFNULL(SUM(f.total),0)
      INTO v_total_ventas
      FROM facturas f
     WHERE f.comercioid = v_comercioid
       AND YEAR(f.postTime) = v_anio
       AND MONTH(f.postTime) = v_mes;

    SELECT IFNULL(SUM(df.subtotal * cf.fee),0)
      INTO v_total_fee
      FROM detallesfactura df
      JOIN facturas f  ON f.facturaid = df.facturaid
      JOIN productos p ON p.productoid = df.productoid
      JOIN contracts c ON c.comercioid = f.comercioid
      JOIN contractscategoriafee cf
           ON cf.contractid = c.contractid
          AND cf.categoriaProductoid = p.categoriaProductoid
          AND (cf.valid_from IS NULL OR cf.valid_from <= f.postTime)
          AND (cf.valid_to   IS NULL OR cf.valid_to   >= f.postTime)
     WHERE f.comercioid = v_comercioid
       AND YEAR(f.postTime) = v_anio
       AND MONTH(f.postTime) = v_mes;

    SET v_total_comercio = ROUND(v_total_ventas - v_total_fee, 2);

    IF (SELECT COUNT(*) FROM tipoTransacciones WHERE tipoTransaccionName='FEE_ADMIN') = 0 THEN
        INSERT INTO tipoTransacciones (tipoTransaccionName, deleted) VALUES ('FEE_ADMIN', b'0');
    END IF;
    IF (SELECT COUNT(*) FROM tipoTransacciones WHERE tipoTransaccionName='LIQUIDACION') = 0 THEN
        INSERT INTO tipoTransacciones (tipoTransaccionName, deleted) VALUES ('LIQUIDACION', b'0');
    END IF;

    IF v_total_fee > 0 THEN
      INSERT INTO transacciones (tipoTransaccionesid, comercioid, monto, descripcion, posttime, deleted)
      VALUES (
        (SELECT tipoTransaccionid FROM tipoTransacciones WHERE tipoTransaccionName='FEE_ADMIN' LIMIT 1),
        v_comercioid, v_total_fee,
        CONCAT('Fee admin ', LPAD(v_mes,2,'0'),'/',v_anio,' kioskoid=', IFNULL(v_kioskoid,0)), NOW(), b'0'
      );
    END IF;

    IF v_total_comercio <> 0 THEN
      INSERT INTO transacciones (tipoTransaccionesid, comercioid, monto, descripcion, posttime, deleted)
      VALUES (
        (SELECT tipoTransaccionid FROM tipoTransacciones WHERE tipoTransaccionName='LIQUIDACION' LIMIT 1),
        v_comercioid, v_total_comercio,
        CONCAT('Liquidación ', LPAD(v_mes,2,'0'),'/',v_anio,' kioskoid=', IFNULL(v_kioskoid,0)), NOW(), b'0'
      );
    END IF;

    INSERT INTO liquidaciones (comercioid, kioskoid, anio, mes, total_ventas, total_fee, total_comercio)
    VALUES (v_comercioid, v_kioskoid, v_anio, v_mes, IFNULL(v_total_ventas,0), IFNULL(v_total_fee,0), IFNULL(v_total_comercio,0));

    -- 8) Log
    INSERT INTO operations_log(oper_name, oper_status, mensaje, details_json, computer, usuario_app, checksum_md5)
    VALUES ('settleCommerce','OK','Liquidación registrada',
            JSON_OBJECT('comercio', p_comercioName, 'anio', v_anio, 'mes', v_mes,
                        'ventas', v_total_ventas, 'fee', v_total_fee, 'neto', v_total_comercio),
            p_computer, p_usuario_app, v_checksum);

    COMMIT;

END proc//
DELIMITER ;
