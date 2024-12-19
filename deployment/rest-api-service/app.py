from fastapi import FastAPI, HTTPException
from pathlib import Path

app = FastAPI()

# Ruta base donde se encuentran los archivos JSON
BASE_PATH = Path("./data")

# Archivos JSON específicos
VIVIENDAS_FILE = BASE_PATH / "Datos_Viviendas_Madrid.json"
SERVICIOS_FILE = BASE_PATH / "Servicios_Madrid.json"
TERRENOS_FILE = BASE_PATH / "Terrenos_Libres_Poligonos_Madrid.json"

# Endpoint para viviendas
@app.get("/viviendas")
async def get_viviendas():
    return read_file(VIVIENDAS_FILE)

# Endpoint para servicios
@app.get("/servicios")
async def get_servicios():
    return read_file(SERVICIOS_FILE)

# Endpoint para terrenos
@app.get("/terrenos")
async def get_terrenos():
    return read_file(TERRENOS_FILE)

# Función para leer archivos
def read_file(file_path: Path):
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"File not found: {file_path.name}")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            content = file.read()
        return {"filename": file_path.name, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
