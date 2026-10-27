SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS especificaciones;
DROP TABLE IF EXISTS listas;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS componentes;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE componentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    socket VARCHAR(50),
    tdp INT,
    vatios INT,
    descripcion TEXT,
    img VARCHAR(255),
    uso_recomendado VARCHAR(50) DEFAULT 'gaming'
);

INSERT INTO componentes (nombre, tipo, precio, socket, tdp, vatios, descripcion, img, uso_recomendado) VALUES
-- ==============================================================================
-- PROCESADORES (CPU) - 9 ÍTEMS (Precios en colones)
-- ==============================================================================
('Intel Core i3-12100F', 'CPU', 52000.00, 'LGA1700', 58, NULL, 'Procesador de entrada de 4 núcleos y 8 hilos perfecto para presupuestos ajustados.', 'Intel Core i3-12100F.jpg', 'trabajo'),
('AMD Ryzen 5 5600X', 'CPU', 85000.00, 'AM4', 65, NULL, 'Gran rendimiento por su precio. Muy popular para gaming de gama media.', 'AMD Ryzen 5 5600X.jpg', 'gaming'),
('Intel Core i5-13400F', 'CPU', 115000.00, 'LGA1700', 65, NULL, 'Procesador de 10 núcleos (6P + 4E), ideal para gaming multitarea.', 'Intel Core i5-13400F.jpg', 'gaming'),
('AMD Ryzen 5 7600', 'CPU', 135000.00, 'AM5', 65, NULL, 'Excelente puerta de entrada a la plataforma DDR5 y socket AM5.', 'AMD Ryzen 5 7600.jpg', 'gaming'),
('Intel Core i5-14600K', 'CPU', 185000.00, 'LGA1700', 125, NULL, 'Procesador unlocked ideal para alta tasa de cuadros y productividad exigente.', 'Intel Core i5-14600K.jpg', 'edicion'),
('AMD Ryzen 7 5700X3D', 'CPU', 155000.00, 'AM4', 105, NULL, 'La mejor actualización para plataformas AM4 enfocada en gaming puro.', 'AMD Ryzen 7 5700X3D.jpg', 'gaming'),
('AMD Ryzen 7 7800X3D', 'CPU', 245000.00, 'AM5', 120, NULL, 'El mejor procesador dedicado puramente a juegos gracias a su memoria 3D V-Cache.', 'AMD Ryzen 7 7800X3D.jpg', 'gaming'),
('Intel Core i7-14700K', 'CPU', 260000.00, 'LGA1700', 125, NULL, 'Procesador de alto rendimiento con 20 núcleos para gaming pesado y renderizado.', 'Intel Core i7-14700K.jpg', 'streaming'),
('AMD Ryzen 9 7900X', 'CPU', 275000.00, 'AM5', 170, NULL, 'Potencia de 12 núcleos y 24 hilos orientada a edición pesada y multitarea extrema.', 'AMD Ryzen 9 7900X.jpg', 'edicion'),

