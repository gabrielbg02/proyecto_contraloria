from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")  # Asegúrate de tener una carpeta "templates" con tu formulario.html

# Ruta para mostrar el formulario
@app.get("/", response_class=HTMLResponse)
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

# Ruta para procesar el formulario
@app.post("/data-processing")
async def procesar_formulario(request: Request, datos: dict = Form(...)):
    # Convertir los datos a un formato legible
    datos_guardar = "\n".join([f"{key}: {value}" for key, value in datos.items()])

    # Guardar los datos en un archivo
    ruta_archivo = os.path.join(os.getcwd(), 'datos_formulario.txt')
    with open(ruta_archivo, 'a') as archivo:
        archivo.write(datos_guardar + "\n\n")

    return "Datos guardados correctamente"

# Para ejecutar el servidor, puedes usar uvicorn desde la línea de comandos:
# uvicorn main:app --reload  (reemplaza "main" con el nombre de tu archivo si es diferente)