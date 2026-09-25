# Checklist del proyecto – Python for ETL

Verificación de los entregables y del cumplimiento de cada requisito del
enunciado (`Python_ETL_Project.pdf`).

---

## 1. Entregables

| ✔ | Archivo / carpeta | Descripción |
|---|---|---|
| [x] | `main.py` | Script ETL con las secciones **EXTRACT**, **TRANSFORM** y **LOAD** separadas por comentarios. |
| [x] | `main.ipynb` | El mismo código en formato notebook, listo para **Google Colab**. |
| [x] | `server_inputs/` | Carpeta de entrada ("servidor de entrada"). |
| [x] | `server_inputs/file.ope` | Datos de entrada (idéntico al archivo original entregado). |
| [x] | `server_outputs/` | Carpeta de salida ("servidor de salida"). |
| [x] | `server_outputs/cliente.csv` | DataFrame `cliente`: 139 filas × 19 columnas. |
| [x] | `server_outputs/deuda.csv` | DataFrame `deuda`: 861 filas × 10 columnas. |
| [x] | `server_outputs/deuda.db` | Bono: base SQLite con la tabla `deuda` (861 registros). |
| [x] | `requirements.txt` | Dependencias externas: solo `pandas`. |
| [x] | `README.md` | Documentación completa del proyecto. |
| [x] | `GUIA_COLAB.md` | Paso a paso para ejecutar en Google Colab. |
| [x] | `GUIA_EJECUCION.md` | Paso a paso para ejecutar en una computadora. |
| [x] | `CHECKLIST.md` | Este documento. |
| [x] | `Python_ETL_Project.pdf` | Enunciado oficial (referencia). |

---

## 2. Requisitos del enunciado (PDF)

### 2.1 Crear el ambiente – 2 puntos
| ✔ | Requisito | Cómo se cumple |
|---|---|---|
| [x] | Carpeta `server_inputs` | Existe y contiene `file.ope`. |
| [x] | Carpeta `server_outputs` | Existe y contiene los resultados (el código la crea si no existe). |
| [x] | Archivo del proyecto `main.py` (o `main.ipynb`) | Se entregan **ambos**, con el mismo código. |
| [x] | 3 partes separadas por comentarios: EXTRACT, TRANSFORM, LOAD | En `main.py` son bloques de comentario; en `main.ipynb` son celdas con título. |

### 2.2 EXTRACT – 2 puntos
| ✔ | Requisito | Cómo se cumple |
|---|---|---|
| [x] | Leer los datos desde el servidor de entrada | Se lee `server_inputs/file.ope` (UTF-8) con una ruta relativa (`pathlib`). |
| [x] | Identificar los tipos de registro | 1001 líneas útiles: **139** de cliente (empiezan en `1`), **861** de deuda (empiezan en `2`), **1** ignorada (cabecera `Field_1`). |

### 2.3 TRANSFORM – DataFrame `cliente` – 5 puntos
| ✔ | Requisito | Cómo se cumple |
|---|---|---|
| [x] | Registros que empiezan en `1` | Se filtran por el primer carácter; el `1` se retira porque solo indica el tipo. |
| [x] | Campos separados por `\|` | `split("\|")`; se valida que cada registro tenga exactamente 19 campos. |
| [x] | Cabeceras en el orden indicado | 19 columnas: `SBSCodigoCliente` … `SBSNOMCLI2`, en el orden del PDF. |
| [x] | Resultado | **139 filas × 19 columnas**. |

### 2.4 TRANSFORM – DataFrame `deuda` – 5 puntos
| ✔ | Campo (PDF) | Posición PDF | Código Python |
|---|---|---|---|
| [x] | CodigoSBS | 1 – 10 | `datos[0:10]` |
| [x] | CodigoEmpresa | 11 – 15 | `datos[10:15]` |
| [x] | TipoCredito | 16 – 17 | `datos[15:17]` |
| [x] | Nivel2 | 18 – 19 | `datos[17:19]` |
| [x] | Moneda | 20 | `datos[19:20]` |
| [x] | SubCodigoCuenta | 21 – 31 | `datos[20:31]` |
| [x] | Condicion | 32 – 37 | `datos[31:37]` |
| [x] | ValorSaldo | 38 – 41 | `datos[37:41]` |
| [x] | ClasificacionDeuda | 42 | `datos[41:42]` |
| [x] | CodigoCuenta | Nivel2 + Moneda + SubCodigoCuenta | Unión de **texto** (14 caracteres). |

`datos` es el registro sin el `2` inicial. Resultado: **861 filas × 10 columnas**.

### 2.5 Renombrado de campos – 2 puntos
| ✔ | Antes | Después |
|---|---|---|
| [x] | `CodigoSBS` | `Cod_SBS` |
| [x] | `CodigoEmpresa` | `Cod_Emp` |
| [x] | `TipoCredito` | `Tip_Credit` |
| [x] | `ValorSaldo` | `Val_Saldo` |
| [x] | `ClasificacionDeuda` | `Clasif_Deu` |
| [x] | `CodigoCuenta` | `Cod_Cuenta` |

