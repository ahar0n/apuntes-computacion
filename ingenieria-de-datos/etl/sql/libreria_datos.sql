INSERT INTO libreria.editorial VALUES(1, 'Wiley');
INSERT INTO libreria.editorial VALUES(2, 'Penguin');
INSERT INTO libreria.editorial VALUES(3, 'Springer');
INSERT INTO libreria.editorial VALUES(4, 'CRC');
INSERT INTO libreria.editorial VALUES(5, 'MIT Press');
INSERT INTO libreria.editorial VALUES(6, 'HarperCollins');

INSERT INTO libreria.genero VALUES(1, 'Mathematics');
INSERT INTO libreria.genero VALUES(2, 'Data Science');
INSERT INTO libreria.genero VALUES(3, 'Economics');
INSERT INTO libreria.genero VALUES(4, 'History');
INSERT INTO libreria.genero VALUES(5, 'Science');

INSERT INTO libreria.libro VALUES(1, 'Data Smart', 'Foreman, John', 1, 2);
INSERT INTO libreria.libro VALUES(2, 'God Created the Integers', 'Hawking, Stephen', 2, 1);
INSERT INTO libreria.libro VALUES(3, 'Superfreakonomics',	'Dubner, Stephen',	6, 3);
INSERT INTO libreria.libro VALUES(4, 'Orientalism',	'Said, Edward', 2, 4);
INSERT INTO libreria.libro VALUES(6, 'The Nature of Statistical Learning Theory', 'Vapnik, Vladimir', 3, 2);
INSERT INTO libreria.libro VALUES(7, 'The Drunkards Walk', 'Mlodinow, Leonard', 2, 2);

INSERT INTO libreria.comuna VALUES(1, 'Santiago');
INSERT INTO libreria.comuna VALUES(2, 'Concepción');
INSERT INTO libreria.comuna VALUES(3, 'Rancagua');
INSERT INTO libreria.comuna VALUES(4, 'Iquique');
INSERT INTO libreria.comuna VALUES(5, 'La Serena');
INSERT INTO libreria.comuna VALUES(6, 'Temuco');
INSERT INTO libreria.comuna VALUES(7, 'Valdivia');

INSERT INTO libreria.cliente VALUES ('17171171K','Jossica','Jones', 'Franklin 123', 1);
INSERT INTO libreria.cliente VALUES ('181234321','Javier','Rosales', 'Sebastopol 554', 1);
INSERT INTO libreria.cliente VALUES ('161231232','Rosa','Saez', 'Campo Lindo 221', 1);
INSERT INTO libreria.cliente VALUES ('19287123K','Juan','Tapia', 'Colon 23', 2);
INSERT INTO libreria.cliente VALUES ('15287123K','Eric','Lara', 'Ohiggins 661', 4);

INSERT INTO libreria.pedido (cliente, libro, cantidad, fecha) VALUES('17171171K',1,3,'2008-11-11 13:00:00');
INSERT INTO libreria.pedido (cliente, libro, cantidad, fecha) VALUES('181234321',3,1,'2008-10-09 18:20:00');
INSERT INTO libreria.pedido (cliente, libro, cantidad, fecha) VALUES('181234321',2,1,'2010-01-03 15:00:00');
INSERT INTO libreria.pedido (cliente, libro, cantidad, fecha) VALUES('19287123K',2,1,'2011-02-03 12:00:00');
INSERT INTO libreria.pedido (cliente, libro, cantidad, fecha) VALUES('15287123K',2,1,'2010-04-04 11:00:00');
INSERT INTO libreria.pedido (cliente, libro, cantidad, fecha) VALUES('15287123K',6,1,'2011-01-11 13:00:00');
INSERT INTO libreria.pedido (cliente, libro, cantidad, fecha) VALUES('19287123K',3,2,'2012-08-03 11:00:00');
INSERT INTO libreria.pedido (cliente, libro, cantidad, fecha) VALUES('15287123K',1,2,'2012-08-03 09:00:00');
INSERT INTO libreria.pedido (cliente, libro, cantidad, fecha) VALUES('17171171K',1,6,'2012-08-03 09:00:00');
INSERT INTO libreria.pedido (cliente, libro, cantidad, fecha) VALUES('181234321',1,4,'2012-08-03 09:00:00');