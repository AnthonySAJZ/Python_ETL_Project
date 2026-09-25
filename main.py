"""
Proyecto Final - Python for ETL

Lee el archivo server_inputs/file.ope, genera dos DataFrames (cliente y deuda)
y los guarda en la carpeta server_outputs (CSV + base de datos SQLite).

Ejecución:
    python main.py
"""

from pathlib import Path
import sqlite3

import pandas as pd


# ============================================================================
# CONFIGURACIÓN: rutas y nombres de columnas
# ============================================================================

# Carpeta donde está este archivo main.py. Todas las rutas se construyen a
# partir de ella, así el proyecto funciona en cualquier computadora.
CARPETA_PROYECTO = Path(__file__).resolve().parent

CARPETA_ENTRADA = CARPETA_PROYECTO / "server_inputs"
CARPETA_SALIDA = CARPETA_PROYECTO / "server_outputs"

ARCHIVO_ENTRADA = CARPETA_ENTRADA / "file.ope"
ARCHIVO_CLIENTE_CSV = CARPETA_SALIDA / "cliente.csv"
ARCHIVO_DEUDA_CSV = CARPETA_SALIDA / "deuda.csv"
ARCHIVO_DEUDA_DB = CARPETA_SALIDA / "deuda.db"

# Columnas del DataFrame cliente (en el orden indicado por el enunciado)
COLUMNAS_CLIENTE = [
    "SBSCodigoCliente", "SBSFechaReporte", "SBSTipoDocumentoT",
    "SBSRucCliente", "SBSTipoDocumento", "SBSNumeroDocumento",
    "SBSTipoPer", "SBSTipoEmpresa", "SBSNumeroEntidad", "SBSSalNor",
    "SBSSalCPP", "SBSSalDEF", "SBSSalDUD", "SBSSalAPER", "SBSAPEPAT",
    "SBSAPEMAT", "SBSAPECAS", "SBSNOMCLI", "SBSNOMCLI2",
]

# Columnas finales del DataFrame deuda (después del renombrado)
COLUMNAS_DEUDA_FINAL = [
    "Cod_SBS", "Cod_Emp", "Tip_Credit", "Nivel2", "Moneda",
    "SubCodigoCuenta", "Condicion", "Val_Saldo", "Clasif_Deu", "Cod_Cuenta",
]

SEPARADOR = "=" * 50


def validar(condicion, descripcion):
    """Muestra [OK] si la condición se cumple; si no, detiene el programa."""
    if condicion:
        print(f"  [OK] {descripcion}")
    else:
        raise ValueError(f"VALIDACIÓN FALLIDA: {descripcion}")


print(SEPARADOR)
print("PROYECTO ETL - file.ope")
print(SEPARADOR)


# ============================================================================
# EXTRACT: leer los datos desde el servidor de entrada (server_inputs)
# ============================================================================
print("\nEXTRACT")

# Validación 1: el archivo de entrada debe existir
validar(ARCHIVO_ENTRADA.exists(), f"Existe el archivo {ARCHIVO_ENTRADA.name}")

# El archivo está codificado en UTF-8 (tiene letras como Ñ, Ó, Ú)
with open(ARCHIVO_ENTRADA, encoding="utf-8") as archivo:
    todas_las_lineas = archivo.read().splitlines()

# Quitamos las líneas vacías
lineas_utiles = [linea for linea in todas_las_lineas if linea.strip() != ""]

# Separamos las líneas según su primer carácter:
#   "1" -> registro de cliente
#   "2" -> registro de deuda
#   otro -> se ignora (por ejemplo, la cabecera "Field_1")
registros_cliente = []
registros_deuda = []
lineas_ignoradas = []

for linea in lineas_utiles:
    if linea.startswith("1"):
        registros_cliente.append(linea)
    elif linea.startswith("2"):
        registros_deuda.append(linea)
    else:
        lineas_ignoradas.append(linea)

print(f"  Total de líneas útiles leídas: {len(lineas_utiles)}")
print(f"  Registros de cliente (empiezan en 1): {len(registros_cliente)}")
print(f"  Registros de deuda (empiezan en 2): {len(registros_deuda)}")
print(f"  Líneas ignoradas: {len(lineas_ignoradas)} {lineas_ignoradas}")

