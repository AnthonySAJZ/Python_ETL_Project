# Guía de ejecución paso a paso

Esta guía explica cómo ejecutar el proyecto ETL desde cero, aunque nunca hayas
ejecutado un programa de Python. Hay dos formas:

- **Parte A – Google Colab** (en el navegador, no hay que instalar nada).
  Es el entorno que se usa en el curso.
- **Parte B – En tu computadora** (con Python instalado).

Las dos formas usan el mismo código y producen los mismos resultados.

---

# PARTE A – Google Colab

Para Colab se usa **`main_Anthony_Silva.ipynb`** (el mismo código que `main_Anthony_Silva.py`, dividido en
celdas). Colab ya trae pandas instalado.

Resumen:

1. Descarga `server_inputs/file.ope` desde GitHub.
2. Abre el notebook:
   <https://colab.research.google.com/github/AnthonySAJZ/Python_ETL_Project/blob/proyecto-etl/main_Anthony_Silva.ipynb>
3. **Entorno de ejecución → Ejecutar todas**.
4. En la celda **Paso 0**, pulsa **"Elegir archivos"** y sube `file.ope`.
5. Revisa las validaciones `[OK]` y descarga los resultados con la última celda.

👉 **El paso a paso completo, con lo que verás en cada celda y
cómo presentarlo, está en [GUIA_COLAB.md](GUIA_COLAB.md).**

---

# PARTE B – En tu computadora

## Paso 0. Lo que vas a necesitar

| Qué | Para qué |
|---|---|
| **Python 3.9 o superior** | Es el lenguaje con el que está hecho el proyecto. |
| **pandas** | Librería para crear los DataFrames. Se instala en el Paso 3. |
| La carpeta del proyecto | Contiene `main_Anthony_Silva.py`, `server_inputs/file.ope`, etc. |

No necesitas instalar SQLite: viene incluido con Python.

---

## Paso 1. Instalar Python (solo la primera vez)

1. Entra a <https://www.python.org/downloads/> y descarga la última versión.
2. **Windows:** en la primera pantalla del instalador marca la casilla
   **"Add python.exe to PATH"** y luego pulsa **"Install Now"**.
3. Comprueba que quedó instalado abriendo una terminal (ver Paso 2) y
   escribiendo:

   ```bash
   python --version
   ```

   Debe aparecer algo como `Python 3.12.x`.

> En Windows, si `python` no funciona, prueba con `py --version`.
> En Mac/Linux, si `python` no funciona, prueba con `python3 --version`.
> En ese caso usa `py` o `python3` en lugar de `python` en todos los pasos.

---

## Paso 2. Obtener la carpeta del proyecto y abrir una terminal en ella

### 2.1 Descargar el proyecto

**Opción A – Descargar ZIP desde GitHub (la más fácil)**
1. Entra al repositorio en GitHub.
2. Asegúrate de estar en la rama correcta: si el Pull Request ya fue unido
   (merge), usa la rama principal; si no, elige la rama `proyecto-etl` en el
   selector de ramas.
3. Pulsa el botón verde **"Code"** → **"Download ZIP"**.
4. Descomprime el ZIP (clic derecho → "Extraer todo").

**Opción B – Con git**
```bash
git clone -b proyecto-etl https://github.com/AnthonySAJZ/Python_ETL_Project.git
```

### 2.2 Abrir una terminal dentro de la carpeta

La carpeta correcta es la que contiene `main_Anthony_Silva.py`.

- **Windows:** abre la carpeta en el Explorador de archivos, haz clic en la
  barra de direcciones, escribe `cmd` y pulsa Enter.
- **Mac:** clic derecho sobre la carpeta → **"Nuevo terminal en la carpeta"**.
- **VS Code:** menú **Archivo → Abrir carpeta…**, elige la carpeta del
  proyecto y luego menú **Terminal → Nuevo terminal**.

Para comprobar que estás en el lugar correcto:

```bash
dir      # en Windows
ls       # en Mac / Linux
```

Debes ver `main_Anthony_Silva.py`, `requirements.txt`, `server_inputs` y `server_outputs`.

---

## Paso 3. Instalar las dependencias (solo la primera vez)

```bash
python -m pip install -r requirements.txt
```

Esto instala **pandas**. Al terminar puedes comprobarlo con:

```bash
python -c "import pandas; print(pandas.__version__)"
```

---

## Paso 4. Ejecutar el ETL

```bash
python main_Anthony_Silva.py
```

### Resultado esperado

