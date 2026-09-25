# Paso a paso: ejecutar el proyecto en Google Colab

Esta guía explica, pantalla por pantalla, cómo ejecutar el proyecto ETL en
**Google Colab** usando el notebook **`main_Anthony_Silva.ipynb`**. No hace falta instalar
nada: solo un navegador y una cuenta de Google.

> `main_Anthony_Silva.ipynb` contiene **el mismo código que `main_Anthony_Silva.py`**, dividido en celdas
> para poder ejecutarlo y explicarlo paso a paso.

---

## Resumen en 5 pasos

1. Descargar `file.ope` a tu computadora.
2. Abrir `main_Anthony_Silva.ipynb` en Colab.
3. **Entorno de ejecución → Ejecutar todas**.
4. En la celda *Paso 0*, subir `file.ope`.
5. Revisar los resultados y descargarlos.

---

## Paso 1. Descargar el archivo de datos `file.ope`

Colab te pedirá subir este archivo desde tu computadora.

1. Entra al repositorio en GitHub:
   <https://github.com/AnthonySAJZ/Python_ETL_Project>
2. Si el Pull Request aún no fue unido (merge), selecciona la rama
   **`proyecto-etl`** en el selector de ramas (arriba a la izquierda).
3. Abre la carpeta **`server_inputs`** → archivo **`file.ope`**.
4. Pulsa el botón **"Download raw file"** (ícono de flecha hacia abajo, a la
   derecha).

Guarda el archivo con el nombre `file.ope` (si el navegador le cambia el
nombre, no importa: el notebook lo renombra automáticamente).

---

## Paso 2. Abrir `main_Anthony_Silva.ipynb` en Google Colab

Elige **una** de estas opciones.

### Opción A – Enlace directo (recomendada)

Abre este enlace en el navegador (con tu cuenta de Google iniciada):

<https://colab.research.google.com/github/AnthonySAJZ/Python_ETL_Project/blob/proyecto-etl/main_Anthony_Silva.ipynb>

> Si el Pull Request ya fue unido, usa este otro enlace:
> <https://colab.research.google.com/github/AnthonySAJZ/Python_ETL_Project/blob/main/main_Anthony_Silva.ipynb>

### Opción B – Desde el menú de Colab

1. Entra a <https://colab.research.google.com>.
2. En la ventana que aparece, elige la pestaña **GitHub**.
3. Pega `https://github.com/AnthonySAJZ/Python_ETL_Project`, elige la rama y
   haz clic en **`main_Anthony_Silva.ipynb`**.

### Opción C – Subir el archivo

1. Descarga `main_Anthony_Silva.ipynb` desde GitHub (igual que en el Paso 1).
2. En Colab: **Archivo → Subir notebook** y elige `main_Anthony_Silva.ipynb`.

### Guardar tu propia copia (recomendado)

Si abriste el notebook con la opción A o B, ve a **Archivo → Guardar una copia
en Drive**. Así el notebook queda en tu Google Drive y puedes volver a abrirlo
o compartirlo con tu profesor.

---

## Paso 3. Ejecutar todas las celdas

1. Menú **Entorno de ejecución → Ejecutar todas**
   (en inglés: *Runtime → Run all*; atajo **Ctrl + F9**).
2. Si aparece el aviso **"Este notebook no lo creó Google"**, pulsa
   **"Ejecutar de todos modos"** (*Run anyway*). Es normal en notebooks
   abiertos desde GitHub.

---

## Paso 4. Subir `file.ope` (celda "Paso 0")

1. La primera celda de código mostrará el mensaje
   *"Selecciona el archivo file.ope desde tu computadora"* y un botón
   **"Elegir archivos"** (*Choose Files*).
2. Pulsa el botón y selecciona el `file.ope` que descargaste en el Paso 1.
3. Verás el mensaje:
   `'file.ope' subido como file.ope`
