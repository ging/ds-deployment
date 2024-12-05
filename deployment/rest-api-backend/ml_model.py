import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import os
import json


def generate_viviendas_con_nota():
    # Cargar los datos
    file_path = '/data/staging_data/viviendas_con_servicios.json'
    df = pd.read_json(file_path)

    # Seleccionar las columnas relevantes
    features = ['Precio_Compra (€)', 'Precio_Venta (€)', 'Superficie (m²)', 'Habitaciones', 'Baños', 
                'Centro Comercial', 'Colegio', 'Estación de Metro', 'Hospital', 'Parque', 'Supermercado']
    target_column = 'Nota'

    # Generar una columna objetivo ficticia (Nota) para entrenar el modelo
    # Suponiendo que esta columna no existe aún, la simulamos como promedio ponderado
    df[target_column] = np.random.uniform(5, 10, size=len(df))  # Crear puntuaciones simuladas

    # Dividir los datos
    X = df[features]
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar un modelo
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluar el modelo
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    # Generar las predicciones para todo el conjunto de datos
    df['Prediccion_Nota'] = model.predict(df[features])
    # # Guardar el nuevo dataset
    output_dir = '/data/model_data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'viviendas_con_notas.json')
    df.to_json(output_file, orient='records', indent=4)
    
def get_viviendas_con_nota():
    file_path = '/data/model_data/viviendas_con_notas.json'   
    with open(file_path, 'r') as file:
        resultado = json.load(file)
        
    print("Resultado de vivendas guardado en:", resultado)
    return resultado