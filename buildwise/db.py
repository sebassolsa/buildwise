import os
import sqlite3
import re

# Ruta absoluta a la base de datos SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'buildwise.db')

def conectar():
    """Crea y retorna una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Devuelve filas como diccionarios
    return conn

def cerrar_db(conexion=None, cursor=None):
    if cursor:
        try: cursor.close()
        except: pass
    if conexion:
        try: conexion.close()
        except: pass

def ejecutar(sql, params=None):
    """Ejecuta consultas INSERT, UPDATE, DELETE en SQLite."""
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        sql_sqlite = sql.replace('%s', '?')
        cursor.execute(sql_sqlite, params or ())
        conexion.commit()
        return cursor.lastrowid
    except Exception as err:
        print(f"Error al ejecutar query: {err}")
        return None
    finally:
        cerrar_db(conexion, cursor)

def consultar(sql, params=None, uno=False):
    """Ejecuta consultas SELECT en SQLite."""
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        sql_sqlite = sql.replace('%s', '?')
        cursor.execute(sql_sqlite, params or ())
        
        if cursor.description:
            rows = cursor.fetchone() if uno else cursor.fetchall()
            if rows is None:
                return None
            if uno:
                return dict(rows)
            return [dict(r) for r in rows]
        else:
            conexion.commit()
            return cursor.lastrowid
    except Exception as err:
        print(f"Error en consulta: {err}")
        return None
    finally:
        cerrar_db(conexion, cursor)

def verificar_compatibilidad_lista(componentes):
    """
    Recibe la lista de componentes y verifica Socket, RAM y Fuente de Poder.
    Retorna (es_compatible: bool, advertencias: list)
    """
    advertencias = []
    if not componentes:
        return True, advertencias

    cpu = next((c for c in componentes if c['tipo'] == 'CPU'), None)
    mobo = next((c for c in componentes if c['tipo'] == 'MOTHERBOARD'), None)
    ram = next((c for c in componentes if c['tipo'] == 'RAM'), None)
    gpu = next((c for c in componentes if c['tipo'] == 'GPU'), None)
    fuente = next((c for c in componentes if c['tipo'] == 'FUENTE'), None)

    # 1. Validación de Socket (Procesador vs Tarjeta Madre)
    if cpu and mobo:
        socket_cpu = cpu.get('socket')
        socket_mobo = mobo.get('socket')
        if socket_cpu and socket_mobo and socket_cpu.upper() != socket_mobo.upper():
            advertencias.append(
                f"Incompatibilidad de Socket: El procesador '{cpu['nombre']}' ({socket_cpu}) "
                f"no encaja en la tarjeta madre '{mobo['nombre']}' ({socket_mobo})."
            )

    # 2. Validación de Tipo de RAM (DDR4 vs DDR5)
    if mobo and ram:
        ram_mobo = mobo.get('tipo_ram') or ('DDR5' if 'DDR5' in mobo['nombre'].upper() else 'DDR4')
        ram_modulo = ram.get('tipo_ram') or ('DDR5' if 'DDR5' in ram['nombre'].upper() else 'DDR4')
        
        if ram_mobo.upper() != ram_modulo.upper():
            advertencias.append(
                f"Incompatibilidad de Memoria RAM: La tarjeta madre '{mobo['nombre']}' utiliza {ram_mobo}, "
                f"pero agregaste un módulo '{ram['nombre']}' ({ram_modulo})."
            )

    # 3. Validación de Potencia de Fuente de Poder (Watts)
    if fuente:
        watts_fuente = fuente.get('watts', 0)
        if not watts_fuente:
            match = re.search(r'(\d+)\s*W', fuente['nombre'], re.IGNORECASE)
            watts_fuente = int(match.group(1)) if match else 500

        consumo_cpu = cpu.get('consumo_w', 65) if cpu else 65
        consumo_gpu = gpu.get('consumo_w', 150) if gpu else 0
        consumo_total = consumo_cpu + consumo_gpu + 100  # Margen para placa, RAM y SSD

        if watts_fuente and consumo_total > watts_fuente:
            advertencias.append(
                f"Fuente Insuficiente: El consumo de tu equipo es de ~{consumo_total}W "
                f"(CPU + GPU + sistema), pero la fuente '{fuente['nombre']}' solo ofrece {watts_fuente}W."
            )

    es_compatible = len(advertencias) == 0
    return es_compatible, advertencias