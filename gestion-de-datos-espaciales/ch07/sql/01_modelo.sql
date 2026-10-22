SET time_zone = '+00:00';

CREATE DATABASE bd_temporal;
USE bd_temporal;

CREATE TABLE estacion (
  estacion_id CHAR(3) PRIMARY KEY,
  nombre VARCHAR(60) NOT NULL
) ENGINE = InnoDB;

CREATE TABLE estado_estacion (
  estado_id INT PRIMARY KEY,
  estacion_id CHAR(3) NOT NULL,
  estado VARCHAR(12) NOT NULL,
  desde_utc DATETIME NOT NULL,
  hasta_utc DATETIME NULL,
  CONSTRAINT fk_estado_estacion
    FOREIGN KEY (estacion_id) REFERENCES estacion(estacion_id),
  CONSTRAINT uq_estado_inicio UNIQUE (estacion_id, desde_utc),
  CONSTRAINT ck_estado_nombre
    CHECK (estado IN ('OPERATIVA', 'INACTIVA')),
  CONSTRAINT ck_estado_intervalo
    CHECK (hasta_utc IS NULL OR desde_utc < hasta_utc)
) ENGINE = InnoDB;

CREATE TABLE lectura (
  lectura_id INT PRIMARY KEY,
  estacion_id CHAR(3) NOT NULL,
  instante_observado_utc DATETIME NOT NULL,
  nivel_cm DECIMAL(7,2) NULL,
  registrado_utc DATETIME NOT NULL,
  CONSTRAINT fk_lectura_estacion
    FOREIGN KEY (estacion_id) REFERENCES estacion(estacion_id),
  CONSTRAINT uq_lectura_instante
    UNIQUE (estacion_id, instante_observado_utc)
) ENGINE = InnoDB;