```
==================================================
PROYECTO ETL - file.ope
==================================================

CREAR AMBIENTE
  Carpetas listas: server_inputs y server_outputs

EXTRACT
  [OK] Existe el archivo server_inputs/file.ope
  Total de líneas útiles leídas: 1001
  Registros de cliente (empiezan en 1): 139
  Registros de deuda (empiezan en 2): 861
  Líneas ignoradas: 1 ['Field_1']
  ...

TRANSFORM
  DataFrame cliente: 139 filas x 19 columnas
  DataFrame deuda:   861 filas x 10 columnas
  ...

LOAD
  ...
  [OK] Registros en SQLite (861) = filas del DataFrame deuda (861)
  ...

==================================================
ETL FINALIZADO CORRECTAMENTE
==================================================
```

Si todas las líneas de validación muestran `[OK]` y aparece
**ETL FINALIZADO CORRECTAMENTE**, el proceso funcionó.

---

## Paso 5. Revisar los resultados

Abre la carpeta `server_outputs`. Debe contener:

| Archivo | Contenido | Cómo abrirlo |
|---|---|---|
| `cliente.csv` | 139 clientes × 19 columnas | Excel, Bloc de notas o VS Code |
| `deuda.csv` | 861 deudas × 10 columnas | Excel, Bloc de notas o VS Code |
| `deuda.db` | Base SQLite con la tabla `deuda` (861 filas) | Ver Paso 6 |

> **Sobre Excel:** si abres un CSV con doble clic, Excel puede mostrar
> `0038518267` como `38518267`, porque lo interpreta como número. El archivo
> sí guarda los ceros: puedes comprobarlo abriéndolo con el Bloc de notas o
> VS Code.

---

## Paso 6. Revisar la base de datos SQLite (opcional)

**Opción A – Con Python (no requiere instalar nada)**

```bash
python -c "import sqlite3; c = sqlite3.connect('server_outputs/deuda.db'); print(c.execute('SELECT COUNT(*) FROM deuda').fetchone()); print(c.execute('SELECT * FROM deuda LIMIT 3').fetchall())"
```

Debe mostrar `(861,)` y las tres primeras deudas.

**Opción B – Con un programa visual**
Instala **DB Browser for SQLite** (<https://sqlitebrowser.org/>), abre
`server_outputs/deuda.db` y ve a la pestaña **"Browse Data"** (Hoja de datos).

---

## Paso 7. Volver a ejecutarlo

Puedes ejecutar `python main_Anthony_Silva.py` las veces que quieras:

- los archivos CSV se sobrescriben;
- la tabla SQLite se reemplaza (`if_exists="replace"`), así que **no se
  duplican registros**.

Si quieres demostrar que el proceso genera todo desde cero, borra los tres
archivos de `server_outputs` y vuelve a ejecutar `python main_Anthony_Silva.py`.
**No borres** `server_inputs/file.ope`, porque es el archivo de entrada.

---

## Problemas frecuentes

| Mensaje / problema | Causa | Solución |
|---|---|---|
| `'python' no se reconoce como un comando…` | Python no está en el PATH. | Usa `py` en lugar de `python`, o reinstala Python marcando "Add python.exe to PATH". |
| `ModuleNotFoundError: No module named 'pandas'` | No se instalaron las dependencias. | Ejecuta el Paso 3. |
| `can't open file '...main_Anthony_Silva.py'` | La terminal no está en la carpeta del proyecto. | Repite el Paso 2.2. |
| `VALIDACIÓN FALLIDA: Existe el archivo server_inputs/file.ope` | Falta `file.ope` o se renombró. | Coloca `file.ope` junto a `main_Anthony_Silva.py` (o dentro de `server_inputs`) con ese nombre exacto. |
| `PermissionError` al guardar un CSV | El CSV está abierto en Excel (Windows lo bloquea). | Cierra el archivo en Excel y ejecuta de nuevo. |
| Excel muestra los códigos sin ceros | Excel convierte el texto a número. | Es solo la vista de Excel; el CSV está correcto (Paso 5). |
| Colab: `VALIDACIÓN FALLIDA: Existe el archivo server_inputs/file.ope` | No se subió `file.ope` (o la sesión se reinició). | Vuelve a ejecutar la celda **Paso 0** y sube el archivo. |
| Colab: `NameError: name 'cliente' is not defined` | Se ejecutó una celda sin haber ejecutado las anteriores. | Usa **Entorno de ejecución → Ejecutar todas**. |
| Colab: la celda de descarga no descarga nada | El navegador bloqueó las descargas múltiples. | Permite las descargas en el aviso del navegador, o descarga los archivos desde el panel 📁 (clic derecho → Descargar). |

---

## Resumen rápido

**Google Colab:** abrir `main_Anthony_Silva.ipynb` → **Entorno de ejecución → Ejecutar
todas** → subir `file.ope` → descargar resultados.

**En tu computadora:**

```bash
cd ruta/a/Python_ETL_Project
python -m pip install -r requirements.txt   # solo la primera vez
python main_Anthony_Silva.py
```
