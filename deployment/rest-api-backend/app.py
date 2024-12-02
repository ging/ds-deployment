from fastapi import FastAPI, HTTPException
from pathlib import Path
import script as scp
import uvicorn
import os
import json


# Inicializa la aplicación FastAPI
app = FastAPI()

# Define la ruta base donde se almacenan los archivos
BASE_PATH = Path("./data")

@app.get("/get_transfer_data")
async def get_transfer_data():
    
    # Crear el directorio 'raw_data' si no existe
    if not os.path.exists('/data/raw_data'):
        os.makedirs('/data/raw_data')
    # Flujo de transferencia de datos usando funciones del script externo
    catalog_id = scp.create_catalog()  # Crea un catálogo en el proveedor de datos
    data = [scp.create_data_servicios(catalog_id), 
            scp.create_data_service_viviendas(catalog_id),
            scp.create_data_terrenos(catalog_id)]
    
    
    for dataservice_id in data:
        
        agreement_id, agreement_pid = scp.create_agreement(dataservice_id)  # Establece un acuerdo
        
        # Configuración y solicitud de transferencia
        callback_info = scp.setup_transfer()  # Configura la transferencia
        scp.request_transfer(agreement_pid, callback_info)  # Realiza la solicitud de transferencia

        # Obtiene datos del plano de datos
        data_plane_address = scp.get_data_plane_address(callback_info["consumerPid"])
        data_frame = scp.fetch_data_from_data_plane(data_plane_address)  # Descarga los datos en formato DataFrame
        response_json = data_frame.to_json(orient="records")  # Convierte el DataFrame a JSON
        
        # Guardar el JSON en un archivo dentro de la carpeta 'raw_data'
        file_path = os.path.join('/data/raw_data', f'{dataservice_id}.json')
        with open(file_path, 'w') as f:
            json.dump(response_json, f, indent=4)
        
        # # Manejo de la transferencia (suspender, reiniciar, completar)
        # scp.suspend_transfer(callback_info["consumerPid"])  # Suspende la transferencia
        # scp.restart_transfer(callback_info["consumerPid"])  # Reinicia la transferencia
        scp.complete_transfer(callback_info["consumerPid"])  # Completa la transferencia
        



if __name__ == "__main__":
    # Inicia el servidor Uvicorn si se ejecuta este script directamente
    uvicorn.run(app, host="0.0.0.0", port=9000)
