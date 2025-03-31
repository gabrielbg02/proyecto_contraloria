from fastapi import FastAPI, Request, Form, staticfiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mongoengine import *
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from reportlab.lib.utils import ImageReader

app = FastAPI()
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configuración de MongoDB (tu código actual)
try:
    connect(
         host="mongodb://localhost:27017",  # Conexión local básica,
    )
    print("Conexión a MongoDB exitosa")
except ConnectionFailure as e:
    print(f"No se pudo conectar a MongoDB: {e}")

# Configuración de correo (ajusta estos valores)
SMTP_SERVER = "smtp.gmail.com"  # Cambia según tu proveedor
SMTP_PORT = 587
EMAIL_ADDRESS = "gabrielitoborges32@gmail.com"  # Cambia por tu correo
EMAIL_PASSWORD = "xbbnpneushvueqto"  # Cambia por tu contraseña o app password

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
    
    # Obtener la ruta base del proyecto
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    def on_first_page(canvas, doc):
        # Ruta absoluta a la imagen
        img_path = os.path.join(base_dir, "static", "images", "logo_contraloria.png")
        
        # Agregar imagen en esquina superior izquierda
        if os.path.exists(img_path):
            img = ImageReader(img_path)
            canvas.drawImage(img, 40, doc.pagesize[1] - 100, width=100, height=80, preserveAspectRatio=True)
        
        # Agregar misma imagen en esquina superior derecha (o usa otra imagen si lo prefieres)
        if os.path.exists(img_path):
            canvas.drawImage(img, doc.pagesize[0] - 140, doc.pagesize[1] - 100, width=100, height=80, preserveAspectRatio=True)
        
        # Texto del encabezado
        canvas.setFont("Helvetica-Bold", 18)
        canvas.drawString(200, doc.pagesize[1] - 50, "Contraloría Municipal de Chacao")
        canvas.setFont("Helvetica", 14)
        canvas.drawString(200, doc.pagesize[1] - 70, "Reporte de Formulario OAC")
    
    def on_later_pages(canvas, doc):
        # Ruta absoluta a la imagen para páginas siguientes
        img_path = os.path.join(base_dir, "static", "images", "logo_contraloria.png")
        
        # Repetir imágenes en páginas siguientes
        if os.path.exists(img_path):
            img = ImageReader(img_path)
            # Esquina izquierda
            canvas.drawImage(img, 40, doc.pagesize[1] - 100, width=100, height=80, preserveAspectRatio=True)
            # Esquina derecha
            canvas.drawImage(img, doc.pagesize[0] - 140, doc.pagesize[1] - 100, width=100, height=80, preserveAspectRatio=True)
        
        # Número de página
        canvas.setFont("Helvetica", 9)
        canvas.drawRightString(doc.pagesize[0] - 50, 30, f"Página {doc.page}")



    # Título
    #title = Paragraph("Contraloria Municipal de Chacao", styles["Title"])
    #elements.append(Paragraph("Reporte de Formulario OAC", styles["Heading2"]))
    #elements.append(title)
    #elements.append(Spacer(1, 12))
    
    # Fecha de generación
    fecha = Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"])
    elements.append(fecha)
    elements.append(Spacer(1, 24))
    
    # ========= SECCIÓN 1: DATOS PERSONALES =========
    elements.append(Paragraph("1. Datos Personales del Jefe/Jefa de la Oficina de Atencion al Ciudadano", styles["Heading2"]))
    elements.append(Spacer(1, 12))
    
    info_personales = [
        ["Nombre y Apellido:", datos.nombre],
        ["Número de Cédula:", datos.numero_cedula],
        ["Cargo:", datos.cargo],
        ["Correo:", datos.correo],
        ["Número de Teléfono:", datos.numero_telefono_jefe]
    ]
    
    tabla_personales = Table(info_personales, colWidths=[200, 300])
    tabla_personales.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#333333')),
        ('TEXTCOLOR', (1,0), (1,-1), colors.HexColor('#000066')),
    ]))
    elements.append(tabla_personales)
    elements.append(Spacer(1, 24))
    
    # ========= SECCIÓN 2: INFORMACIÓN DEL ORGANISMO =========
    elements.append(Paragraph("2. Información del Organismo/Ente", styles["Heading2"]))
    elements.append(Spacer(1, 12))
    
    info_organismo = [
        ["Estado:", datos.estado],
        ["Municipio:", datos.municipio],
        ["Nombre del Organismo:", datos.nombre_organismo],
        ["Instancia:", datos.instancia]
    ]
    
    tabla_organismo = Table(info_organismo, colWidths=[200, 300])
    tabla_organismo.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#333333')),
        ('TEXTCOLOR', (1,0), (1,-1), colors.HexColor('#000066')),
    ]))
    elements.append(tabla_organismo)
    elements.append(Spacer(1, 24))
    
    # ========= SECCIÓN 3: PERSONA QUE LLENÓ EL FORMULARIO =========
    elements.append(Paragraph("3. Informacion Personal de Quien Llenó el Formulario", styles["Heading2"]))
    elements.append(Spacer(1, 12))
    
    info_personal_llenado = [
        ["Nombre y Apellido:", datos.nombre_llenado],
        ["Número de Cédula:", datos.numero_cedula_llenado],
        ["Cargo:", datos.cargo_llenado],
        ["Correo:", datos.correo_llenado],
        ["Número de Teléfono:", datos.numero_telefono_llenado]
    ]
    
    tabla_personal_llenado = Table(info_personal_llenado, colWidths=[200, 300])
    tabla_personal_llenado.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#333333')),
        ('TEXTCOLOR', (1,0), (1,-1), colors.HexColor('#000066')),
    ]))
    elements.append(tabla_personal_llenado)
    elements.append(Spacer(1, 24))
    
    # ========= SECCIÓN 4: ATENCIÓN AL CIUDADANO =========
    elements.append(Paragraph("4. Actividades de la Oficina", styles["Heading2"]))
    elements.append(Paragraph("   Mecanismos de Participacion Ciudadana", styles["Heading3"]))
    elements.append(Spacer(1, 12))
    
    atencion_ciudadano = [
        ["Denuncias recibidas:", datos.cantidad_denuncias],
        ["Reclamos recibidos:", datos.cantidad_reclamos],
        ["Quejas recibidas:", datos.cantidad_quejas],
        ["Peticiones recibidas:", datos.cantidad_peticiones],
        ["Sugerencias recibidas:", datos.cantidad_sugerencias],
        ["Asesorías realizadas:", datos.cantidad_asesorias],
        ["Población masculina atendida:", datos.cantidad_poblacion_masc],
        ["Población femenina atendida:", datos.cantidad_poblacion_fem]
    ]
    
    tabla_atencion = Table(atencion_ciudadano, colWidths=[200, 100])
    tabla_atencion.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0f0f0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(tabla_atencion)
    elements.append(Spacer(1, 24))
    
    # ========= SECCIÓN 5: ORIENTACIÓN E INFORMACIÓN (OIPP) =========
    elements.append(Paragraph("5. Actividades para la OIPP", styles["Heading2"]))
    elements.append(Spacer(1, 12))
    
    actividades_oipp = [
        ["Talleres realizados:", datos.cantidad_talleres_oipp],
        ["Charlas realizadas:", datos.cantidad_charlas_oipp],
        ["Conversatorios realizados:", datos.cantidad_conversatorios_oipp],
        ["Jornadas realizadas:", datos.cantidad_jornadas_oipp],
        ["Forochats realizados:", datos.cantidad_forochats_oipp],
        ["Adultos masculinos atendidos:", datos.cantidad_adulto_masculino_atentido_oipp],
        ["Adultos femeninos atendidos:", datos.cantidad_adulto_femenino_atentida_oipp]
    ]
    
    tabla_oipp = Table(actividades_oipp, colWidths=[200, 100])
    tabla_oipp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0f0f0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(tabla_oipp)
    elements.append(Spacer(1, 24))
    
    if datos.nombre_escuela_se:  # Solo mostrar si hay datos
        elements.append(Paragraph("6. Actividades Sistema Educativo", styles["Heading2"]))
        elements.append(Spacer(1, 12))
        
        # Creamos un estilo especial para celdas con texto largo
        estilo_texto_largo = ParagraphStyle(
            'texto_largo',
            parent=styles['Normal'],
            wordWrap='CJK'  # Permite el ajuste de texto
        )
        
        # Preparamos los datos con Paragraph para texto largo
        descripcion_actividades = Paragraph(datos.cantidad_actividades_se, estilo_texto_largo) if datos.cantidad_actividades_se else ""
        
        servicio_educativo = [
            ["Nombre de la escuela:", datos.nombre_escuela_se],
            ["Cantidad y descripción de actividades:", descripcion_actividades],
            ["Talleres realizados:", str(datos.cantidad_talleres_se)],
            ["Charlas realizadas:", str(datos.cantidad_charlas_se)],
            ["Conversatorios realizados:", str(datos.cantidad_conversatorios_se)],
            ["Jornadas realizadas:", str(datos.cantidad_jornadas_se)],
            ["Forochats realizados:", str(datos.cantidad_forochats_se)],
            ["Niños/adolescentes masculinos atendidos:", str(datos.cantidad_ninosyadol_masculino_se)],
            ["Niñas/adolescentes femeninas atendidas:", str(datos.cantidad_ninasyadol_femenino_se)],
            ["Adultos masculinos atendidos:", str(datos.cantidad_adultos_masculino_atendidos_se)],
            ["Adultos femeninos atendidos:", str(datos.cantidad_adultos_femenino_atendidos_se)]
        ]
        
        # Creamos la tabla con ajuste automático de altura
        tabla_educativo = Table(servicio_educativo, colWidths=[200, 300])
        tabla_educativo.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0f0f0')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('PADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (0,-1), 'RIGHT'),
            ('ALIGN', (1,0), (1,-1), 'LEFT'),
            ('RIGHTPADDING', (1,1), (1,1), 10),  # Celda de descripción
            ('LEFTPADDING', (1,1), (1,1), 10),
        ]))
        elements.append(tabla_educativo)
        elements.append(Spacer(1, 24))
    
    # ========= SECCIÓN 7: ATENCIÓN A FUNCIONARIOS =========
    if datos.nombre_ministerio_ap:  # Solo mostrar si hay datos
        elements.append(Paragraph("7. Actividades para la Administración Pública", styles["Heading2"]))
        elements.append(Spacer(1, 12))
        
        # Preparamos los datos con Paragraph para texto largo
        descripcion_actividades_ap = Paragraph(datos.cantidad_actividades_ap, estilo_texto_largo) if datos.cantidad_actividades_ap else ""
        
        atencion_funcionarios = [
            ["Ministerio/Institución:", datos.nombre_ministerio_ap],
            ["Cantidad y descripción de actividades:", descripcion_actividades_ap],
            ["Talleres realizados:", str(datos.cantidad_talleres_ap)],
            ["Charlas realizadas:", str(datos.cantidad_charlas_ap)],
            ["Jornadas realizadas:", str(datos.cantidad_jornadas_ap)],
            ["Forochats realizados:", str(datos.cantidad_forochats_ap)],
            ["Funcionarios masculinos atendidos:", str(datos.cantidad_funcionarios_masculino_ap)],
            ["Funcionarios femeninos atendidos:", str(datos.cantidad_funcionarios_femenino_ap)]
        ]
        
        tabla_funcionarios = Table(atencion_funcionarios, colWidths=[200, 300])
        tabla_funcionarios.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f0f0f0')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('PADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (0,-1), 'RIGHT'),
            ('ALIGN', (1,0), (1,-1), 'LEFT'),
            ('RIGHTPADDING', (1,1), (1,1), 10),  # Celda de descripción
            ('LEFTPADDING', (1,1), (1,1), 10),
        ]))
        elements.append(tabla_funcionarios)
        elements.append(Spacer(1, 24))
    
    # ========= SECCIÓN 8: OBSERVACIONES =========
    if datos.observaciones:
        elements.append(Paragraph("8. Observaciones", styles["Heading2"]))
        elements.append(Spacer(1, 8))
        elements.append(Paragraph(datos.observaciones, styles["Normal"]))
        elements.append(Spacer(1, 24))
    
    doc.build(
        elements,
        onFirstPage=on_first_page,
        onLaterPages=on_later_pages
    )

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