USE VentasDM;
SELECT 
    Tiempo.Anio AS anio,
    Libro.Genero AS genero,
    SUM(round(((Cantidad * 100) / temp.total),0)) AS porcentaje    
FROM 
    Ventas
INNER JOIN Tiempo ON Tiempo.TiempoID = Ventas.TiempoID
INNER JOiN Libro ON Libro.LibroID = Ventas.LibroID
CROSS JOIN (
    SELECT SUM(Cantidad) AS total
    FROM Ventas
    ) temp
GROUP BY anio, genero
ORDER BY anio;