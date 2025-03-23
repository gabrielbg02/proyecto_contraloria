#Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /proyecto_contraloria

# Copiar el archivo de dependencias
COPY requirements.txt ./

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . ./


# Comando para ejecutar la aplicación
CMD ["uvicorn", "app_fastapi:app", "--host", "0.0.0.0", "--port", "8002", "--workers", "4"]

# Exponer el puerto en el que se ejecutará FastAPI
EXPOSE 8002

#Usar una imagen base de Python
#FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
#WORKDIR /proyecto_cmch

# Copiar el archivo de dependencias
#COPY requirements.txt .

# Instalar las dependencias
#RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
#COPY . ./


# Comando para ejecutar la aplicación
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]

# Exponer el puerto en el que se ejecutará FastAPI
#EXPOSE 8001