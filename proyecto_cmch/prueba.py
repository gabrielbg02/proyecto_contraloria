from fastapi import FastAPI, Request, Form, staticfiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mongoengine import *
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configuración de MongoDB (tu código actual)
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

# Configuración de correo (ajusta estos valores)
SMTP_SERVER = "smtp.gmail.com"  # Cambia según tu proveedor
SMTP_PORT = 587
EMAIL_ADDRESS = "gabrielusuario0208@gmail.com"  # Cambia por tu correo
EMAIL_PASSWORD = "Fbs983932"  # Cambia por tu contraseña o app password

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

def generar_pdf(datos: datos_formulario, filename: str):
    """Genera un PDF con los datos del formulario"""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title = Paragraph("Reporte de Formulario OAC", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Fecha de generación
    fecha = Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"])
    elements.append(fecha)
    elements.append(Spacer(1, 24))
    
    # Información básica
    info_basica = [
        ["Nombre:", datos.nombre],
        ["Correo:", datos.correo],
        ["Cargo:", datos.cargo],
        ["Estado:", datos.estado],
        ["Municipio:", datos.municipio],
        ["Organismo:", datos.nombre_organismo],
        ["Instancia:", datos.instancia]
    ]
    
    # Tabla de datos generales
    tabla_info = Table(info_basica, colWidths=[150, 300])
    tabla_info.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#333333')),
        ('TEXTCOLOR', (1,0), (1,-1), colors.HexColor('#000066')),
    ]))
    
    elements.append(tabla_info)
    elements.append(Spacer(1, 24))
    
    # Sección de estadísticas
    secciones = [
        ("Denuncias y Solicitudes", [
            ("Denuncias", datos.cantidad_denuncias),
            ("Reclamos", datos.cantidad_reclamos),
            ("Quejas", datos.cantidad_quejas),
            ("Peticiones", datos.cantidad_peticiones),
            ("Sugerencias", datos.cantidad_sugerencias),
            ("Asesorías", datos.cantidad_asesorias)
        ]),
        ("Población Atendida", [
            ("Población Masculina", datos.cantidad_poblacion_masc),
            ("Población Femenina", datos.cantidad_poblacion_fem)
        ])
        # Agrega más secciones según necesites
    ]
    
    for titulo, items in secciones:
        elements.append(Paragraph(titulo, styles["Heading2"]))
        elements.append(Spacer(1, 8))
        
        tabla = Table([[k, str(v)] for k, v in items], colWidths=[200, 100])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0f0f0')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        
        elements.append(tabla)
        elements.append(Spacer(1, 16))
    
    # Observaciones
    if datos.observaciones:
        elements.append(Paragraph("Observaciones", styles["Heading3"]))
        elements.append(Spacer(1, 8))
        elements.append(Paragraph(datos.observaciones, styles["Normal"]))
    
    doc.build(elements)

def enviar_correo(destinatario: str, asunto: str, cuerpo: str, archivo_adjunto: str):
    """Envía un correo electrónico con el PDF adjunto"""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = destinatario
    msg['Subject'] = asunto
    
    # Cuerpo del mensaje
    msg.attach(MIMEText(cuerpo, 'plain'))
    
    # Adjuntar el PDF
    with open(archivo_adjunto, "rb") as f:
        adjunto = MIMEApplication(f.read(), _subtype="pdf")
        adjunto.add_header('Content-Disposition', 'attachment', filename=os.path.basename(archivo_adjunto))
        msg.attach(adjunto)
    
    # Enviar el correo
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

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
    
    # Generar PDF
    pdf_filename = f"reporte_{datos_guardar.nombre_llenado.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
    generar_pdf(datos_guardar, pdf_filename)
    
    # Enviar por correo
    asunto = f"Reporte OAC - {datos_guardar.nombre_organismo}"
    cuerpo = f"""Estimado/a {datos_guardar.nombre_llenado},

Adjunto encontrará el reporte generado a partir de los datos ingresados en el formulario OAC.

Datos principales:
- Organismo: {datos_guardar.nombre_organismo}
- Estado: {datos_guardar.estado}
- Municipio: {datos_guardar.municipio}

Este es un mensaje automático, por favor no responda directamente a este correo.

Atentamente,
Sistema de Reportes OAC
"""
    
    try:
        enviar_correo(
            destinatario=datos_guardar.correo_llenado,
            asunto=asunto,
            cuerpo=cuerpo,
            archivo_adjunto=pdf_filename
        )
        print(f"Correo enviado exitosamente a {datos_guardar.correo_llenado}")
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")
    
    return templates.TemplateResponse("exito.html", {"request": request})