-- ==============================================================================
-- TARJETAS DE VIDEO (GPU) - 10 ÍTEMS (Precios en colones)
-- ==============================================================================
('AMD RX 6600', 'GPU', 135000.00, NULL, 132, NULL, 'Excelente opción para jugar a 1080p con la mejor relación costo-beneficio.', 'AMD RX 6600.jpg', 'gaming'),
('NVIDIA RTX 3060 12GB', 'GPU', 175000.00, NULL, 170, NULL, 'Tarjeta gráfica con abundante VRAM para modelos de IA y juegos a 1080p.', 'NVIDIA RTX 3060 12GB.jpg', 'trabajo'),
('NVIDIA RTX 4060', 'GPU', 195000.00, NULL, 115, NULL, 'Tarjeta gráfica eficiente de arquitectura Ada Lovelace con soporte para DLSS 3.', 'NVIDIA RTX 4060.jpg', 'gaming'),
('AMD RX 7600 XT', 'GPU', 210000.00, NULL, 190, NULL, '16GB de VRAM ideales para texturas en ultra a resolución 1080p/1440p.', 'AMD RX 7600 XT.jpg', 'gaming'),
('NVIDIA RTX 4060 Ti 8GB', 'GPU', 255000.00, NULL, 160, NULL, 'Rendimiento sólido en 1080p y 1440p con bajo consumo energético.', 'NVIDIA RTX 4060 Ti 8GB.jpg', 'gaming'),
('AMD RX 7700 XT', 'GPU', 285000.00, NULL, 245, NULL, 'Gran opción para 1440p con alto rendimiento en rasterizado tradicional.', 'AMD RX 7700 XT.jpg', 'gaming'),
('AMD RX 7800 XT', 'GPU', 335000.00, NULL, 263, NULL, 'Competidor directo en 1440p con 16GB de VRAM para juegos exigentes.', 'AMD RX 7800 XT.jpg', 'gaming'),
('NVIDIA RTX 4070', 'GPU', 365000.00, NULL, 200, NULL, 'Ideal para jugar holgadamente en resolución 1440p (2K) a altas tasas de refresco.', 'NVIDIA RTX 4070.jpg', 'streaming'),
('NVIDIA RTX 4070 Super', 'GPU', 395000.00, NULL, 220, NULL, 'Incremento de rendimiento notable para gaming en 1440p con Ray Tracing.', 'NVIDIA RTX 4070 Super.jpg', 'gaming'),
('NVIDIA RTX 4080 Super', 'GPU', 660000.00, NULL, 320, NULL, 'Potencia extrema para gaming en 4K y flujos de trabajo profesionales pesados.', 'NVIDIA RTX 4080 Super.jpg', 'edicion'),

-- ==============================================================================
-- PLACAS BASE (MOTHERBOARD) - 5 ÍTEMS (Precios en colones)
-- ==============================================================================
('Gigabyte A520M S2H', 'MOTHERBOARD', 42000.00, 'AM4', NULL, NULL, 'Placa base ultra económica para ensambles básicos con procesadores Ryzen 3000/5000.', 'Gigabyte A520M S2H.jpg', 'trabajo'),
('MSI PRO B760M-A WiFi', 'MOTHERBOARD', 88000.00, 'LGA1700', NULL, NULL, 'Placa base formato Micro-ATX equilibrada para procesadores Intel de 12a, 13a y 14a gen.', 'MSI PRO B760M-A WiFi.jpg', 'gaming'),
('ASUS Prime B550M-A WiFi', 'MOTHERBOARD', 72000.00, 'AM4', NULL, NULL, 'Placa formato Micro-ATX con PCIe 4.0 y conectividad inalámbrica integrada.', 'ASUS Prime B550M-A WiFi.jpg', 'gaming'),
('ASUS TUF Gaming B650-PLUS', 'MOTHERBOARD', 125000.00, 'AM5', NULL, NULL, 'Placa base robusta para la plataforma Ryzen 7000/8000 con soporte PCIe 5.0.', 'ASUS TUF Gaming B650-PLUS.jpg', 'gaming'),
('MSI MAG Z790 Tomahawk WiFi', 'MOTHERBOARD', 170000.00, 'LGA1700', NULL, NULL, 'Placa de gama alta diseñada para overclocking y procesadores Intel unlocked i7 e i9.', 'MSI MAG Z790 Tomahawk WiFi.jpg', 'edicion'),

-- ==============================================================================
-- MEMORIA RAM - 4 ÍTEMS (Precios en colones)   
-- ==============================================================================
('Corsair 16GB DDR4 3200MHz', 'RAM', 26000.00, 'DDR4', NULL, NULL, 'Módulo de memoria RAM fiable para plataformas DDR4 estándar.', 'Corsair 16GB DDR4 3200MHz.jpg', 'trabajo'),
('Kingston 32GB DDR4 3600MHz', 'RAM', 52000.00, 'DDR4', NULL, NULL, 'Kit de doble canal ideal para edición de video y juegos que consumen más RAM.', 'Kingston 32GB DDR4 3600MHz.jpg', 'gaming'),
('Corsair Vengeance 16GB DDR5 5200MHz', 'RAM', 42000.00, 'DDR5', NULL, NULL, 'Memoria de entrada para la nueva generación DDR5.', 'Corsair Vengeance 16GB DDR5 5200MHz.jpg', 'gaming'),
('G.Skill Trident Z5 32GB DDR5 6000MHz', 'RAM', 78000.00, 'DDR5', NULL, NULL, 'Memoria DDR5 de alta velocidad con disipador térmico y rendimiento extremo.', 'G.Skill Trident Z5 32GB DDR5 6000MHz.jpg', 'edicion'),