4. Las demás celdas se ejecutarán solas, una tras otra.

> Mientras no subas el archivo, las demás celdas quedan en espera.

---

## Paso 5. Revisar lo que muestra cada celda

| Celda | Qué hace | Qué debes ver |
|---|---|---|
| **Paso 0** | Sube `file.ope` desde tu computadora. | `... subido como file.ope` |
| **Librerías, rutas y columnas** | Importa pandas, pathlib, shutil y sqlite3; define rutas y columnas. | `PROYECTO ETL - file.ope` |
| **Crear el ambiente** | Crea `server_inputs` y `server_outputs` y copia `file.ope` al servidor de entrada. | `Carpetas listas: server_inputs y server_outputs` y `file.ope copiado a la carpeta server_inputs` |
| **EXTRACT** | Lee `file.ope` y separa clientes (`1`) y deudas (`2`). | `Registros de cliente: 139`, `Registros de deuda: 861`, `Líneas ignoradas: 1 ['Field_1']` |
| **TRANSFORM** | Crea los DataFrames `cliente` y `deuda`, `Cod_Cuenta` y los renombrados. | `139 filas x 19 columnas`, `861 filas x 10 columnas` y validaciones `[OK]` |
| **LOAD** | Guarda `cliente.csv`, `deuda.csv` y `deuda.db`. | `[OK] Registros en SQLite (861) = ...` y **ETL FINALIZADO CORRECTAMENTE** |
| **Vista previa** | Muestra las 3 primeras filas de `cliente` y de `deuda`. | Dos tablas; los códigos conservan ceros (`0038518267`). |
| **Consulta SQLite** | Lee 3 filas de la tabla `deuda` dentro de `deuda.db`. | Una tabla igual a la vista previa de `deuda`. |
| **Descargar** | Descarga los 3 archivos de resultado. | Tres descargas en tu navegador. |

Todas las validaciones deben mostrar **`[OK]`**. Si alguna falla, el
notebook se detiene y muestra `VALIDACIÓN FALLIDA: ...` con el motivo.

---

## Paso 6. Ver y descargar los resultados

- **Ver los archivos:** haz clic en el ícono de **carpeta** 📁 del panel
  izquierdo. Verás `server_inputs/file.ope` y, dentro de `server_outputs`,
  `cliente.csv`, `deuda.csv` y `deuda.db`. Si no aparecen, pulsa el botón
  de actualizar del panel.
- **Descargar:** la última celda los descarga automáticamente. Si el
  navegador pregunta, permite **descargar varios archivos**. También puedes
  hacer clic derecho sobre un archivo del panel 📁 → **Descargar**.

> **Importante:** los archivos de Colab son temporales y se **borran cuando
> la sesión se desconecta o se cierra**. Descarga los resultados antes de
> salir.

---

## Paso 7. Volver a ejecutarlo

- **En la misma sesión:** menú **Entorno de ejecución → Reiniciar sesión y
  ejecutar todo** (*Restart session and run all*). Como `file.ope` ya está
  subido, el Paso 0 no lo vuelve a pedir. Los resultados se sobrescriben y
  SQLite no duplica registros.
- **En una sesión nueva** (por ejemplo, al día siguiente): el Paso 0 pedirá
  subir `file.ope` otra vez.

---

## Paso 8. Descargar el notebook para entregarlo

El profesor pide **un único archivo** llamado `main_<nombre>_<ape_pat>`. Para
entregar el notebook **con los resultados de tu ejecución**:

1. Ejecuta todo (Pasos 3 a 5) y comprueba que aparezca
   **ETL FINALIZADO CORRECTAMENTE**.
2. Revisa el nombre del notebook (arriba a la izquierda). Si dice
   **"Copia de main_Anthony_Silva.ipynb"** (pasa al usar *Guardar una copia
   en Drive*), haz clic sobre el nombre y déjalo en
   **`main_Anthony_Silva.ipynb`**.
