# Proyecto Final – Python for ETL

Proceso ETL (**E**xtract → **T**ransform → **L**oad) escrito en Python que toma
los datos del "servidor de entrada" (`server_inputs`), los transforma en dos
tablas (`cliente` y `deuda`) y los guarda en el "servidor de salida"
(`server_outputs`).

El enunciado oficial está en `Python_ETL_Project.pdf`.

---

## 1. Requisitos

- **Python 3.9 o superior** (probado con Python 3.11).
- La librería **pandas** (probado con pandas 2.3 y 3.0).

`pathlib` y `sqlite3` ya vienen incluidos con Python, no hay que instalarlos.

## 2. Instalación

Desde la carpeta del proyecto, ejecutar:

```bash
python -m pip install -r requirements.txt
```

## 3. Estructura del proyecto

```
Python_ETL_Project/
│
├── main.py                  -> programa principal (EXTRACT, TRANSFORM, LOAD)
├── requirements.txt         -> librerías externas necesarias (pandas)
├── README.md                -> este documento
├── Python_ETL_Project.pdf   -> enunciado del proyecto
│
├── server_inputs/           -> "servidor de entrada": aquí están los datos originales
│   └── file.ope             -> archivo con los registros de clientes y deudas
│
└── server_outputs/          -> "servidor de salida": aquí se guardan los resultados
    ├── cliente.csv          -> tabla de clientes
    ├── deuda.csv            -> tabla de deudas
    └── deuda.db             -> base de datos SQLite con la tabla "deuda" (bono)
```

| Elemento | Para qué sirve |
|---|---|
| `main.py` | Contiene todo el proceso ETL, dividido con comentarios en EXTRACT, TRANSFORM y LOAD. |
| `server_inputs` | Carpeta de entrada. Simula el servidor desde donde se leen los datos. |
| `server_outputs` | Carpeta de salida. Simula el servidor donde se dejan los resultados. Si no existe, `main.py` la crea. |
| `file.ope` | Archivo de texto con los datos. Las líneas que empiezan en `1` son clientes y las que empiezan en `2` son deudas. |
| `cliente.csv` | Resultado: el DataFrame `cliente` (19 columnas). |
| `deuda.csv` | Resultado: el DataFrame `deuda` (10 columnas). |
| `deuda.db` | Resultado del bono: base de datos SQLite con la tabla `deuda`. |

## 4. Ejecución

Desde la carpeta del proyecto:

```bash
python main.py
```

Las rutas se calculan a partir de la carpeta donde está `main.py`
(`Path(__file__).resolve().parent`), por lo que el proyecto se puede copiar a
otra computadora y ejecutar sin cambiar nada. El programa puede ejecutarse
todas las veces que se quiera: los archivos de salida se reemplazan y no se
duplican registros.

Salida esperada (resumida):

```
EXTRACT
  [OK] Existe el archivo file.ope
  Total de líneas útiles leídas: 1001
  Registros de cliente (empiezan en 1): 139
  Registros de deuda (empiezan en 2): 861
  Líneas ignoradas: 1 ['Field_1']
TRANSFORM
  DataFrame cliente: 139 filas x 19 columnas
  DataFrame deuda:   861 filas x 10 columnas
LOAD
  [OK] cliente.csv: 139 filas, columnas y datos correctos
  [OK] deuda.csv: 861 filas, columnas y datos correctos
  [OK] Registros en SQLite (861) = filas del DataFrame deuda (861)
ETL FINALIZADO CORRECTAMENTE
```

## 5. Explicación del ETL

### EXTRACT (extraer)
Se abre `server_inputs/file.ope` (codificación UTF-8) y se leen todas sus
líneas. Se descartan las líneas vacías y se separan según el primer carácter:

- `1` → registro de **cliente**
- `2` → registro de **deuda**
- cualquier otro → se ignora (en este archivo solo la cabecera `Field_1`)

### TRANSFORM (transformar)

**DataFrame `cliente`**
1. Se quita el primer carácter (`1`), que solo indica el tipo de registro.
2. Se separan los campos con `|`.
3. Se comprueba que cada registro tenga exactamente 19 campos.
4. Se crea el DataFrame con las 19 columnas del enunciado
   (`SBSCodigoCliente` … `SBSNOMCLI2`).

Ejemplo: `10038518267|20200930|...` → `SBSCodigoCliente = "0038518267"`.

**DataFrame `deuda`**
1. Se quita el primer carácter (`2`).
2. Se "cortan" los campos por posición (ancho fijo). Como Python cuenta desde
   0 y el final del corte no se incluye, "del carácter 1 al 10" se escribe
   `datos[0:10]`:

   | Campo | Caracteres (PDF) | Código Python |
   |---|---|---|
   | CodigoSBS | 1 – 10 | `datos[0:10]` |
   | CodigoEmpresa | 11 – 15 | `datos[10:15]` |
   | TipoCredito | 16 – 17 | `datos[15:17]` |
   | Nivel2 | 18 – 19 | `datos[17:19]` |
   | Moneda | 20 | `datos[19:20]` |
   | SubCodigoCuenta | 21 – 31 | `datos[20:31]` |
   | Condicion | 32 – 37 | `datos[31:37]` |
   | ValorSaldo | 38 – 41 | `datos[37:41]` |
   | ClasificacionDeuda | 42 | `datos[41:42]` |

3. Se crea `CodigoCuenta = Nivel2 + Moneda + SubCodigoCuenta`
   (unión de **texto**, no una suma).
