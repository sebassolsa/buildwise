# BuildWise 🖥️
**Arma tu computadora de manera sabia e inteligente**

Catálogo de componentes con especificaciones explicadas en lenguaje simple, productos compatibles
(procesador ↔ placa base ↔ RAM…), un asesor y una lista personal guardada en MySQL.

---

## 1. Ejecutarlo en tu computadora

```bash
pip install -r requirements.txt
```

1. Crea la base de datos en MySQL:
   ```sql
   CREATE DATABASE buildwise CHARACTER SET utf8mb4;
   ```
2. Copia `.env.example` como `.env` y pon tu usuario/contraseña de MySQL.
3. Crea las tablas y carga los datos:
   ```bash
   python init_db.py
   ```
   (o `mysql -u root -p buildwise < schema.sql`)
4. Inicia:
   ```bash
   python app.py
   ```
   Abre http://127.0.0.1:5000

> `init_db.py` / `schema.sql` **borran y recrean** las tablas (incluidas las listas guardadas). Úsalo solo para empezar o reiniciar.

---

## 2. Publicarlo para todos (opción más fácil: PythonAnywhere)

1. Crea cuenta en pythonanywhere.com (el plan gratis incluye MySQL y Flask).
2. Pestaña **Files**: sube la carpeta del proyecto (o súbela a GitHub y haz `git clone` en una consola Bash).
3. Pestaña **Databases**: inicializa MySQL, anota *host*, *usuario* y el nombre de la base (suele ser `tuusuario$buildwise`, créala ahí).
4. En una consola Bash: `pip install --user -r requirements.txt`, crea tu `.env` con esos datos y corre `python init_db.py`.
5. Pestaña **Web** → *Add a new web app* → Flask. En el archivo WSGI apunta a tu app:
   ```python
   import sys
   sys.path.insert(0, "/home/TUUSUARIO/buildwise")
   from app import app as application
   ```
6. Pon en `.env` una `SECRET_KEY` larga y aleatoria. Pulsa **Reload**. Listo: `tuusuario.pythonanywhere.com`.

Otras opciones: **Render** o **Railway** (ya incluye `Procfile` con gunicorn; Railway ofrece MySQL, y las variables del `.env` se configuran en su panel).

---

## Cómo funciona

| Ruta | Qué hace |
|------|----------|
| `/` | Inicio |
| `/catalogo?tipo=CPU&q=intel` | Catálogo con filtro y búsqueda |
| `/producto/<id>` | Especificaciones explicadas + productos compatibles |
| `/asesor` | Recomendación según uso y presupuesto |
| `/lista` | Tu lista guardada, con avisos de compatibilidad y total |
| `/lista/<token>` | Enlace para recuperar tu lista en otro dispositivo |

### Base de datos (`schema.sql`)
- `componentes`: datos de cada pieza. Las columnas `socket` y `tipo_ram` son las que definen la compatibilidad.
- `especificaciones`: filas `etiqueta / valor / ayuda` (la *ayuda* es la explicación para principiantes).
- `listas` y `lista_items`: listas guardadas. No hay login: cada navegador recibe un token en una cookie.

### Agregar un componente nuevo (sin tocar el código)
```sql
INSERT INTO componentes (tipo,marca,nombre,precio,descripcion,nivel,socket,tipo_ram)
VALUES ('Placa base','ASRock','ASRock B550M-HDV',80,'Placa básica para Ryzen.','Básico','AM4','DDR4');
-- luego sus specs:
INSERT INTO especificaciones (componente_id,etiqueta,valor,ayuda)
VALUES (LAST_INSERT_ID(),'Socket','AM4','El "enchufe" del procesador.');
```
Pon la foto en `static/img/` y escribe su nombre en la columna `img` (sin foto se muestra un icono).

### Reglas de compatibilidad (en `app.py`, función `relacionados`)
- CPU ↔ Placa base: mismo `socket`.
- RAM ↔ Placa base: mismo `tipo_ram`.
- GPU y almacenamiento: entran en cualquier placa del catálogo.

## Ideas para después
- [ ] Placas con DDR5, fuentes de poder y cajas (revisar vatios y tamaño)
- [ ] Comparador lado a lado
- [ ] Login para guardar varias listas
- [ ] Enlaces a tiendas