# Validaciones 2 y 3: se encontraron clientes y deudas
validar(len(registros_cliente) > 0, "Se encontraron registros de cliente")
validar(len(registros_deuda) > 0, "Se encontraron registros de deuda")


# ============================================================================
# TRANSFORM: construir los DataFrames cliente y deuda
# ============================================================================
print("\nTRANSFORM")

# ---------------------------------------------------------------------------
# DataFrame cliente
# ---------------------------------------------------------------------------
# El primer carácter ("1") solo indica el tipo de registro, por eso se quita.
# Ejemplo: "10038518267|20200930|..." -> SBSCodigoCliente = "0038518267"
# Luego se separan los campos usando el carácter "|".
filas_cliente = []

for numero, registro in enumerate(registros_cliente, start=1):
    campos = registro[1:].split("|")

    # Validación 4: cada registro debe tener exactamente 19 campos
    if len(campos) != len(COLUMNAS_CLIENTE):
        raise ValueError(
            f"El cliente N° {numero} tiene {len(campos)} campos "
            f"(se esperaban {len(COLUMNAS_CLIENTE)}): {registro}"
        )
    filas_cliente.append(campos)

# Todos los valores se guardan como texto para no perder ceros iniciales
cliente = pd.DataFrame(filas_cliente, columns=COLUMNAS_CLIENTE)

# ---------------------------------------------------------------------------
# DataFrame deuda
# ---------------------------------------------------------------------------
# Los campos son de ancho fijo. Igual que en cliente, se quita el primer
# carácter ("2") que solo indica el tipo de registro. Así, el carácter 1
# del enunciado es el primer carácter del código SBS.
#
# Python cuenta desde 0 y el final del slice NO se incluye, por lo tanto:
#   "del caracter 1 al 10"  ->  datos[0:10]
#   "del caracter 11 al 15" ->  datos[10:15]   ... y así sucesivamente.
filas_deuda = []

for registro in registros_deuda:
    datos = registro[1:]
    fila = {
        "CodigoSBS": datos[0:10],           # caracteres 1 al 10
        "CodigoEmpresa": datos[10:15],      # caracteres 11 al 15
        "TipoCredito": datos[15:17],        # caracteres 16 al 17
        "Nivel2": datos[17:19],             # caracteres 18 al 19
        "Moneda": datos[19:20],             # caracter 20
        "SubCodigoCuenta": datos[20:31],    # caracteres 21 al 31
        "Condicion": datos[31:37],          # caracteres 32 al 37
        "ValorSaldo": datos[37:41],         # caracteres 38 al 41
        "ClasificacionDeuda": datos[41:42], # caracter 42
    }
    filas_deuda.append(fila)

deuda = pd.DataFrame(filas_deuda)

# CodigoCuenta = Nivel2 + Moneda + SubCodigoCuenta (unión de TEXTO, no suma)
deuda["CodigoCuenta"] = deuda["Nivel2"] + deuda["Moneda"] + deuda["SubCodigoCuenta"]

# Renombrado de columnas pedido por el enunciado
deuda = deuda.rename(columns={
    "CodigoSBS": "Cod_SBS",
    "CodigoEmpresa": "Cod_Emp",
    "TipoCredito": "Tip_Credit",
    "ValorSaldo": "Val_Saldo",
    "ClasificacionDeuda": "Clasif_Deu",
    "CodigoCuenta": "Cod_Cuenta",
})

print(f"  DataFrame cliente: {cliente.shape[0]} filas x {cliente.shape[1]} columnas")
print(f"  DataFrame deuda:   {deuda.shape[0]} filas x {deuda.shape[1]} columnas")

# Validación 4: columnas de cliente
validar(list(cliente.columns) == COLUMNAS_CLIENTE,
        "cliente tiene las 19 columnas en el orden correcto")
validar(len(cliente) == len(registros_cliente),
        "cliente tiene una fila por cada registro que empieza en 1")