4. Se renombran las columnas:
   `CodigoSBS → Cod_SBS`, `CodigoEmpresa → Cod_Emp`, `TipoCredito → Tip_Credit`,
   `ValorSaldo → Val_Saldo`, `ClasificacionDeuda → Clasif_Deu`,
   `CodigoCuenta → Cod_Cuenta`.

Columnas finales de `deuda`: `Cod_SBS, Cod_Emp, Tip_Credit, Nivel2, Moneda,
SubCodigoCuenta, Condicion, Val_Saldo, Clasif_Deu, Cod_Cuenta`.

Todos los valores se manejan como **texto** para no perder los ceros
iniciales (por ejemplo `0038518267`).

### LOAD (cargar)
- `cliente` se guarda en `server_outputs/cliente.csv`.
- `deuda` se guarda en `server_outputs/deuda.csv`.
- Se usa `index=False` (sin columna de índice) y la codificación `utf-8-sig`,
  para que Excel muestre correctamente las tildes y la Ñ.
- Luego se vuelven a leer los CSV para comprobar que el contenido es igual al
  de los DataFrames.

## 6. Resultados (ejecución real)

| Dato | Valor |
|---|---|
| Líneas útiles leídas | 1001 |
| Registros de cliente | **139** |
| Registros de deuda | **861** |
| Líneas ignoradas | 1 (la cabecera `Field_1`) |
| DataFrame `cliente` | 139 filas × 19 columnas |
| DataFrame `deuda` | 861 filas × 10 columnas |
| Registros en SQLite | 861 |

## 7. SQLite (bono)

Además de los CSV, la deuda se guarda en una base de datos SQLite:

```python
conexion = sqlite3.connect(ARCHIVO_DEUDA_DB)
deuda.to_sql("deuda", conexion, if_exists="replace", index=False)
```

- Archivo: `server_outputs/deuda.db`, tabla: `deuda`.
- `if_exists="replace"` reemplaza la tabla en cada ejecución, así no se
  duplican registros.
- Después se ejecuta `SELECT COUNT(*) FROM deuda` y se comprueba que el
  resultado (861) sea igual al número de filas del DataFrame.
- Las columnas se guardan como `TEXT`, por lo que también conservan los
  ceros iniciales.

## 8. Validaciones incluidas en `main.py`

Cada validación muestra `[OK]` en la consola; si alguna falla, el programa se
detiene con un mensaje claro.

1. El archivo `file.ope` existe.
2. Hay registros de cliente.
3. Hay registros de deuda.
4. Cada cliente tiene 19 campos y el DataFrame tiene las 19 columnas en orden.
5. El DataFrame `deuda` tiene las 10 columnas finales (con los renombrados).
6. Los códigos SBS conservan sus 10 dígitos (no se pierden ceros iniciales).
7. `Cod_Cuenta` coincide con los caracteres 18 al 31 del registro original
   (que son justamente Nivel2 + Moneda + SubCodigoCuenta).
8. `cliente.csv` y `deuda.csv` existen, no están vacíos y al releerlos tienen
   las mismas columnas, filas y datos.
9. `deuda.db` existe con la tabla `deuda`.
10. `SELECT COUNT(*)` en SQLite = filas del DataFrame `deuda`.

## 9. Observaciones

### 9.1 Los registros de deuda son más largos que lo definido en el PDF

- Cada registro de deuda mide **55 caracteres** (todos iguales).
- Sin el identificador inicial `2` quedan **54 caracteres**.
- El PDF solo define los caracteres **1 al 42**.
- Por lo tanto, **quedan 12 caracteres al final de cada registro sin
  especificar** (caracteres 43 al 54).

Se aplicaron las posiciones **tal como indica el PDF**; los 12 caracteres
finales no se usan y no se inventaron columnas para ellos.

Ejemplos (sin modificar):

```
Registro original:  2003851826700145111415030202000001490000000000001100904
Sin el "2":          003851826700145111415030202000001490000000000001100904
Caracteres 1-42:     003851826700145111415030202000001490000000
Sin especificar:                                               000001100904

Registro original:  2003851826700140118113020000000004270000000000000543604
Caracteres 1-42:     003851826700140118113020000000004270000000
Sin especificar:                                               000000543604
```

### 9.2 ¿Por qué se quita el primer carácter (`1` o `2`)?

El PDF dice que los registros "empiezan en 1" o "empiezan en 2", es decir,
ese carácter identifica el tipo de registro. Al quitarlo:

- el primer campo del cliente queda con 10 dígitos (`0038518267`), y
- los caracteres 1 al 10 de cada deuda (`0038518267`) coinciden con el código
  de un cliente.

Se comprobó que **los 861 códigos SBS de deuda existen en la tabla cliente**,
lo que confirma que las posiciones se cuentan después del identificador.

### 9.3 Otras observaciones de los datos

- El archivo tiene una cabecera `Field_1` que se ignora.
- En los 15 clientes persona natural (`SBSTipoPer = 1`), `SBSAPEPAT` viene
  vacío y el apellido aparece en `SBSAPEMAT` (ej. `||BAUTISTA||JUANA|`). En
  las 124 empresas (`SBSTipoPer = 2`) la razón social está en `SBSAPEPAT`.
  Se respetó el orden de columnas del PDF sin mover datos.
- Algunos nombres de empresa traen comillas y el carácter `¿`
  (ej. `LOUREN¿S`). Ese `¿` ya está así en el archivo original; no es un
  error de lectura, por lo que no se modificó.
- Si se abre un CSV haciendo doble clic en Excel, Excel puede mostrar
  `0038518267` como `38518267` porque lo interpreta como número. El archivo
  CSV sí guarda los ceros (se puede ver abriéndolo con un editor de texto o
  importándolo en Excel como texto).
