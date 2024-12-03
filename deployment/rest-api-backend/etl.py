import pandas as pd
import json
import geopandas as gpd
from shapely.geometry import Point, Polygon

def cruzar_viviendas_y_servicios():
    viviendas_path = '/data/raw_data/viviendas.csv'   
    servicios_path = '/data/raw_data/servicios.csv'   

    # Parse the CSV string into a DataFrame
    viviendas_df = pd.read_csv(viviendas_path, sep=',')
    servicios_df = pd.read_csv(servicios_path, sep=',')

    # Display the first few rows of the DataFrame
    
    # Contar los servicios por ubicación y categoría
    servicios_count = servicios_df.groupby(['Coordenadas', 'Tipo_de_Servicio']).size().reset_index(name='Cantidad')

    # Pivotar los datos para tener una columna por tipo de servicio
    servicios_pivot = servicios_count.pivot(index='Coordenadas', columns='Tipo_de_Servicio', values='Cantidad').fillna(0)
    servicios_pivot = servicios_pivot.reset_index()

    
    # Combinar con las viviendas
    resultado = viviendas_df.merge(servicios_pivot, how='left', on='Coordenadas')
    resultado.fillna(0, inplace=True)  # Rellenar valores faltantes con 0
    
    # Guardar el resultado en un archivo CSV 
    resultado_path = '/data/staging_data/viviendas_con_servicios.json'
    resultado.to_json(resultado_path, index=False)
    print("Resultado de viviendas guardado en:", resultado_path)
    

def cruzar_terrenos_y_servicios():

    terrenos_path = '/data/raw_data/terrenos.csv'   
    servicios_path = '/data/raw_data/servicios.csv' 

    terrenos_df = pd.read_csv(terrenos_path)
    servicios_df = pd.read_csv(servicios_path)

    # Validar columnas necesarias
    if 'Nodos' not in terrenos_df.columns or 'Coordenadas' not in servicios_df.columns:
        raise ValueError("El archivo de terrenos debe contener 'Nodos' y el de servicios debe contener 'Coordenadas'.")
    if 'Tipo_de_Servicio' not in servicios_df.columns:
        raise ValueError("El archivo de servicios debe contener la columna 'Categoría'.")

    # Convertir coordenadas de terrenos a polígonos
    terrenos_df['geometry'] = terrenos_df['Nodos'].apply(
        lambda coords: Polygon(eval(coords)) if isinstance(coords, str) else None
    )
    terrenos_gdf = gpd.GeoDataFrame(terrenos_df, geometry='geometry', crs='EPSG:4326')

    # Convertir ubicaciones de servicios a puntos
    servicios_df['geometry'] = servicios_df['Coordenadas'].apply(
        lambda loc: Point(eval(loc)) if isinstance(loc, str) else None
    )
    servicios_gdf = gpd.GeoDataFrame(servicios_df, geometry='geometry', crs='EPSG:4326')

    # Verificar intersecciones entre terrenos y servicios
    servicios_in_terrenos = gpd.sjoin(servicios_gdf, terrenos_gdf, how='inner', predicate='within')

    # Contar servicios por categoría para cada terreno
    servicios_count = servicios_in_terrenos.groupby(['ID_Servicio', 'Tipo_de_Servicio']).size().reset_index(name='Cantidad')

    # Pivotar para crear una columna por categoría de servicio
    servicios_pivot = servicios_count.pivot(index='ID_Servicio', columns='Tipo_de_Servicio', values='Cantidad').fillna(0)

    # Unir con los terrenos originales
    resultado = terrenos_gdf.merge(servicios_pivot, how='left', left_on='ID_Terreno', right_index=True)
    resultado.fillna(0, inplace=True)  # Rellenar valores faltantes con 0
    
    # Guardar el resultado en un archivo json
    # Generar el GeoJSON como string
    geojson_data = resultado.to_json()

    # Guardar el GeoJSON en un archivo
    resultado_path = '/data/staging_data/terrenos_con_servicios.json'
    with open(resultado_path, 'w') as file:
        file.write(geojson_data)
    print("Resultado de terrenos guardado en:", resultado_path)