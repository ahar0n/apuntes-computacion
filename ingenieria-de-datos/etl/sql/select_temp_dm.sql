-- Cantidad de ventas diarias agrupadas por fecha, libro, genero, comuna. Sistema OLTP Libreria
USE Libreria;
SELECT date(Pedido.Fecha) as fecha,
    Libro.Titulo AS libro,
    Genero.Nombre AS genero,
    Comuna.Nombre AS comuna,
    sum(Pedido.Cantidad) AS cantidad
FROM Pedido
INNER JOIN Libro ON Libro.LibroID = Pedido.LibroID
INNER JOIN Genero ON Genero.GeneroID = Libro.GeneroID
INNER JOIN Cliente ON Cliente.ClienteID = Pedido.ClienteID
INNER JOIN Comuna ON Comuna.ComunaID = Cliente.ComunaID
GROUP BY fecha, libro, genero, comuna;