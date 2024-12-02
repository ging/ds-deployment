from fastapi import FastAPI, HTTPException
from pathlib import Path

app = FastAPI()

BASE_PATH = Path("./data")  # Directorio donde se almacenan los archivos

@app.get("/files/{filename}")
async def get_file_content(filename: str):
    file_path = BASE_PATH / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with file_path.open("r") as file:
            content = file.read()
        return {"filename": filename, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)