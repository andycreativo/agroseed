"""
Modulo main
Punto de entrada de la aplicacion Agroseed.
Inicializa la base de datos y arranca el servidor Flask.
"""
from flask import Flask

from infrastructure.database import inicializar_base_datos
from web.routes import bp as web_bp
from web.auth_routes import auth_bp
from web.api_routes import api_bp          # <-- NUEVO


def crear_aplicacion() -> Flask:
    """Crea y configura la instancia de la aplicacion Flask."""
    app = Flask(__name__)
    app.register_blueprint(web_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)          # <-- NUEVO
    return app


if __name__ == "__main__":
    inicializar_base_datos()
    app = crear_aplicacion()
    app.run(debug=True)