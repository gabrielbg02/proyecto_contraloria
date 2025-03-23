from fastapi import FastAPI, Request, Form, staticfiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mongoengine import *
import os

app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

try:
    connect(
        db = "registro_oac",
        username = "heimdall",
        password = "Nn77Tw0WPM8Az1W1",
        host = "mongodb+srv://cluster0.3vudx.mongodb.net",
        authentication_source = 'admin',
        ssl = True,
    )
    print("Conexión a MongoDB exitosa")
except ConnectionFailure as e:
    print(f"No se pudo conectar a MongoDB: {e}")

class datos_formulario(Document):
    nombre = StringField()
    correo = EmailField()
    cargo = StringField()
    numero_cedula = StringField()
    numero_telefono_jefe = StringField()
    estado = StringField()
    municipio = StringField()
    nombre_organismo = StringField()
    instancia = StringField()
    nombre_llenado = StringField()
    correo_llenado = EmailField()
    cargo_llenado = StringField()
    numero_cedula_llenado = StringField()
    numero_telefono_llenado = StringField()
    cantidad_denuncias = IntField()
    cantidad_reclamos = IntField()
    cantidad_quejas = IntField()
    cantidad_peticiones = IntField()
    cantidad_sugerencias = IntField()
    cantidad_asesorias = IntField()
    cantidad_poblacion_masc = IntField()
    cantidad_poblacion_fem = IntField()
    cantidad_talleres_oipp = IntField()
    cantidad_charlas_oipp = IntField ()
    cantidad_conversatorios_oipp = IntField()
    cantidad_jornadas_oipp = IntField()
    cantidad_forochats_oipp = IntField()
    cantidad_adulto_masculino_atentido_oipp = IntField() 
    cantidad_adulto_femenino_atentida_oipp = IntField()
    nombre_escuela_se = StringField()
    cantidad_actividades_se = StringField()
    cantidad_talleres_se = IntField()
    cantidad_charlas_se = IntField()
    cantidad_conversatorios_se = IntField()
    cantidad_jornadas_se = IntField()
    cantidad_forochats_se = IntField()
    cantidad_ninosyadol_masculino_se = IntField()
    cantidad_ninasyadol_femenino_se = IntField()
    cantidad_adultos_masculino_atendidos_se = IntField()
    cantidad_adultos_femenino_atendidos_se = IntField()
    nombre_ministerio_ap = StringField()
    cantidad_actividades_ap = StringField()
    cantidad_talleres_ap = IntField()
    cantidad_charlas_ap = IntField()
    cantidad_jornadas_ap = IntField()
    cantidad_forochats_ap = IntField()
    cantidad_funcionarios_masculino_ap = IntField()
    cantidad_funcionarios_femenino_ap = IntField()
    observaciones = StringField()

    meta = {'collection': 'formulario'}

@app.get("/", response_class=HTMLResponse)
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

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
    nombre_llenado: str = Form(...),
    correo_llenado: str = Form(...),
    cargo_llenado: str = Form(...),
    numero_cedula_llenado: str = Form(...),
    numero_telefono_llenado: str = Form(...), 
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
    observaciones: str = Form(...),
):
    datos_guardar = datos_formulario(
        nombre = nombre,
        correo = correo,
        cargo = cargo,
        numero_cedula = numero_cedula,
        numero_telefono_jefe = numero_telefono_jefe,
        estado = estado,
        municipio = municipio,
        nombre_organismo = nombre_organismo,
        instancia = instancia,
        nombre_llenado = nombre_llenado,
        correo_llenado = correo_llenado,
        cargo_llenado = cargo_llenado,
        numero_cedula_llenado = numero_cedula_llenado,
        numero_telefono_llenado = numero_telefono_llenado, 
        cantidad_denuncias = int (cantidad_denuncias),
        cantidad_reclamos = int (cantidad_reclamos),
        cantidad_quejas = int (cantidad_quejas),
        cantidad_peticiones = int (cantidad_peticiones),
        cantidad_sugerencias = int (cantidad_sugerencias),
        cantidad_asesorias = int (cantidad_asesorias),
        cantidad_poblacion_masc = int (cantidad_poblacion_masc),
        cantidad_poblacion_fem = int (cantidad_poblacion_fem),
        cantidad_talleres_oipp = int (cantidad_talleres_oipp),
        cantidad_charlas_oipp=int (cantidad_charlas_oipp),
        cantidad_conversatorios_oipp = int (cantidad_conversatorios_oipp),
        cantidad_jornadas_oipp = int (cantidad_jornadas_oipp),
        cantidad_forochats_oipp = int (cantidad_forochats_oipp),
        cantidad_adulto_masculino_atentido_oipp = int ( cantidad_adulto_masculino_atentido_oipp),
        cantidad_adulto_femenino_atentida_oipp = int (cantidad_adulto_femenino_atentida_oipp),
        nombre_escuela_se = nombre_escuela_se,
        cantidad_actividades_se = cantidad_actividades_se,
        cantidad_talleres_se = int (cantidad_talleres_se),
        cantidad_charlas_se = int (cantidad_charlas_se),
        cantidad_conversatorios_se = int (cantidad_conversatorios_se ),
        cantidad_jornadas_se = int (cantidad_jornadas_se),
        cantidad_forochats_se = int (cantidad_forochats_se),
        cantidad_ninosyadol_masculino_se = int (cantidad_ninosyadol_masculino_se),
        cantidad_ninasyadol_femenino_se = int (cantidad_ninasyadol_femenino_se),
        cantidad_adultos_masculino_atendidos_se = int (cantidad_adultos_masculino_atendidos_se),
        cantidad_adultos_femenino_atendidos_se = int (cantidad_adultos_femenino_atendidos_se),
        nombre_ministerio_ap = nombre_ministerio_ap,
        cantidad_actividades_ap=cantidad_actividades_ap,
        cantidad_talleres_ap = int (cantidad_talleres_ap),
        cantidad_charlas_ap = int (cantidad_charlas_ap ),
        cantidad_jornadas_ap = int (cantidad_jornadas_ap),
        cantidad_forochats_ap = int (cantidad_forochats_ap),
        cantidad_funcionarios_masculino_ap = int (cantidad_funcionarios_masculino_ap),
        cantidad_funcionarios_femenino_ap = int (cantidad_funcionarios_femenino_ap),
        observaciones = observaciones
    )
    
    datos_guardar.save()
    return templates.TemplateResponse("exito.html", {"request": request})