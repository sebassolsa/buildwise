import re
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)
from db import consultar, ejecutar, verificar_compatibilidad_lista

app = Flask(__name__)
app.secret_key = "buildwise_secret_key_cr"


# ==========================================
# FILTROS Y FUNCIONES AUXILIARES JINJA2
# ==========================================
@app.template_filter("formato_colones")
def formato_colones(valor):
    """Formatea valores numéricos a colones costarricenses (₡)."""
    try:
        if valor is None:
            return "₡0"
        return f"₡{float(valor):,.0f}"
    except (ValueError, TypeError):
        return f"₡{valor}"


# ==========================================
# RUTA 1: INICIO / LANDING PAGE
# ==========================================
@app.route("/")
@app.route("/inicio")
def index():
    return render_template("index.html")


@app.route("/inicio-alias")
def inicio():
    return index()


# ==========================================
# RUTA 2: CATÁLOGO DE COMPONENTES
# ==========================================
@app.route("/catalogo")
def catalogo():
    categoria = request.args.get("categoria", "todos")

    if categoria == "todos":
        sql = "SELECT * FROM componentes ORDER BY tipo ASC, precio ASC"
        componentes = consultar(sql)
    else:
        sql = "SELECT * FROM componentes WHERE tipo = %s ORDER BY precio ASC"
        componentes = consultar(sql, (categoria,))

    if componentes is None:
        componentes = []

    categorias_disponibles = [
        "CPU",
        "GPU",
        "MOTHERBOARD",
        "RAM",
        "M.2",
        "FUENTE",
        "CASE",
    ]

    return render_template(
        "catalogo.html",
        componentes=componentes,
        categoria_seleccionada=categoria,
        categorias_disponibles=categorias_disponibles,
    )


# ==========================================
# RUTA 3: DETALLE DE COMPONENTE INDIVIDUAL
# ==========================================
@app.route("/componente/<int:cid>")
def detalle_componente(cid):
    sql = "SELECT * FROM componentes WHERE id = %s"
    item = consultar(sql, (cid,), uno=True)

    if not item:
        flash("El componente solicitado no existe.", "warning")
        return redirect(url_for("catalogo"))

    sql_rec = "SELECT * FROM componentes WHERE id != %s AND tipo != %s ORDER BY RANDOM() LIMIT 4"
    recomendados = consultar(sql_rec, (cid, item["tipo"]))

    if not isinstance(recomendados, list):
        recomendados = [recomendados] if recomendados else []

    return render_template(
        "detalle.html", item=item, recomendados=recomendados
    )


