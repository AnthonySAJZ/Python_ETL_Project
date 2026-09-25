# Guía de ejecución paso a paso

Esta guía explica cómo ejecutar el proyecto ETL desde cero, aunque nunca hayas
ejecutado un programa de Python. Hay dos formas:

- **Parte A – Google Colab** (en el navegador, no hay que instalar nada).
  Es el entorno que se usa en el curso.
- **Parte B – En tu computadora** (con Python instalado).

Las dos formas usan el mismo código y producen los mismos resultados.

---

# PARTE A – Google Colab

Para Colab se usa **`main.ipynb`**: tiene el mismo código que `main.py`,
dividido en celdas (Paso 0, EXTRACT, TRANSFORM, LOAD). Colab ya trae pandas.

### A.1 Tener a mano el archivo `file.ope`

Colab te pedirá subirlo desde tu computadora. Si no lo tienes:
en GitHub entra a la carpeta `server_inputs` → `file.ope` → botón
**"Download raw file"** (ícono de descarga).

### A.2 Abrir el notebook en Colab

**Opción 1 – Enlace directo (la más fácil)**

<https://colab.research.google.com/github/AnthonySAJZ/Python_ETL_Project/blob/proyecto-etl/main.ipynb>

> Si el Pull Request ya fue unido (merge), cambia `proyecto-etl` por `main`
> en el enlace.

**Opción 2 – Subir el archivo**
1. Descarga `main.ipynb` desde GitHub (o desde el ZIP del proyecto).
2. Entra a <https://colab.research.google.com>.
3. Menú **Archivo → Subir notebook** y elige `main.ipynb`.

Para conservar el notebook en tu cuenta: **Archivo → Guardar una copia en
Drive**.

### A.3 Ejecutar

1. Menú **Entorno de ejecución → Ejecutar todas**
   (o ejecuta cada celda en orden con **Shift + Enter**).
2. La celda **Paso 0** mostrará un botón **"Elegir archivos"**:
   selecciona `file.ope`. El notebook lo guarda automáticamente en
   `server_inputs/file.ope`.
3. Las celdas EXTRACT, TRANSFORM y LOAD mostrarán las validaciones `[OK]` y
   al final **ETL FINALIZADO CORRECTAMENTE**.
4. Las celdas de vista previa muestran las 3 primeras filas de `cliente` y
   `deuda`.

### A.4 Ver y descargar los resultados

- Haz clic en el ícono de **carpeta** 📁 (panel izquierdo de Colab) para ver
  `server_inputs` y `server_outputs`.
- La última celda descarga `cliente.csv`, `deuda.csv` y `deuda.db` a tu
  computadora. Si el navegador pregunta, permite las descargas múltiples.

> **Importante:** los archivos de Colab se **borran al cerrar la sesión**.
> Descarga los resultados antes de salir. La próxima vez tendrás que volver a
> subir `file.ope` (el Paso 0 lo pedirá de nuevo).

### A.5 Alternativa: ejecutar `main.py` dentro de Colab

Si prefieres ejecutar el archivo `main.py` tal cual, crea un notebook nuevo en
Colab y ejecuta esta celda (descarga el proyecto completo desde GitHub,
incluido `file.ope`):

```python
!git clone -b proyecto-etl https://github.com/AnthonySAJZ/Python_ETL_Project.git
%cd Python_ETL_Project
!python main.py
```

> Si el Pull Request ya fue unido, puedes quitar `-b proyecto-etl`.

---

# PARTE B – En tu computadora

## Paso 0. Lo que vas a necesitar

| Qué | Para qué |
|---|---|
| **Python 3.9 o superior** | Es el lenguaje con el que está hecho el proyecto. |
| **pandas** | Librería para crear los DataFrames. Se instala en el Paso 3. |
| La carpeta del proyecto | Contiene `main.py`, `server_inputs/file.ope`, etc. |

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

La carpeta correcta es la que contiene `main.py`.

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

Debes ver `main.py`, `requirements.txt`, `server_inputs` y `server_outputs`.

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
python main.py
```

### Resultado esperado

```
==================================================
PROYECTO ETL - file.ope
==================================================

EXTRACT
  [OK] Existe el archivo file.ope
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

Puedes ejecutar `python main.py` las veces que quieras:

- los archivos CSV se sobrescriben;
- la tabla SQLite se reemplaza (`if_exists="replace"`), así que **no se
  duplican registros**.

Si quieres demostrar que el proceso genera todo desde cero, borra los tres
archivos de `server_outputs` y vuelve a ejecutar `python main.py`.
**No borres** `server_inputs/file.ope`, porque es el archivo de entrada.

---

## Problemas frecuentes

| Mensaje / problema | Causa | Solución |
|---|---|---|
| `'python' no se reconoce como un comando…` | Python no está en el PATH. | Usa `py` en lugar de `python`, o reinstala Python marcando "Add python.exe to PATH". |
| `ModuleNotFoundError: No module named 'pandas'` | No se instalaron las dependencias. | Ejecuta el Paso 3. |
| `can't open file '...main.py'` | La terminal no está en la carpeta del proyecto. | Repite el Paso 2.2. |
| `VALIDACIÓN FALLIDA: Existe el archivo file.ope` | Falta `server_inputs/file.ope` o se renombró. | Asegúrate de que el archivo esté en `server_inputs` y se llame exactamente `file.ope`. |
| `PermissionError` al guardar un CSV | El CSV está abierto en Excel (Windows lo bloquea). | Cierra el archivo en Excel y ejecuta de nuevo. |
| Excel muestra los códigos sin ceros | Excel convierte el texto a número. | Es solo la vista de Excel; el CSV está correcto (Paso 5). |
| Colab: `VALIDACIÓN FALLIDA: Existe el archivo file.ope` | No se subió `file.ope` (o la sesión se reinició). | Vuelve a ejecutar la celda **Paso 0** y sube el archivo. |
| Colab: `NameError: name 'cliente' is not defined` | Se ejecutó una celda sin haber ejecutado las anteriores. | Usa **Entorno de ejecución → Ejecutar todas**. |
| Colab: la celda de descarga no descarga nada | El navegador bloqueó las descargas múltiples. | Permite las descargas en el aviso del navegador, o descarga los archivos desde el panel 📁 (clic derecho → Descargar). |

---

## Resumen rápido

**Google Colab:** abrir `main.ipynb` → **Entorno de ejecución → Ejecutar
todas** → subir `file.ope` → descargar resultados.

**En tu computadora:**

```bash
cd ruta/a/Python_ETL_Project
python -m pip install -r requirements.txt   # solo la primera vez
python main.py
```
