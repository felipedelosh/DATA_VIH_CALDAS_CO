"""
FelipedelosH

Convertir a SQL la información sobre la mortalidad por VIH en caldas
https://www.datos.gov.co/Salud-y-Protecci-n-Social/Mortalidad-VIH-2010-A-2016/yht4-twf4/about_data
"""

# Instalar python para trabajar con excel
# Abrir el terminal y ejecutar: Python -m pip install pandas
_ruta_excel = "DATA/Mortalidad_VIH_2010_A_2016_20240403.csv"

# PARTE 0
# importar la libreria pandas
import pandas as pd

# PARTE 0
# Crear el dataframe (Matriz que contiene los datos)
dataframe = pd.read_csv(_ruta_excel)

# PARTE 1
# Vamos a crear la consulta para crear la tabla
"""
Ejemplo:
CREATE TABLE IF NOT EXISTS nombreTabla (
    col_a TEXT,
    col_b TEXT,
    ...
    col_z TEXT
);
"""
_nombre_tabla = "VIH"
_SQL = f"CREATE TABLE IF NOT EXISTS {_nombre_tabla}(\n"


# Ver nombres de las cabeceras del dataframe
for columna in dataframe.columns:
    _SQL = _SQL + f" {columna} TEXT,\n"


# Borrar la ultima coma y salto de linea
_SQL = _SQL[:-2]


# Poner el cierre de consulta
_SQL = _SQL + "\n);"


# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------


# PARTE 2
# Construir la consulta para insert los datos
"""
Ejemplo:

INSERT INTO nombreTabla 
(col_a, col_b) 
VALUES 
('valor1', 'valor2');
"""

_DATOS = []

# Construir la cabecera:
# INSERT INTO nombreTabla (col_a, col_b) 
_HEAD_INSERT_SQL = f"INSERT INTO {_nombre_tabla} ("
for columna in dataframe.columns:
    _HEAD_INSERT_SQL = _HEAD_INSERT_SQL + columna + ","

# Borrar la ultima coma
_HEAD_INSERT_SQL = _HEAD_INSERT_SQL[:-1]
# Poner cierre de parentesis y keyword values
_HEAD_INSERT_SQL = _HEAD_INSERT_SQL + ") VALUES "



# Vamos a construir el resto de la consulta con un metodo
def poner_datos_en_query(cabecera_sql, datos):
    _VALUES = "("
    for i in datos:
        if str(i) == "nan":
            _VALUES = _VALUES + "\'\'" + ","
        else:
            _VALUES = _VALUES + "\'" + str(i) + "\'" + ","

    # Borrar la ultima coma
    _VALUES = _VALUES[:-1]

    # Poner el final ) y ;
    _VALUES = _VALUES + ");" 

    # Guardar
    _DATOS.append(cabecera_sql + _VALUES)

# Aqui se recorren los datos:
for indice, fila in dataframe.iterrows():
    poner_datos_en_query(_HEAD_INSERT_SQL, fila.values)


# Guardar en un archivo plano
_FINAL_SQL = ""
for i in _DATOS:
    _FINAL_SQL = _FINAL_SQL + i + "\n"


with open(f"data_{_nombre_tabla}.sql", "w", encoding="UTF-8") as f:
    f.write(_FINAL_SQL)
