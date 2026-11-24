
"""
@file app.py
@brief Aplicación web de ejemplo para el proyecto DevSecOps.

@details
Este módulo agrega una aplicación web utilizando Flask.
Proporciona una ruta principal y una ruta para generar
saludos personalizados mediante parámetros HTTP.

@author Equipo DevSecOps
@version 1.0
"""

from flask import Flask, request

# Inicialización de la aplicación Flask.
app = Flask(__name__)


@app.route("/")
def home():
    """
    @brief Muestra la página principal de la aplicación.

    @return Mensaje de confirmación del funcionamiento
            de la aplicación DevSecOps.
    """
    return "Aplicación DevSecOps funcionando súper"


@app.route("/hello")
def hello():
    """
    @brief Genera un saludo personalizado.

    @details
    Obtiene el nombre desde el parámetro HTTP 'name'.
    Si no se proporciona, utiliza 'Mundito Mundirijillo' como valor
    predeterminado.

    @return Mensaje de saludo personalizado.
    """
    name = request.args.get("name", "Mundito Mundirijillo")
    return f"Hola hola hola, {name}!"


if __name__ == "__main__":
    """
    @brief Punto de entrada de la aplicación.

    Inicia el servidor Flask escuchando en todas las
    interfaces de red, utilizando el puerto 5000.
    """
    app.run(host="0.0.0.0", port=5000, debug=False)
