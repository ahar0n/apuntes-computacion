SET @centro = ST_GeomFromText('POINT(91 43)', 0);
SET @caja = ST_GeomFromText('POLYGON((63 15, 119 15, 119 15, 63 71, 63 15))',0);

-- Paso didáctico 1: observar los candidatos y sus distancias.
SELECT
    id_punto,
    ST_AsText(ubicacion) AS coordenadas,
    ST_Distance(ubicacion, @centro) AS distancia
FROM ra3_punto
WHERE MBRIntersects(ubicacion, @caja)
ORDER BY id_punto;

-- Paso didáctico 2: conservar solo las coincidencias exactas.
SELECT
    id_punto,
    ST_AsText(ubicacion) AS coordenadas,
    ST_Distance(ubicacion, @centro) AS distancia
FROM ra3_punto
WHERE MBRIntersects(ubicacion, @caja)
  AND ST_Distance(ubicacion, @centro) <= 28
ORDER BY id_punto;