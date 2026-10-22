USE bd_temporal;

SELECT 'estacion' AS tabla, COUNT(*) AS filas FROM estacion
UNION ALL
SELECT 'estado_estacion', COUNT(*) FROM estado_estacion
UNION ALL
SELECT 'lectura', COUNT(*) FROM lectura;