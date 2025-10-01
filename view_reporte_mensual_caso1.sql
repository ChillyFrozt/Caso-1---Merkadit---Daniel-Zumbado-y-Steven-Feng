CREATE OR REPLACE VIEW reporte_negocios_mensual AS
SELECT 
    c.comercioName AS negocio,
    k.kioskoid AS kiosko,
    b.buildingName AS edificio,
    MIN(f.postTime) AS primera_venta_mes,
    MAX(f.postTime) AS ultima_venta_mes,
    SUM(df.cantidad) AS cantidad_total_vendida,
    SUM(f.total) AS total_ventas,
    (cf.fee * 100) AS porcentaje_dueno,
    SUM(f.total * cf.fee) AS monto_dueno,
    con.montoBase AS renta_a_pagar
FROM merkadit_db.facturas f
JOIN merkadit_db.detallesFactura df ON df.facturaid = f.facturaid
JOIN merkadit_db.productos p ON p.productoid = df.productoid
JOIN merkadit_db.comercios c ON c.comercioid = f.comercioid
JOIN merkadit_db.contracts con ON con.contractid = c.contractid
JOIN merkadit_db.kioskos k ON k.kioskoid = con.kioskoid
JOIN merkadit_db.mercados m ON m.mercadoid = k.mercadoid
JOIN merkadit_db.buildings b ON b.buildingid = m.buildingid
JOIN merkadit_db.contractsCategoriaFee cf 
    ON cf.contractid = con.contractid 
   AND cf.categoriaProductoid = p.categoriaProductoid
WHERE MONTH(f.postTime) = MONTH(CURDATE()) 
  AND YEAR(f.postTime) = YEAR(CURDATE())
GROUP BY c.comercioName, k.kioskoid, b.buildingName, con.montoBase, cf.fee
ORDER BY negocio, kiosko;
