DROP PROCEDURE IF EXISTS settleCommerce;
DELIMITER //

CREATE PROCEDURE settleCommerce(
    IN p_comercioName VARCHAR(150),
    IN p_localName    VARCHAR(150)  
)
proc: BEGIN
    DECLARE v_comercioid INT;
    DECLARE v_kioskoid INT;
    DECLARE v_anio INT;
    DECLARE v_mes  INT;
    DECLARE v_total_ventas DECIMAL(14,2);
    DECLARE v_total_fee DECIMAL(14,2);
    DECLARE v_total_comercio DECIMAL(14,2);
    DECLARE v_tipoFee INT;
    DECLARE v_tipoLiq INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    SET v_anio = YEAR(CURDATE());
    SET v_mes  = MONTH(CURDATE());

    START TRANSACTION;

    SELECT comercioid
      INTO v_comercioid
      FROM comercio
     WHERE comercioName = p_comercioName
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

    IF EXISTS (
        SELECT 1
          FROM transacciones t
          JOIN tipoTransacciones tt ON tt.tipoTransaccionid = t.tipoTransaccionesid
         WHERE t.comercioid = v_comercioid
           AND tt.tipoTransaccionName = 'LIQUIDACION'
           AND YEAR(t.posttime) = v_anio
           AND MONTH(t.posttime) = v_mes
    ) THEN
        ROLLBACK;
        LEAVE proc;
    END IF;

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

    SELECT tipoTransaccionid INTO v_tipoFee
      FROM tipoTransacciones WHERE tipoTransaccionName = 'FEE_ADMIN' LIMIT 1;
    IF v_tipoFee IS NULL THEN
        INSERT INTO tipoTransacciones (tipoTransaccionName, deleted) VALUES ('FEE_ADMIN', b'0');
        SET v_tipoFee = LAST_INSERT_ID();
    END IF;

    SELECT tipoTransaccionid INTO v_tipoLiq
      FROM tipoTransacciones WHERE tipoTransaccionName = 'LIQUIDACION' LIMIT 1;
    IF v_tipoLiq IS NULL THEN
        INSERT INTO tipoTransacciones (tipoTransaccionName, deleted) VALUES ('LIQUIDACION', b'0');
        SET v_tipoLiq = LAST_INSERT_ID();
    END IF;

    IF v_total_fee > 0 THEN
      INSERT INTO transacciones (tipoTransaccionesid, comercioid, monto, descripcion, posttime, deleted)
      VALUES (v_tipoFee, v_comercioid, v_total_fee,
              CONCAT('Fee admin ', LPAD(v_mes,2,'0'),'/',v_anio,' kioskoid=', IFNULL(v_kioskoid,0)),
              NOW(), b'0');
    END IF;

    IF v_total_comercio <> 0 THEN
      INSERT INTO transacciones (tipoTransaccionesid, comercioid, monto, descripcion, posttime, deleted)
      VALUES (v_tipoLiq, v_comercioid, v_total_comercio,
              CONCAT('Liquidación ', LPAD(v_mes,2,'0'),'/',v_anio,' kioskoid=', IFNULL(v_kioskoid,0)),
              NOW(), b'0');
    END IF;

    COMMIT;
END proc//
DELIMITER ;