Columnas finales: `Cod_SBS, Cod_Emp, Tip_Credit, Nivel2, Moneda,
SubCodigoCuenta, Condicion, Val_Saldo, Clasif_Deu, Cod_Cuenta`.

### 2.6 LOAD – 2 puntos
| ✔ | Requisito | Cómo se cumple |
|---|---|---|
| [x] | Guardar los DataFrames en `server_outputs` | `cliente.csv` y `deuda.csv`, con `index=False` y codificación `utf-8-sig` (compatible con Excel). |

### 2.7 Bono: SQLite – 2 puntos
| ✔ | Requisito | Cómo se cumple |
|---|---|---|
| [x] | Guardar la deuda en SQLite | `server_outputs/deuda.db`, tabla `deuda`, con `sqlite3` + `to_sql(if_exists="replace")`. |
| [x] | Verificación | `SELECT COUNT(*) FROM deuda` = **861** = filas del DataFrame. |

---

## 3. Calidad y buenas prácticas

| ✔ | Aspecto | Detalle |
|---|---|---|
| [x] | Rutas portables | Sin rutas absolutas; todo se construye desde la carpeta del proyecto. |
| [x] | Compatible con Google Colab | `main.ipynb` sube `file.ope`, ejecuta el ETL y descarga los resultados. |
| [x] | Ceros iniciales conservados | Todo se maneja como texto: `0038518267` se mantiene así en DataFrames, CSV y SQLite. |
| [x] | Reproducible | Se puede ejecutar varias veces: los CSV se sobrescriben y SQLite no duplica registros. |
| [x] | Validaciones en el código | 10 validaciones que muestran `[OK]` (ver sección 4). |
| [x] | Código para principiantes | Sin clases ni estructuras avanzadas; comentarios en español. |
| [x] | Dependencias mínimas | Solo `pandas` (`sqlite3` y `pathlib` vienen con Python). |

---

## 4. Validaciones que ejecuta el programa

| # | Validación | Resultado |
|---|---|---|
| 1 | Existe `file.ope` | [OK] |
| 2 | Hay registros de cliente | [OK] 139 |
| 3 | Hay registros de deuda | [OK] 861 |
| 4 | `cliente` tiene las 19 columnas en orden y una fila por registro | [OK] |
| 5 | `deuda` tiene las 10 columnas finales y una fila por registro | [OK] |
| 6 | Los códigos SBS conservan sus 10 dígitos (ceros iniciales) | [OK] |
| 7 | `Cod_Cuenta` = Nivel2 + Moneda + SubCodigoCuenta | [OK] |
| 8 | `cliente.csv` y `deuda.csv` existen y coinciden con los DataFrames | [OK] |
| 9 | `deuda.db` existe con la tabla `deuda` | [OK] |
| 10 | Registros en SQLite = filas del DataFrame `deuda` | [OK] 861 = 861 |

---

## 5. Pruebas realizadas antes de la entrega

| ✔ | Prueba | Resultado |
|---|---|---|
| [x] | `python main.py` con Python 3.11 + pandas 3.0 | Correcto |
| [x] | `python main.py` con Python 3.12 + pandas 2.2.2 (versiones de Colab) | Correcto |
| [x] | Ejecutar desde otra carpeta y dos veces seguidas | Correcto, mismos resultados |
| [x] | `main.ipynb` en un entorno que simula Colab (carpeta vacía + subida de `file.ope`) | Correcto; en la 2ª ejecución no vuelve a pedir el archivo |
| [x] | Resultados de todas las ejecuciones | CSV idénticos byte a byte |
| [x] | Comparación con un cálculo independiente desde `file.ope` | 139 clientes y 861 deudas idénticos |
| [x] | Cada `Cod_SBS` de deuda existe en `cliente` | Correcto (confirma las posiciones) |
| [x] | SQLite: tabla, columnas (TEXT) y filas iguales a `deuda.csv` | Correcto |

---

## 6. Observaciones documentadas

- **Longitud de los registros de deuda:** cada registro mide 55 caracteres
  (54 sin el `2`), pero el PDF solo define hasta el carácter 42. Quedan
  **12 caracteres sin especificar**, que no se usan (se respetó el PDF).
  Detalle y ejemplos en el `README.md`, sección 9.
- **Identificador de tipo:** el `1` / `2` inicial se retira antes de obtener
  los campos; así los códigos SBS de deuda coinciden con los de cliente.
- **Carácter `¿`** en algunos nombres (ej. `LOUREN¿S`): viene así en el
  archivo original; no es un error de lectura.
- **Excel** puede ocultar los ceros iniciales al abrir un CSV con doble clic;
  el archivo sí los conserva.
