from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Ruta para mostrar el formulario
@app.route('/')
def mostrar_formulario():
    return render_template('formulario.html')

# Ruta para procesar el formulario
@app.route('/data-processing', methods=['POST'])
def procesar_formulario():
    # Obtener los datos del formulario
    datos = request.form

    # Convertir los datos a un formato legible
    datos_guardar = "\n".join([f"{key}: {value}" for key, value in datos.items()])

    # Guardar los datos en un archivo
    ruta_archivo = os.path.join(os.getcwd(), 'datos_formulario.txt')
    with open(ruta_archivo, 'a') as archivo:
        archivo.write(datos_guardar + "\n\n")

    return "Datos guardados correctamente"

# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)