-- ==============================================================================
-- ALMACENAMIENTO (SSD / HDD) - 4 ÍTEMS (Precios en colones)
-- ==============================================================================
('Kingston NV2 500GB NVMe', 'M.2', 25000.00, NULL, NULL, NULL, 'SSD M.2 económico ideal para instalar el sistema operativo de forma rápida.', 'Kingston NV2 500GB NVMe.jpg', 'trabajo'),
('Samsung 970 EVO 1TB NVMe', 'M.2', 52000.00, NULL, NULL, NULL, 'Unidad de estado sólido M.2 rápida y durable para el sistema operativo y juegos.', 'Samsung 970 EVO 1TB NVMe.jpg', 'gaming'),
('Seagate 2TB HDD', 'SATA', 35000.00, 'SATA', NULL, NULL, 'Disco duro mecánico para almacenamiento secundario de archivos pesados.', 'Seagate 2TB HDD.jpg', 'trabajo'),
('Crucial T500 2TB NVMe PCIe 4.0', 'M.2', 92000.00, NULL, NULL, NULL, 'SSD M.2 ultra rápido alcanzando hasta 7400 MB/s de lectura.', 'Crucial T500 2TB NVMe PCIe 4.0.jpg', 'edicion'),

-- ==============================================================================
-- FUENTES DE PODER (PSU) - 4 ÍTEMS (Precios en colones)
-- ==============================================================================
('EVGA 600 W1 600W 80 Plus', 'FUENTE', 31000.00, NULL, NULL, 600, 'Fuente de poder económica de 600 Watts para ensambles de entrada.', 'EVGA 600 W1 600W 80 Plus.jpg', 'trabajo'),
('MSI MAG A650BN 650W 80+ Bronze', 'FUENTE', 41000.00, NULL, NULL, 650, 'Fuente confiable de 650W con certificación Bronze para configuraciones de gama media.', 'MSI MAG A650BN 650W 80+ Bronze.jpg', 'gaming'),
('Corsair RM750x 750W Gold', 'FUENTE', 75000.00, NULL, NULL, 750, 'Fuente totalmente modular con certificación 80 Plus Gold de alta eficiencia.', 'Corsair RM750x 750W Gold.jpg', 'gaming'),
('Cooler Master MWE 850W Gold V2', 'FUENTE', 88000.00, NULL, NULL, 850, 'Potencia de sobra para placas gráficas de alto consumo como RTX 4080/4090.', 'Cooler Master MWE 850W Gold V2.jpg', 'edicion'),

-- ==============================================================================
-- GABINETES (CASE) - 3 ÍTEMS (Precios en colones)
-- ==============================================================================
('Gabinete ATX Mid Tower RGB', 'CASE', 34000.00, NULL, NULL, NULL, 'Gabinete espacioso con flujo de aire optimizado y cristal templado.', 'gabinete atx mid tower rgb.jpg', 'gaming'),
('Gabinete Micro-ATX Compacto', 'CASE', 26000.00, NULL, NULL, NULL, 'Gabinete compacto ideal para ensambles de entrada y espacios reducidos.', 'Gabinete Micro-ATX Compacto.jpg', 'trabajo'),
('Gabinete Gamer Premium ATX', 'CASE', 58000.00, NULL, NULL, NULL, 'Gabinete de gama alta con ventilación de alto rendimiento y soporte para GPUs grandes.', 'Gabinete Gamer Premium ATX.jpg', 'edicion');