-- Crear bd
CREATE DATABASE tarea3;

-- Conectar a la base de datos
\c tarea3

-- Crear tabla principal de CIs
CREATE TABLE IF NOT EXISTS cis (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    descripcion TEXT,
    numero_serie VARCHAR(100),
    version VARCHAR(50),
    fecha_adquisicion DATE,
    estado_actual VARCHAR(20) NOT NULL,
    propietario VARCHAR(100),
    ambiente VARCHAR(10) NOT NULL,
    nivel_seguridad VARCHAR(20),
    cumplimiento VARCHAR(30),
    estado_configuracion VARCHAR(30),
    numero_licencia VARCHAR(100),
    fecha_vencimiento DATE,
    documentacion TEXT,
    incidentes TEXT
);

-- Tabla de relaciones muchos-a-muchos (padres/hijos)
CREATE TABLE IF NOT EXISTS relaciones_ci (
    padre_id INT REFERENCES cis(id) ON DELETE CASCADE,
    hijo_id INT REFERENCES cis(id) ON DELETE CASCADE,
    PRIMARY KEY (padre_id, hijo_id)
);

-- Tabla de auditoría de cambios
CREATE TABLE IF NOT EXISTS auditoria (
    id SERIAL PRIMARY KEY,
    ci_id INT REFERENCES cis(id) ON DELETE CASCADE,
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descripcion_cambio TEXT NOT NULL,
    usuario VARCHAR(100)
);
