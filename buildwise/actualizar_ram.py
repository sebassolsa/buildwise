import os
import sqlite3

directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_db = os.path.join(directorio_actual, "buildwise.db")

conn = sqlite3.connect(ruta_db)
cursor = conn.cursor()

# 1. Agregar la columna 'tipo_ram' a la tabla 'componentes' si aún no existe
try:
    cursor.execute("ALTER TABLE componentes ADD COLUMN tipo_ram TEXT")
    print("Columna 'tipo_ram' agregada con éxito a la tabla.")
except sqlite3.OperationalError:
    # La columna ya existía previamente
    pass

# 2. Asignar 'DDR4' o 'DDR5' a los módulos de RAM según su nombre y descripción
cursor.execute(
    "UPDATE componentes SET tipo_ram = 'DDR4' WHERE tipo = 'RAM' AND (nombre LIKE '%DDR4%' OR descripcion LIKE '%DDR4%')"
)
cursor.execute(
    "UPDATE componentes SET tipo_ram = 'DDR5' WHERE tipo = 'RAM' AND (nombre LIKE '%DDR5%' OR descripcion LIKE '%DDR5%')"
)

# 3. Asignar 'DDR4' o 'DDR5' a las Tarjetas Madre según su socket/nombre
cursor.execute(
    "UPDATE componentes SET tipo_ram = 'DDR4' WHERE tipo = 'MOTHERBOARD' AND (nombre LIKE '%DDR4%' OR socket = 'AM4' OR descripcion LIKE '%DDR4%')"
)
cursor.execute(
    "UPDATE componentes SET tipo_ram = 'DDR5' WHERE tipo = 'MOTHERBOARD' AND (nombre LIKE '%DDR5%' OR socket = 'AM5' OR descripcion LIKE '%DDR5%')"
)

conn.commit()
conn.close()
print("¡Estructura y datos de 'tipo_ram' actualizados correctamente!")