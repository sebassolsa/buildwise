import os
from db import obtener_conexion

def inicializar_bd():
    ruta_sql = os.path.join(os.path.dirname(__file__), "schema.sql")
    
    if not os.path.exists(ruta_sql):
        print("Error: No se encontró el archivo schema.sql.")
        return

    with open(ruta_sql, "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Separar comandos por punto y coma (;) ignorando comentarios
    comandos = [c.strip() for c in sql_script.split(";") if c.strip()]

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    for cmd in comandos:
        if cmd:
            cursor.execute(cmd)

    conexion.commit()
    
    # Verificar cuántos componentes se cargaron
    cursor.execute("SELECT COUNT(*) FROM componentes;")
    total = cursor.fetchone()[0]
    
    print(f"¡Éxito! Base de datos inicializada con {total} componentes desde schema.sql.")


    cursor.close()
    conexion.close()

if __name__ == "__main__":
    inicializar_bd()