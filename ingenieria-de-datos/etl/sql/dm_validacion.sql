select * from VentasDM.Libro;

USE VentasDM;
SELECT sum(Ventas.Cantidad) AS cantidad
    -- Tiempo.Anio AS 'año',
    ,Libro.Genero AS genero 
    -- Localizacion.Region AS region
FROM Ventas
-- INNER JOIN Localizacion ON Localizacion.LocalizacionID = Ventas.LocalizacionID
INNER JOIN Libro ON Libro.LibroID = Ventas.LibroID
GROUP BY genero
        -- ,region
ORDER BY cantidad DESC;

USE VentasDM;
SELECT sum(Ventas.Cantidad) AS 'cant',
    Localizacion.Region AS 'region'
FROM Ventas
INNER JOIN Localizacion ON Localizacion.LocalizacionID = Ventas.LocalizacionID
GROUP BY region;