# ==========================================
# RUTA 4: ASESOR DE ARMADO (COMPATIBILIDAD ESTRICTA RAM)
# ==========================================
@app.route("/asesor", methods=["GET", "POST"])
def asesor():
    recomendaciones = []
    uso = "gaming"
    presupuesto = None
    tipo_busqueda = "completo"
    categoria_especifica = "CPU"
    mensaje_error = None

    MINIMO_COMPLETO_OFICINA = 200000
    MINIMO_COMPLETO_GAMING = 330000
    MINIMO_ESPECIFICO = 25000
    UMBRAL_GPU_OFICINA = 350000

    if request.method == "POST":
        tipo_busqueda = request.form.get("tipo_busqueda", "completo")
        categoria_especifica = request.form.get("categoria_especifica", "CPU")
        uso = request.form.get("uso", "gaming")

        try:
            presupuesto_str = request.form.get("presupuesto", "0")
            presupuesto_limpio = re.sub(r"[^\d.]", "", presupuesto_str)
            presupuesto = float(presupuesto_limpio) if presupuesto_limpio else 0.0
        except (ValueError, TypeError):
            presupuesto = 0.0

        if tipo_busqueda == "completo":
            minimo_requerido = (
                MINIMO_COMPLETO_OFICINA
                if uso == "trabajo"
                else MINIMO_COMPLETO_GAMING
            )
            if presupuesto < minimo_requerido:
                mensaje_error = (
                    f"El presupuesto mínimo estimado para un ensamble completo "
                    f"de tipo '{uso.capitalize()}' es de ₡{minimo_requerido:,.0f} colones."
                )
        else:
            if presupuesto < MINIMO_ESPECIFICO:
                mensaje_error = (
                    f"El presupuesto mínimo para buscar un componente individual "
                    f"es de ₡{MINIMO_ESPECIFICO:,.0f} colones."
                )

        if not mensaje_error and presupuesto > 0:
            if tipo_busqueda == "especifico":
                sql = """
                    SELECT * FROM componentes 
                    WHERE tipo = %s AND precio <= %s AND (uso_recomendado = %s OR uso_recomendado = 'gaming' OR uso_recomendado = 'todos')
                    ORDER BY precio DESC LIMIT 3
                """
                res = consultar(sql, (categoria_especifica, presupuesto, uso))

                if isinstance(res, list):
                    recomendaciones = res
                elif res:
                    recomendaciones = [res]
                else:
                    sql_alt = """
                        SELECT * FROM componentes 
                        WHERE tipo = %s AND precio <= %s 
                        ORDER BY precio DESC LIMIT 3
                    """
                    res_alt = consultar(sql_alt, (categoria_especifica, presupuesto))
                    if isinstance(res_alt, list):
                        recomendaciones = res_alt
                    elif res_alt:
                        recomendaciones = [res_alt]
                    else:
                        recomendaciones = []

            else:
                # ENSAMBLE COMPLETO
                if uso == "trabajo":
                    if presupuesto >= UMBRAL_GPU_OFICINA:
                        porcentajes = {
                            "GPU": 0.25,
                            "CPU": 0.25,
                            "MOTHERBOARD": 0.18,
                            "RAM": 0.12,
                            "M.2": 0.10,
                            "FUENTE": 0.06,
                            "CASE": 0.04,
                        }
                    else:
                        porcentajes = {
                            "CPU": 0.35,
                            "MOTHERBOARD": 0.20,
                            "RAM": 0.15,
                            "M.2": 0.12,
                            "FUENTE": 0.10,
                            "CASE": 0.08,
                        }
                elif uso in ["gaming", "streaming"]:
                    porcentajes = {
                        "GPU": 0.38,
                        "CPU": 0.22,
                        "MOTHERBOARD": 0.13,
                        "RAM": 0.10,
                        "M.2": 0.07,
                        "FUENTE": 0.06,
                        "CASE": 0.04,
                    }
                else:
                    porcentajes = {
                        "CPU": 0.30,
                        "GPU": 0.28,
                        "MOTHERBOARD": 0.14,
                        "RAM": 0.12,
                        "M.2": 0.08,
                        "FUENTE": 0.05,
                        "CASE": 0.03,
                    }

                socket_seleccionado = None
                tipo_ram_requerido = None

                for cat, pct in porcentajes.items():
                    presupuesto_cat = presupuesto * pct
                    item = None

                    # 1. Selección de CPU
                    if cat == "CPU":
                        if uso == "trabajo" and presupuesto < UMBRAL_GPU_OFICINA:
                            sql = "SELECT * FROM componentes WHERE tipo = 'CPU' AND precio <= %s AND nombre NOT LIKE '%%X3D%%' ORDER BY precio DESC LIMIT 1"
                        else:
                            sql = "SELECT * FROM componentes WHERE tipo = 'CPU' AND precio <= %s ORDER BY precio DESC LIMIT 1"
                        
                        item = consultar(sql, (presupuesto_cat,))
                        if not item:
                            item = consultar("SELECT * FROM componentes WHERE tipo = 'CPU' ORDER BY precio ASC LIMIT 1")

                    # 2. Selección de MOTHERBOARD
                    elif cat == "MOTHERBOARD":
                        if socket_seleccionado:
                            sql = "SELECT * FROM componentes WHERE tipo = 'MOTHERBOARD' AND socket = %s AND precio <= %s ORDER BY precio DESC LIMIT 1"
                            item = consultar(sql, (socket_seleccionado, presupuesto_cat * 1.3))
                            if not item:
                                item = consultar("SELECT * FROM componentes WHERE tipo = 'MOTHERBOARD' AND socket = %s ORDER BY precio ASC LIMIT 1", (socket_seleccionado,))
                        else:
                            sql = "SELECT * FROM componentes WHERE tipo = 'MOTHERBOARD' AND precio <= %s ORDER BY precio DESC LIMIT 1"
                            item = consultar(sql, (presupuesto_cat,))

                    # 3. Selección de RAM según el socket de la tarjeta madre
                    elif cat == "RAM":
                        if tipo_ram_requerido:
                            # Busca en la columna 'socket' de las RAMs donde guardamos 'DDR4' o 'DDR5'
                            sql = "SELECT * FROM componentes WHERE tipo = 'RAM' AND socket = %s AND precio <= %s ORDER BY precio DESC LIMIT 1"
                            item = consultar(sql, (tipo_ram_requerido, presupuesto_cat * 1.8))
                            
                            if not item:
                                sql_fallback = "SELECT * FROM componentes WHERE tipo = 'RAM' AND socket = %s ORDER BY precio ASC LIMIT 1"
                                item = consultar(sql_fallback, (tipo_ram_requerido,))
                        else:
                            sql = "SELECT * FROM componentes WHERE tipo = 'RAM' AND precio <= %s ORDER BY precio DESC LIMIT 1"
                            item = consultar(sql, (presupuesto_cat,))

                    # 4. Resto de componentes
                    else:
                        sql = "SELECT * FROM componentes WHERE tipo = %s AND precio <= %s ORDER BY precio DESC LIMIT 1"
                        item = consultar(sql, (cat, presupuesto_cat))
                        if not item:
                            item = consultar("SELECT * FROM componentes WHERE tipo = %s ORDER BY precio ASC LIMIT 1", (cat,))

                    if item:
                        comp_obj = item[0] if isinstance(item, list) else item
                        recomendaciones.append(comp_obj)

                        # Actualizar parámetros para los componentes siguientes
                        if cat == "CPU":
                            socket_seleccionado = comp_obj.get("socket")

                        elif cat == "MOTHERBOARD":
                            mb_socket = str(comp_obj.get("socket") or "").upper()
                            mb_nombre = str(comp_obj.get("nombre") or "").upper()

                            # Determina si requiere DDR5 o DDR4 evaluando la tarjeta madre
                            if mb_socket == "AM5" or "DDR5" in mb_nombre:
                                tipo_ram_requerido = "DDR5"
                            else:
                                tipo_ram_requerido = "DDR4"

    return render_template(
        "asesor.html",
        recomendaciones=recomendaciones,
        uso=uso,
        presupuesto=presupuesto,
        tipo_busqueda=tipo_busqueda,
        categoria_especifica=categoria_especifica,
        mensaje_error=mensaje_error,
    )

