USE bd_temperatura;

-- Ejercicio 1
SELECT COUNT(*) AS registros,COUNT(temperatura_c) AS con_temperatura,
       COUNT(*)-COUNT(temperatura_c) AS sin_temperatura,
       MIN(instante_utc) AS primer_registro,MAX(instante_utc) AS ultimo_registro
FROM temperatura;

-- Ejercicio 2
SELECT instante_utc,temperatura_c FROM temperatura
WHERE instante_utc>='2026-07-01 00:00:00'
  AND instante_utc<'2026-07-08 00:00:00'
ORDER BY instante_utc;

-- Ejercicio 3
SELECT DATE(instante_utc) AS dia,COUNT(*) AS registros,
       COUNT(temperatura_c) AS con_temperatura,
       ROUND(MIN(temperatura_c),3) AS minima_c,
       ROUND(MAX(temperatura_c),3) AS maxima_c,
       ROUND(AVG(temperatura_c),3) AS media_c
FROM temperatura
GROUP BY DATE(instante_utc) ORDER BY dia;

-- Ejercicio 4
SELECT DATE(c.instante_utc) AS dia,COUNT(*) AS esperados,
 COUNT(t.instante_utc) AS recibidos,COUNT(t.temperatura_c) AS con_temperatura,
 COUNT(t.instante_utc)-COUNT(t.temperatura_c) AS nulos,
 COUNT(*)-COUNT(t.instante_utc) AS ausentes,
 ROUND(100.0*COUNT(t.temperatura_c)/COUNT(*),2) AS disponibilidad_pct
FROM calendario c LEFT JOIN temperatura t ON t.instante_utc=c.instante_utc
GROUP BY DATE(c.instante_utc) ORDER BY dia;

-- Ejercicio 6
SELECT DATE_FORMAT(c.instante_utc,'%Y-%m') AS mes,
 COUNT(*) AS esperados,COUNT(t.instante_utc) AS recibidos,
 COUNT(t.temperatura_c) AS con_temperatura,
 ROUND(AVG(t.temperatura_c),3) AS media_observada_c,
 ROUND(100.0*COUNT(t.temperatura_c)/COUNT(*),2) AS disponibilidad_pct
FROM calendario c LEFT JOIN temperatura t ON t.instante_utc=c.instante_utc
GROUP BY DATE_FORMAT(c.instante_utc,'%Y-%m') ORDER BY mes;

-- Ejercicio 7
SELECT DATE(c.instante_utc) AS dia,
 COUNT(t.temperatura_c) AS con_temperatura,
 ROUND(100.0*COUNT(t.temperatura_c)/COUNT(*),2) AS disponibilidad_pct,
 SUM(CASE WHEN t.temperatura_c>18 THEN 1 ELSE 0 END) AS sobre_18c,
 ROUND(MAX(t.temperatura_c),3) AS maxima_c
FROM calendario c LEFT JOIN temperatura t ON t.instante_utc=c.instante_utc
GROUP BY DATE(c.instante_utc)
HAVING disponibilidad_pct>=90 AND sobre_18c>=4
ORDER BY dia;

-- Ejercicio 8diaria
SELECT DATE(c.instante_utc) AS dia,
 COUNT(t.instante_utc) AS registros,COUNT(t.temperatura_c) AS con_temperatura,
 ROUND(AVG(t.temperatura_c),3) AS media_c
FROM calendario c LEFT JOIN temperatura t ON t.instante_utc=c.instante_utc
GROUP BY DATE(c.instante_utc) ORDER BY dia;

-- Ejercicio 8comparacion
SELECT p.periodo,COUNT(c.instante_utc) AS esperados,
 COUNT(t.instante_utc) AS recibidos,COUNT(t.temperatura_c) AS con_temperatura,
 ROUND(100.0*COUNT(t.temperatura_c)/COUNT(c.instante_utc),2) AS disponibilidad_pct,
 ROUND(AVG(t.temperatura_c),3) AS media_c,
 ROUND(MIN(t.temperatura_c),3) AS minima_c,
 ROUND(MAX(t.temperatura_c),3) AS maxima_c
FROM (
 SELECT 'Primera semana' AS periodo,
        CAST('2026-07-01 00:00:00' AS DATETIME) AS desde,
        CAST('2026-07-08 00:00:00' AS DATETIME) AS hasta
 UNION ALL
 SELECT 'Ultima semana',CAST('2026-09-24 00:00:00' AS DATETIME),
        CAST('2026-10-01 00:00:00' AS DATETIME)
) p
LEFT JOIN calendario c ON c.instante_utc>=p.desde AND c.instante_utc<p.hasta
LEFT JOIN temperatura t ON t.instante_utc=c.instante_utc
GROUP BY p.periodo,p.desde ORDER BY p.desde;

