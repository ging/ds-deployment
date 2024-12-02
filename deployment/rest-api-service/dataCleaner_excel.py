import pandas as pd

# Ruta del archivo original
input_file = "Datos_Viviendas_Madrid.xlsx"
output_file = "Viviendas_Format.xlsx"

# Leer el archivo original
df = pd.read_excel(input_file)

# Asegurarse de que las columnas están correctamente organizadas
columns = [
    "ID_Vivienda", "Coordenadas", "Fecha_Compra", "Fecha_Venta",
    "Precio_Compra (€)", "Precio_Venta (€)", "Superficie (m²)",
    "Habitaciones", "Baños", "Tipo", "Distrito"
]

# Verificar y reorganizar las columnas si es necesario
df = df[columns]

# Guardar en un nuevo archivo Excel con el formato solicitado
df.to_excel(output_file, index=False)

print(f"El archivo se ha formateado y guardado como: {output_file}")
