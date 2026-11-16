CREATE DATABASE libreria;
USE libreria;

CREATE TABLE genero(
    id_genero INT NOT NULL ,
    nombre VARCHAR(200) NOT NULL,
    CONSTRAINT pk_genero PRIMARY KEY (id_genero)
);

CREATE TABLE editorial(
    id_editorial INT NOT NULL ,
    nombre VARCHAR(200) NOT NULL,
    CONSTRAINT pk_editorial PRIMARY KEY (id_editorial)
);

CREATE TABLE libro(
    id_libro INT NOT NULL ,
    titulo VARCHAR(500) NOT NULL,
    autor VARCHAR(500),
    editorial INT NOT NULL,
    genero INT NOT NULL,
    CONSTRAINT pk_libro PRIMARY KEY (id_libro),
    CONSTRAINT fk_libro_genero FOREIGN KEY (genero)
        REFERENCES genero(id_genero)
        ON DELETE NO ACTION ON UPDATE NO ACTION ,
    CONSTRAINT fk_libro_editorial FOREIGN KEY (editorial)
        REFERENCES editorial(id_editorial)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE comuna(
    id_comuna INT NOT NULL ,
    nombre VARCHAR(200) NOT NULL,
    CONSTRAINT pk_comuna PRIMARY KEY (id_comuna)
);

CREATE TABLE cliente(
    id_cliente VARCHAR(9) NOT NULL ,
    nombre VARCHAR(100),
    apellido VARCHAR(100) NOT NULL,
    direccion VARCHAR(500),
    comuna INT NOT NULL,
    CONSTRAINT pk_cliente PRIMARY KEY (id_cliente),
    CONSTRAINT fk_cliente_comuna FOREIGN KEY (comuna)
        REFERENCES comuna(id_comuna)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE pedido(
    orden INT AUTO_INCREMENT NOT NULL ,
    cliente VARCHAR(9) NOT NULL,
    libro INT NOT NULL,
    cantidad INT NOT NULL,
    fecha DATETIME NOT NULL,
    CONSTRAINT pk_pedido PRIMARY KEY (orden),
    CONSTRAINT fk_pedido_cliente FOREIGN KEY (cliente)
        REFERENCES cliente(id_cliente)
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT fk_pedido_libro FOREIGN KEY (libro)
        REFERENCES libro(id_libro)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);
