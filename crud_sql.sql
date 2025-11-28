-- ============================================
-- SISTEMA DE GESTIÓN DE CONTACTOS (LEADS TRACKER)
-- Script SQL para MySQL Workbench + AWS RDS
-- ============================================

-- Seleccionar la base de datos
USE leads_db;

-- Eliminar la tabla si existe
DROP TABLE IF EXISTS leads;

-- Crear la tabla de leads
CREATE TABLE leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(200) NOT NULL,
    correo_electronico VARCHAR(120) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    interes_servicio VARCHAR(100) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_correo (correo_electronico),
    INDEX idx_fecha (fecha_registro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insertar datos de ejemplo
INSERT INTO leads (nombre_completo, correo_electronico, telefono, interes_servicio) VALUES
('Juan Pérez García', 'juan.perez@example.com', '+593 99 123 4567', 'Consultoría Tecnológica'),
('María González López', 'maria.gonzalez@example.com', '+593 98 765 4321', 'Desarrollo de Software'),
('Carlos Rodríguez Sánchez', 'carlos.rodriguez@example.com', '+593 97 111 2222', 'Cloud Computing (AWS)'),
('Ana Martínez Torres', 'ana.martinez@example.com', '+593 96 333 4444', 'Ciberseguridad'),
('Luis Hernández Ramírez', 'luis.hernandez@example.com', '+593 95 555 6666', 'Transformación Digital'),
('Laura Díaz Flores', 'laura.diaz@example.com', '+593 94 777 8888', 'Análisis de Datos'),
('Roberto Castro Morales', 'roberto.castro@example.com', '+593 93 999 0000', 'Inteligencia Artificial'),
('Patricia Ruiz Jiménez', 'patricia.ruiz@example.com', '+593 92 888 1111', 'Consultoría Tecnológica'),
('Fernando Silva Ortiz', 'fernando.silva@example.com', '+593 91 666 2222', 'Desarrollo de Software'),
('Carmen Vargas Mendoza', 'carmen.vargas@example.com', '+593 90 444 3333', 'Cloud Computing (AWS)');

-- Verificar que se insertaron correctamente
SELECT * FROM leads;

-- ============================================
-- CONSULTAS BÁSICAS
-- ============================================

-- Ver todos los leads
SELECT * FROM leads ORDER BY fecha_registro DESC;

-- Buscar por ID
SELECT * FROM leads WHERE id = 1;

-- Buscar por correo
SELECT * FROM leads WHERE correo_electronico = 'juan.perez@example.com';

-- Contar total de leads
SELECT COUNT(*) AS total FROM leads;

-- Leads por servicio
SELECT interes_servicio, COUNT(*) AS cantidad 
FROM leads 
GROUP BY interes_servicio 
ORDER BY cantidad DESC;

-- ============================================
-- OPERACIONES DE ACTUALIZACIÓN
-- ============================================

-- Actualizar teléfono
UPDATE leads SET telefono = '+593 99 999 9999' WHERE id = 1;

-- Actualizar servicio
UPDATE leads SET interes_servicio = 'Inteligencia Artificial' WHERE correo_electronico = 'maria.gonzalez@example.com';

-- ============================================
-- OPERACIONES DE ELIMINACIÓN
-- ============================================

-- Eliminar por ID (CUIDADO: Descomenta para usar)
-- DELETE FROM leads WHERE id = 1;

-- Eliminar por correo (CUIDADO: Descomenta para usar)
-- DELETE FROM leads WHERE correo_electronico = 'juan.perez@example.com';

-- ============================================
-- INFORMACIÓN DE CONEXIÓN
-- ============================================
-- Host: contactos.cjuwydxejd04.us-east-1.rds.amazonaws.com
-- Port: 3306
-- Usuario: admin
-- Base de datos: leads_db
