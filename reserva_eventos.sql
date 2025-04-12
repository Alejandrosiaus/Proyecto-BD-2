-- Tabla de eventos
CREATE TABLE evento (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL
);

-- Tabla de asientos por evento
CREATE TABLE asiento (
    id SERIAL PRIMARY KEY,
    id_evento INTEGER NOT NULL,
    numero_asiento INTEGER NOT NULL,
    FOREIGN KEY (id_evento) REFERENCES evento(id),
    UNIQUE (id_evento, numero_asiento) -- Evita duplicados de asiento en un mismo evento
);

-- Tabla de usuarios
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla de reservas
CREATE TABLE reserva (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_asiento INTEGER NOT NULL UNIQUE, -- Solo un usuario puede reservar un asiento
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id),
    FOREIGN KEY (id_asiento) REFERENCES asiento(id)
);

-- Insertar un evento
INSERT INTO evento (nombre, fecha)
VALUES ('Concierto de Rock', '2025-06-15');

-- Insertar 30 asientos para el evento (id_evento = 1)
DO $$
BEGIN
    FOR i IN 1..30 LOOP
        INSERT INTO asiento (id_evento, numero_asiento)
        VALUES (1, i);
    END LOOP;
END $$;

-- Insertar 10 usuarios
INSERT INTO usuario (nombre) VALUES
('Ana'), ('Carlos'), ('Laura'), ('Miguel'), ('Sofía'),
('Daniel'), ('Elena'), ('Pablo'), ('Valeria'), ('Andrés');

-- Insertar 2 reservas iniciales (usuarios 1 y 2 reservan los asientos 1 y 2)
INSERT INTO reserva (id_usuario, id_asiento) VALUES
(1, 1),
(2, 2);

-- Mostrar eventos
SELECT * FROM evento;

-- Mostrar usuarios
SELECT * FROM usuario;

-- Mostrar asientos del evento
SELECT * FROM asiento WHERE id_evento = 1;

-- Mostrar reservas hechas
SELECT * FROM reserva;

DELETE FROM reserva WHERE id_asiento = 7;