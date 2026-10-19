USE red_agua;

-- Crea tabal para el experimento
CREATE TABLE ra7_demo_planes (
    id_punto INT NOT NULL PRIMARY KEY,
    ubicacion POINT NOT NULL SRID 0
) ENGINE = InnoDB;

-- Inserta datos. Cuadrícula de 400x600: x=i+0.5/5, i=0...599; j=i+0.5/5 i=0...399
INSERT INTO ra7_demo_planes (id_punto, ubicacion)
WITH
digitos AS (
    SELECT 0 AS d UNION ALL SELECT 1
    UNION ALL SELECT 2 UNION ALL SELECT 3
    UNION ALL SELECT 4 UNION ALL SELECT 5
    UNION ALL SELECT 6 UNION ALL SELECT 7
    UNION ALL SELECT 8 UNION ALL SELECT 9
),
numeros AS (
    SELECT
        unidades.d
        + 10 * decenas.d
        + 100 * centenas.d AS n
    FROM digitos AS unidades
    CROSS JOIN digitos AS decenas
    CROSS JOIN digitos AS centenas
)
SELECT
    eje_y.n * 600 + eje_x.n + 1,
    POINT(
        (eje_x.n + 0.5) / 5.0,
        (eje_y.n + 0.5) / 5.0
    )
FROM numeros AS eje_x
CROSS JOIN numeros AS eje_y
WHERE eje_x.n < 600
  AND eje_y.n < 400;

-- Comprueba la insersión de datos: 240000 regs.
SELECT COUNT(*) AS total_puntos
FROM ra7_demo_planes;

-- Crea índice espacial
CREATE SPATIAL INDEX idx_ra7_demo_ubicacion
ON ra7_demo_planes (ubicacion);

-- Verifica índice espacial
SHOW INDEX FROM ra7_demo_planes;

-- Define zona de inspección
SET @zona = ST_GeomFromText('POLYGON((10 10,20 10,10 20.05,10 10))',0);

-- FILTRO Y REFINAMIENTO
-- Candidatos del filtro.
SELECT COUNT(*) AS candidatos
FROM ra7_demo_planes
WHERE MBRIntersects(@zona, ubicacion);

-- Refinamiento de los candidatos
SELECT COUNT(*) AS coincidencias
FROM ra7_demo_planes
WHERE MBRIntersects(@zona, ubicacion)
  AND ST_Intersects(@zona, ubicacion);

-- Verificación (consulta exacta de referencia)
SELECT COUNT(*) AS coincidencias_referencia
FROM ra7_demo_planes
WHERE ST_Intersects(@zona, ubicacion);

-- Estudiar estrategia del optimizador para resolver el SELECT
-- possible_keys: índices que podrían intervenir
-- key: índice seleccionado por el optimizador
-- type: mecanísmo de acceso (e.g., range, ALL)
-- rows: cantidad estimada de filas por examinar
EXPLAIN
SELECT COUNT(*)
FROM ra7_demo_planes
WHERE MBRIntersects(@zona, ubicacion)
  AND ST_Intersects(@zona, ubicacion);

-- Para comparar: EXPLAIN consulta excluyendo el índice espacial
EXPLAIN
SELECT COUNT(*)
FROM ra7_demo_planes
IGNORE INDEX (idx_ra7_demo_ubicacion)
WHERE MBRIntersects(@zona, ubicacion)
  AND ST_Intersects(@zona, ubicacion);