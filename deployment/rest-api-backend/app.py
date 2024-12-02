from fastapi import FastAPI, HTTPException
from pathlib import Path
import script as scp
import uvicorn


# Inicializa la aplicación FastAPI
app = FastAPI()

# Define la ruta base donde se almacenan los archivos
BASE_PATH = Path("./data")

@app.get("/files/{filename}")
async def get_transfer_data():
    
    # Flujo de transferencia de datos usando funciones del script externo
    catalog_id = scp.create_catalog()  # Crea un catálogo en el proveedor de datos
    dataservice_id = scp.create_data_service(catalog_id)  # Crea un servicio de datos
    agreement_id, agreement_pid = scp.create_agreement(dataservice_id)  # Establece un acuerdo
    
    # Configuración y solicitud de transferencia
    callback_info = scp.setup_transfer()  # Configura la transferencia
    scp.request_transfer(agreement_pid, callback_info)  # Realiza la solicitud de transferencia

    # Obtiene datos del plano de datos
    data_plane_address = scp.get_data_plane_address(callback_info["consumerPid"])
    data_frame = scp.fetch_data_from_data_plane(data_plane_address)  # Descarga los datos en formato DataFrame

    # Manejo de la transferencia (suspender, reiniciar, completar)
    scp.suspend_transfer(callback_info["consumerPid"])  # Suspende la transferencia
    scp.restart_transfer(callback_info["consumerPid"])  # Reinicia la transferencia
    scp.complete_transfer(callback_info["consumerPid"])  # Completa la transferencia

    try:
        # Lee el contenido del archivo y lo devuelve
        with file_path.open("r") as file:
            content = file.read()
        return {"filename": filename, "content": content}
    except Exception as e:
        # Manejo de errores durante la lectura del archivo
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

if __name__ == "__main__":
    # Inicia el servidor Uvicorn si se ejecuta este script directamente
    uvicorn.run(app, host="0.0.0.0", port=9000)