3. Menú **Archivo → Descargar → Descargar .ipynb**.
4. Entrega ese archivo. No hace falta adjuntar carpetas: el notebook crea
   `server_inputs` y `server_outputs` por sí solo.

---

## Alternativa: ejecutar `main_Anthony_Silva.py` dentro de Colab

Si el profesor pide ver el script `main_Anthony_Silva.py` en funcionamiento, crea un
notebook nuevo en Colab (**Archivo → Nuevo notebook**) y ejecuta esta celda.
Descarga el proyecto completo desde GitHub (incluido `file.ope`) y ejecuta el
script:

```python
!git clone -b proyecto-etl https://github.com/AnthonySAJZ/Python_ETL_Project.git
%cd Python_ETL_Project
!python main_Anthony_Silva.py
```

> Si el Pull Request ya fue unido, puedes quitar `-b proyecto-etl`.
> Si vuelves a ejecutar la celda en la misma sesión, `git clone` dirá que la
> carpeta ya existe; en ese caso ejecuta solo `!python main_Anthony_Silva.py`.

---

## Cómo presentarlo al profesor en Colab

Ejecuta todo antes de la presentación y luego recorre las celdas en orden:

1. **Paso 0 y Crear el ambiente:** "Subo `file.ope` y el programa crea los
   dos servidores: `server_inputs` (entrada) y `server_outputs` (salida), y
   deja `file.ope` en el servidor de entrada."
2. **Librerías y rutas:** "Uso pandas para los DataFrames, pathlib para las
   rutas y sqlite3 para la base de datos. Defino las 19 columnas de cliente y
   las 10 finales de deuda."
3. **EXTRACT:** "Leo el archivo y separo las líneas por su primer carácter:
   1 es cliente, 2 es deuda. La cabecera `Field_1` se ignora."
4. **TRANSFORM:** "En cliente separo por `|` y obtengo 19 campos. En deuda
   corto por posiciones; como Python empieza en 0, el carácter 1 al 10 es
   `[0:10]`. `Cod_Cuenta` es la unión de texto de Nivel2, Moneda y
   SubCodigoCuenta. Después renombro las 6 columnas."
5. **LOAD:** "Guardo los dos CSV en `server_outputs` y, como bono, la deuda
   en SQLite. Compruebo con `SELECT COUNT(*)` que hay 861 registros."
6. **Vista previa y consulta SQLite:** "Aquí se ven los datos finales y se
   confirma que los códigos conservan los ceros iniciales."

---

## Problemas frecuentes en Colab

| Problema | Causa | Solución |
|---|---|---|
| Aviso "Este notebook no lo creó Google" | El notebook se abrió desde GitHub. | Pulsa **Ejecutar de todos modos**. |
| No aparece el botón "Elegir archivos" | La celda Paso 0 no se ejecutó o se interrumpió. | Ejecuta de nuevo la celda Paso 0 (botón ▶). |
| `VALIDACIÓN FALLIDA: Existe el archivo server_inputs/file.ope` | No se subió `file.ope` o la sesión se desconectó. | Ejecuta la celda Paso 0, sube el archivo y vuelve a **Ejecutar todas**. |
| `NameError: name 'cliente' is not defined` | Se ejecutó una celda sin ejecutar las anteriores. | Usa **Entorno de ejecución → Ejecutar todas**. |
| La celda de descarga no descarga nada | El navegador bloqueó las descargas múltiples. | Permite las descargas en el aviso del navegador, o descarga desde el panel 📁 (clic derecho → Descargar). |
| Los archivos desaparecieron | La sesión de Colab se cerró o reinició. | Es normal: vuelve a ejecutar todo y sube `file.ope`. |
| Excel muestra `38518267` en vez de `0038518267` | Excel convierte el texto a número al abrir el CSV. | El CSV está correcto; ábrelo con un editor de texto para comprobarlo. |
