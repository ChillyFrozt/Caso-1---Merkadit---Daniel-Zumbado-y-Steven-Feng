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
FROM caso1.facturas f
JOIN caso1.detallesfactura df ON df.facturaid = f.facturaid
JOIN caso1.productos p ON p.productoid = df.productoid
JOIN caso1.comercio c ON c.comercioid = f.comercioid
JOIN caso1.contracts con ON con.contractid = c.contractid
JOIN caso1.kioskos k ON k.kioskoid = con.kioskoid
JOIN caso1.mercados m ON m.mercadoid = k.mercadoid
JOIN caso1.buildings b ON b.buildingid = m.buildingid
JOIN caso1.contractscategoriafee cf 
    ON cf.contractid = con.contractid 
   AND cf.categoriaProductoid = p.categoriaProductoid
WHERE MONTH(f.postTime) = MONTH(CURDATE()) 
  AND YEAR(f.postTime) = YEAR(CURDATE())
GROUP BY c.comercioName, k.kioskoid, b.buildingName, con.montoBase, cf.fee
ORDER BY negocio, kiosko;
