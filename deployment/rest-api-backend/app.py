import pprint
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
    catalog_id = scp.create_catalog()# Crea un catálogo en el proveedor de datos
    pprint.pprint("prubea 1:")
    # pprint(scp.create_data_servicios(catalog_id))
    data = {
        "servicios": scp.create_data_servicios(catalog_id),
        "viviendas": scp.create_data_service_viviendas(catalog_id),
        "terrenos": scp.create_data_terrenos(catalog_id)
    }
    
    pprint.pprint("data: " + "".join(data), indent=4)
    
    for clave in data:
        pprint.pprint("clave: "+ clave)
        dataservice_id = data[clave]
        agreement_id, agreement_pid = scp.create_agreement(dataservice_id)  # Establece un acuerdo
        
        # Configuración y solicitud de transferencia
        callback_info = scp.setup_transfer()  # Configura la transferencia
        scp.request_transfer(agreement_pid, callback_info)  # Realiza la solicitud de transferencia

        # Obtiene datos del plano de datos
        data_plane_address = scp.get_data_plane_address(callback_info["consumerPid"])
        data_frame = scp.fetch_data_from_data_plane(data_plane_address)  # Descarga los datos en formato DataFrame
        # response_json = data_frame.to_json(orient="records")  # Convierte el DataFrame a JSON
        pprint.pprint("data_frame en la API: ")
        pprint.pprint(data_frame)
                
        file_path = os.path.join('/data/raw_data', f'{clave}.json')
        pprint.pprint("file_path donde guardamos el df:")
        pprint.pprint(file_path)
        data_frame.to_csv(file_path, index=False)
        
        # # Manejo de la transferencia (suspender, reiniciar, completar)
        # scp.suspend_transfer(callback_info["consumerPid"])  # Suspende la transferencia
        # scp.restart_transfer(callback_info["consumerPid"])  # Reinicia la transferencia
        scp.complete_transfer(callback_info["consumerPid"])  # Completa la transferencia
        



if __name__ == "__main__":
    # Inicia el servidor Uvicorn si se ejecuta este script directamente
    uvicorn.run(app, host="0.0.0.0", port=9000)
