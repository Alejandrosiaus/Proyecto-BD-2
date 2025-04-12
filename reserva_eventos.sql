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
