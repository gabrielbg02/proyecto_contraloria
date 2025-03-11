from fastapi import FastAPI, Request, Form, staticfiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pydantic import BaseModel
import os

app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

MONGODB_URI = "mongodb+srv://heimdall:Nn77Tw0WPM8Az1W1@cluster0.3vudx.mongodb.net/registro_oac?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)

try:
    client.admin.command('ping')
    print("Conexión a MongoDB exitosa")
except ConnectionFailure:
    print("No se pudo conectar a MongoDB")

db = client.registro_oac


class datos_formulario(BaseModel):
    nombre: str
    correo: str
    cargo: str
    numero_cedula: str
    numero_telefono_jefe: str
    estado: str
    municipio: str
    nombre_organismo: str
    instancia: str
    cantidad_denuncias: str
    cantidad_reclamos: str
    cantidad_quejas: str
    cantidad_peticiones: str
    cantidad_sugerencias: str
    cantidad_asesorias: str
    cantidad_poblacion_masc: str
    cantidad_poblacion_fem: str
    cantidad_talleres_oipp: str
    cantidad_charlas_oipp: str
    cantidad_conversatorios_oipp: str
    cantidad_jornadas_oipp: str
    cantidad_forochats_oipp: str
    cantidad_adulto_masculino_atentido_oipp: str
    cantidad_adulto_femenino_atentida_oipp: str
    nombre_escuela_se: str
    cantidad_actividades_se: str
    cantidad_talleres_se: str
    cantidad_charlas_se: str
    cantidad_conversatorios_se: str
    cantidad_jornadas_se: str
    cantidad_forochats_se: str
    cantidad_ninosyadol_masculino_se: str
    cantidad_ninasyadol_femenino_se: str
    cantidad_adultos_masculino_atendidos_se: str
    cantidad_adultos_femenino_atendidos_se: str
    nombre_ministerio_ap: str
    cantidad_actividades_ap: str
    cantidad_talleres_ap: str
    cantidad_charlas_ap: str
    cantidad_jornadas_ap: str
    cantidad_forochats_ap: str
    cantidad_funcionarios_masculino_ap: str
    cantidad_funcionarios_femenino_ap: str

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
    cantidad_charlas_oipp: str = Form(...),
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
    cantidad_funcionarios_femenino_ap: str = Form(...),
):
    datos_guardar = {
        "nombre": nombre,
        "correo": correo,
        "cargo": cargo,
        "numero_cedula": numero_cedula,
        "numero_telefono_jefe": numero_telefono_jefe,
        "estado": estado,
        "municipio": municipio,
        "nombre_organismo": nombre_organismo,
        "instancia": instancia,
        "cantidad_denuncias": cantidad_denuncias,
        "cantidad_reclamos": cantidad_reclamos,
        "cantidad_quejas": cantidad_quejas,
        "cantidad_peticiones": cantidad_peticiones,
        "cantidad_sugerencias": cantidad_sugerencias,
        "cantidad_asesorias": cantidad_asesorias,
        "cantidad_poblacion_masc": cantidad_poblacion_masc,
        "cantidad_poblacion_fem": cantidad_poblacion_fem,
        "cantidad_talleres_oipp": cantidad_talleres_oipp,
        "cantidad_charlas_oipp": cantidad_charlas_oipp,
        "cantidad_conversatorios_oipp": cantidad_conversatorios_oipp,
        "cantidad_jornadas_oipp": cantidad_jornadas_oipp,
        "cantidad_forochats_oipp": cantidad_forochats_oipp,
        "cantidad_adulto_masculino_atentido_oipp": cantidad_adulto_masculino_atentido_oipp,
        "cantidad_adulto_femenino_atentida_oipp": cantidad_adulto_femenino_atentida_oipp,
        "nombre_escuela_se": nombre_escuela_se,
        "cantidad_actividades_se": cantidad_actividades_se,
        "cantidad_talleres_se": cantidad_talleres_se,
        "cantidad_charlas_se": cantidad_charlas_se,
        "cantidad_conversatorios_se": cantidad_conversatorios_se,
        "cantidad_jornadas_se": cantidad_jornadas_se,
        "cantidad_forochats_se": cantidad_forochats_se,
        "cantidad_ninosyadol_masculino_se": cantidad_ninosyadol_masculino_se,
        "cantidad_ninasyadol_femenino_se": cantidad_ninasyadol_femenino_se,
        "cantidad_adultos_masculino_atendidos_se": cantidad_adultos_masculino_atendidos_se,
        "cantidad_adultos_femenino_atendidos_se": cantidad_adultos_femenino_atendidos_se,
        "nombre_ministerio_ap": nombre_ministerio_ap,
        "cantidad_actividades_ap": cantidad_actividades_ap,
        "cantidad_talleres_ap": cantidad_talleres_ap,
        "cantidad_charlas_ap": cantidad_charlas_ap,
        "cantidad_jornadas_ap": cantidad_jornadas_ap,
        "cantidad_forochats_ap": cantidad_forochats_ap,
        "cantidad_funcionarios_masculino_ap": cantidad_funcionarios_masculino_ap,
        "cantidad_funcionarios_femenino_ap": cantidad_funcionarios_femenino_ap,
    }
    # Guardar los datos en MongoDB
    db.formulario.insert_one(datos_guardar)
    return templates.TemplateResponse("exito.html", {"request": request})