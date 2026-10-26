import os
import sqlite3

# Obtener la ruta dinámica del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')
DB_PATH = os.path.join(BASE_DIR, 'buildwise.db')

# Conectar o crear la base de datos SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Leer el script SQL
with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
    sql_script = f.read()

# Adaptaciones de sintaxis de MySQL a SQLite
sql_script = sql_script.replace('SET FOREIGN_KEY_CHECKS = 0;', '')
sql_script = sql_script.replace('SET FOREIGN_KEY_CHECKS = 1;', '')
sql_script = sql_script.replace('INT AUTO_INCREMENT PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')
sql_script = sql_script.replace('DECIMAL(10,2)', 'REAL')

# Ejecutar la creación e inserción masiva
cursor.executescript(sql_script)
conn.commit()
conn.close()

print(f"¡Base de datos SQLite generada con éxito en: {DB_PATH}!")