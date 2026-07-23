"""
Modulo main
Punto de entrada de la aplicacion Agroseed.
Inicializa la base de datos y arranca el servidor Flask.
"""
from flask import Flask

from infrastructure.database import inicializar_base_datos
from web.routes import bp as web_bp


def crear_aplicacion() -> Flask:
    """Crea y configura la instancia de la aplicacion Flask."""
    app = Flask(__name__)
    app.register_blueprint(web_bp)
    return app


if __name__ == "__main__":
    inicializar_base_datos()
    app = crear_aplicacion()
    app.run(debug=True)
    