# ==========================================
# RUTA 5: VISTA DE MI LISTA
# ==========================================
@app.route("/lista")
def lista_ver():
    ids_en_sesion = session.get("mi_lista", [])
    componentes = []

    for cid in ids_en_sesion:
        comp = consultar(
            "SELECT * FROM componentes WHERE id = %s", (cid,), uno=True
        )
        if comp:
            componentes.append(comp)

    es_compatible, advertencias = verificar_compatibilidad_lista(componentes)
    total_precio = sum(item["precio"] for item in componentes)

    return render_template(
        "lista.html",
        componentes=componentes,
        total_precio=total_precio,
        es_compatible=es_compatible,
        advertencias=advertencias,
    )


# ==========================================
# RUTA 6: AGREGAR A LA LISTA
# ==========================================
@app.route("/lista/agregar/<int:cid>", methods=["POST"])
@app.route("/lista/agregar/<int:producto_id>", methods=["POST"])
def lista_agregar(cid=None, producto_id=None):
    item_id = cid or producto_id

    if "mi_lista" not in session:
        session["mi_lista"] = []

    lista_actual = list(session["mi_lista"])

    if item_id not in lista_actual:
        lista_actual.append(item_id)
        session["mi_lista"] = lista_actual
        session.modified = True
        flash("Componente añadido a tu lista de ensamble.", "success")
    else:
        flash("El componente ya está en tu lista.", "info")

    return redirect(request.referrer or url_for("lista_ver"))


# ==========================================
# RUTA 7: AGREGAR MÚLTIPLES COMPONENTES
# ==========================================
@app.route("/lista/agregar-multiples", methods=["POST"])
def lista_agregar_multiples():
    ids = request.form.getlist("ids[]")

    if "mi_lista" not in session:
        session["mi_lista"] = []

    lista_actual = list(session["mi_lista"])
    agregados = 0

    for cid in ids:
        try:
            cid_int = int(cid)
            if cid_int not in lista_actual:
                lista_actual.append(cid_int)
                agregados += 1
        except ValueError:
            continue

    session["mi_lista"] = lista_actual
    session.modified = True

    if agregados > 0:
        flash(f"Se agregaron {agregados} componentes a tu lista.", "success")
    else:
        flash("Los componentes ya estaban en tu lista.", "info")

    return redirect(url_for("lista_ver"))


# ==========================================
# RUTA 8: ELIMINAR / QUITAR DE LA LISTA
# ==========================================
@app.route("/lista/eliminar/<int:cid>", methods=["POST"])
@app.route("/lista/quitar/<int:cid>", methods=["POST"])
def lista_eliminar(cid):
    if "mi_lista" in session:
        lista_actual = list(session["mi_lista"])
        if cid in lista_actual:
            lista_actual.remove(cid)
            session["mi_lista"] = lista_actual
            session.modified = True
            flash("Componente eliminado de tu lista.", "info")

    return redirect(url_for("lista_ver"))


@app.route("/lista/quitar-alias/<int:cid>", methods=["POST"])
def lista_quitar(cid):
    return lista_eliminar(cid)


# ==========================================
# RUTA 9: VACIAR LA LISTA
# ==========================================
@app.route("/lista/vaciar", methods=["POST"])
def lista_vaciar():
    session["mi_lista"] = []
    session.modified = True
    flash("Tu lista ha sido vaciada.", "info")
    return redirect(url_for("lista_ver"))


# ==========================================
# MANEJO DE ERRORES HTTP
# ==========================================
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template("index.html"), 404


@app.errorhandler(500)
def error_servidor(e):
    return "Error interno del servidor.", 500


if __name__ == "__main__":
    for puerto in [5000, 5001, 5002, 8080]:
        try:
            app.run(debug=True, host="127.0.0.1", port=puerto)
            break
        except SystemExit:  
            continue
        except OSError:
            continue