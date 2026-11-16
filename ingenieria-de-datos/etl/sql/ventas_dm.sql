CREATE DATABASE ventas_dm;
USE ventas_dm;
            
CREATE TABLE libro
(
    id_libro INT NOT NULL,
    titulo VARCHAR(500) NOT NULL,
    genero VARCHAR(200) NULL    ,
    CONSTRAINT pk_libro PRIMARY KEY (id_libro)
) COMMENT 'Dimension';

CREATE TABLE localizacion
(
    id_localizacion INT NOT NULL,
    comuna VARCHAR(200) NOT NULL,
    region VARCHAR(200) NOT NULL,
    CONSTRAINT pk_localizacion PRIMARY KEY (id_localizacion)
) COMMENT 'Dimension';

CREATE TABLE tiempo
(
    id_tiempo INT NOT NULL,
    fecha DATE NOT NULL,
    dia INT NOT NULL,
    mes INT NOT NULL,
    anio INT NOT NULL,
    trimestre INT NOT NULL,
    CONSTRAINT pk_tiempo PRIMARY KEY (id_tiempo)
) COMMENT 'Dimension';

CREATE TABLE ventas
(
    id_localizacion INT NOT NULL,
    id_tiempo INT NOT NULL,
    id_libro INT NOT NULL,
    cantidad INT NOT NULL,
    CONSTRAINT pk_ventas PRIMARY KEY (id_libro, id_localizacion, id_tiempo),
    CONSTRAINT fk_localizacion_ventas FOREIGN KEY (id_localizacion) REFERENCES localizacion(id_localizacion),
    CONSTRAINT fk_tiempo_ventas FOREIGN KEY (id_tiempo) REFERENCES tiempo (id_tiempo),
    CONSTRAINT fk_libro_ventas FOREIGN KEY (id_libro) REFERENCES libro (id_libro)
) COMMENT 'FactTable';
