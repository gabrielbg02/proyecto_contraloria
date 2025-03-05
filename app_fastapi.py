from fastapi import FastAPI, Request, Form, staticfiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static") # para mostrar la imagen
templates = Jinja2Templates(directory="templates") 

# Ruta para mostrar el formulario
@app.get("/", response_class=HTMLResponse)
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

# Ruta para procesar el formulario
@app.post("/data-processing")
async def procesar_formulario(
    request: Request,
    nombre: str = Form(...),
    correo: str = Form(...),
    cargo: str = Form(...),
    numero_cedula: str = Form(...),
    numero_telefono_jefe: str = Form(...),
    estado: str = Form(...),
    municipio: str = Form(...),
    nombre_organismo: str = Form(...),
    instancia: str = Form(...),
    cantidad_denuncias: str = Form(...),
    cantidad_reclamos: str = Form(...),
    cantidad_quejas: str = Form(...),
    cantidad_peticiones: str = Form(...),
    cantidad_sugerencias: str = Form(...),
    cantidad_asesorias: str = Form(...),
    cantidad_poblacion_masc: str = Form(...),
    cantidad_poblacion_fem: str = Form(...),
    cantidad_talleres_oipp: str = Form(...),
    cantidad_charlas_oipp: str = Form (...),
    cantidad_conversatorios_oipp: str = Form(...),
    cantidad_jornadas_oipp: str = Form(...),
    cantidad_forochats_oipp: str = Form(...),
    cantidad_adulto_masculino_atentido_oipp: str = Form(...),
    cantidad_adulto_femenino_atentida_oipp: str = Form(...),
    nombre_escuela_se: str = Form(...),
    cantidad_actividades_se: str = Form(...),
    cantidad_talleres_se: str = Form(...),
    cantidad_charlas_se: str = Form(...),
    cantidad_conversatorios_se: str = Form(...),
    cantidad_jornadas_se: str = Form(...),
    cantidad_forochats_se: str = Form(...),
    cantidad_ninosyadol_masculino_se: str = Form(...),
    cantidad_ninasyadol_femenino_se: str = Form(...),
    cantidad_adultos_masculino_atendidos_se: str = Form(...),
    cantidad_adultos_femenino_atendidos_se: str = Form(...),
    nombre_ministerio_ap: str = Form(...),
    cantidad_actividades_ap: str = Form(...),
    cantidad_talleres_ap: str = Form(...),
    cantidad_charlas_ap: str = Form(...),
    cantidad_jornadas_ap: str = Form(...),
    cantidad_forochats_ap: str = Form(...),
    cantidad_funcionarios_masculino_ap: str = Form(...),
    cantidad_funcionarios_femenino_ap: str = Form(...)):
    datos_guardar = "\n".join([
        f"nombre: {nombre}",
        f"correo: {correo}",
        f"cargo: {cargo}",
        f"numero_cedula: {numero_cedula}",
        f"numero_telefono_jefe: {numero_telefono_jefe}",
        f"estado: {estado}",
        f"municipio: {municipio}",
        f"nombre_organismo: {nombre_organismo}",
        f"instancia: {instancia}",
        f"cantidad_denuncias: {cantidad_denuncias}",
        f"cantidad_reclamos: {cantidad_reclamos}",
        f"cantidad_quejas: {cantidad_quejas}",
        f"cantidad_peticiones: {cantidad_peticiones}",
        f"cantidad_sugerencias: {cantidad_sugerencias}",
        f"cantidad_asesorias: {cantidad_asesorias}",
        f"cantidad_poblacion_masc: {cantidad_poblacion_masc}",
        f"cantidad_poblacion_fem: {cantidad_poblacion_fem}",
        f"cantidad_talleres_oipp: {cantidad_talleres_oipp}",
        f"cantidad_charlas_oipp: {cantidad_charlas_oipp}",
        f"cantidad_conversatorios_oipp: {cantidad_conversatorios_oipp}",
        f"cantidad_jornadas_oipp: {cantidad_jornadas_oipp}",
        f"cantidad_forochats_oipp: {cantidad_forochats_oipp}",
        f"cantidad_adulto_masculino_atentido_oipp: {cantidad_adulto_masculino_atentido_oipp}",
        f"cantidad_adulto_femenino_atentida_oipp: {cantidad_adulto_femenino_atentida_oipp}",
        f"nombre_escuela_se: {nombre_escuela_se}",
        f"cantidad_actividades_se: {cantidad_actividades_se}",
        f"cantidad_talleres_se: {cantidad_talleres_se}",
        f"cantidad_charlas_se: {cantidad_charlas_se}",
        f"cantidad_conversatorios_se: {cantidad_conversatorios_se}",
        f"cantidad_jornadas_se: {cantidad_jornadas_se}",
        f"cantidad_forochats_se: {cantidad_forochats_se}",
        f"cantidad_ninosyadol_masculino_se: {cantidad_ninosyadol_masculino_se}",
        f"cantidad_ninasyadol_femenino_se: {cantidad_ninasyadol_femenino_se}",
        f"cantidad_adultos_masculino_atendidos_se: {cantidad_adultos_masculino_atendidos_se}",
        f"cantidad_adultos_femenino_atendidos_se: {cantidad_adultos_femenino_atendidos_se}",
        f"nombre_ministerio_ap: {nombre_ministerio_ap}",
        f"cantidad_actividades_ap: {cantidad_actividades_ap}",
        f"cantidad_talleres_ap: {cantidad_talleres_ap}",
        f"cantidad_charlas_ap: {cantidad_charlas_ap}",
        f"cantidad_jornadas_ap: {cantidad_jornadas_ap}",
        f"cantidad_forochats_ap: {cantidad_forochats_ap}",
        f"cantidad_funcionarios_masculino_ap: {cantidad_funcionarios_masculino_ap}",
        f"cantidad_funcionarios_femenino_ap: {cantidad_funcionarios_femenino_ap}"
    ])

    # Guardar los datos en un archivo
    ruta_archivo = os.path.join(os.getcwd(), 'datos_formulario.txt')
    with open(ruta_archivo, 'a') as archivo:
        archivo.write(datos_guardar + "\n\n")

    return templates.TemplateResponse('exito.html' , {"request": request})