# Validación 5: columnas de deuda
validar(list(deuda.columns) == COLUMNAS_DEUDA_FINAL,
        "deuda tiene las 10 columnas finales (con los 6 renombrados)")
validar(len(deuda) == len(registros_deuda),
        "deuda tiene una fila por cada registro que empieza en 2")

# Validación 6: no se pierden los ceros iniciales (los códigos miden 10)
validar(cliente["SBSCodigoCliente"].str.len().eq(10).all()
        and deuda["Cod_SBS"].str.len().eq(10).all(),
        "Los códigos SBS conservan sus 10 dígitos (ceros iniciales incluidos)")

# Validación 7: Cod_Cuenta está bien construido.
# Nivel2, Moneda y SubCodigoCuenta están juntos en el archivo (caracteres
# 18 al 31), así que Cod_Cuenta debe ser igual a ese tramo del registro.
tramo_original = [registro[1:][17:31] for registro in registros_deuda]
validar(list(deuda["Cod_Cuenta"]) == tramo_original,
        "Cod_Cuenta = Nivel2 + Moneda + SubCodigoCuenta (14 caracteres)")

# Observación: el enunciado define 42 caracteres, pero los registros reales
# de deuda son más largos. Esos caracteres extra no se usan (ver README).
longitud_maxima = max(len(registro[1:]) for registro in registros_deuda)
print(f"  Observación: los registros de deuda tienen hasta {longitud_maxima} caracteres "
      f"(sin el '2'); el enunciado solo define los primeros 42.")


# ============================================================================
# LOAD: guardar los DataFrames en el servidor de salida (server_outputs)
# ============================================================================
print("\nLOAD")

CARPETA_SALIDA.mkdir(exist_ok=True)

# Archivos CSV ("utf-8-sig" permite que Excel muestre bien las tildes y la Ñ)
cliente.to_csv(ARCHIVO_CLIENTE_CSV, index=False, encoding="utf-8-sig")
deuda.to_csv(ARCHIVO_DEUDA_CSV, index=False, encoding="utf-8-sig")

# Validación 8: los CSV existen y tienen el mismo contenido que los DataFrames.
# Se leen como texto (dtype=str) para comprobar que los ceros se conservan.
for archivo_csv, dataframe in [(ARCHIVO_CLIENTE_CSV, cliente),
                               (ARCHIVO_DEUDA_CSV, deuda)]:
    validar(archivo_csv.exists() and archivo_csv.stat().st_size > 0,
            f"{archivo_csv.name} creado y no está vacío")
    csv_leido = pd.read_csv(archivo_csv, dtype=str, keep_default_na=False,
                            encoding="utf-8-sig")
    validar(list(csv_leido.columns) == list(dataframe.columns)
            and len(csv_leido) == len(dataframe)
            and csv_leido.values.tolist() == dataframe.values.tolist(),
            f"{archivo_csv.name}: {len(csv_leido)} filas, columnas y datos correctos")

# BONO: guardar la deuda en una base de datos SQLite.
# if_exists="replace" evita duplicar registros si se ejecuta el ETL otra vez.
conexion = sqlite3.connect(ARCHIVO_DEUDA_DB)
deuda.to_sql("deuda", conexion, if_exists="replace", index=False)

cantidad_sqlite = conexion.execute("SELECT COUNT(*) FROM deuda").fetchone()[0]
primer_codigo_sqlite = conexion.execute("SELECT Cod_SBS FROM deuda LIMIT 1").fetchone()[0]
conexion.close()

# Validaciones 9 y 10: la base existe y tiene la misma cantidad de filas
validar(ARCHIVO_DEUDA_DB.exists(), f"{ARCHIVO_DEUDA_DB.name} creado con la tabla deuda")
validar(cantidad_sqlite == len(deuda),
        f"Registros en SQLite ({cantidad_sqlite}) = filas del DataFrame deuda ({len(deuda)})")
validar(primer_codigo_sqlite == deuda.loc[0, "Cod_SBS"],
        f"SQLite conserva los ceros iniciales (primer Cod_SBS = {primer_codigo_sqlite})")


print("\n" + SEPARADOR)
print("ETL FINALIZADO CORRECTAMENTE")
print(SEPARADOR)
