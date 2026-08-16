"""
Modulo web.auth_routes
Define los endpoints de autenticacion (registro e inicio de sesion)
del sistema Agroseed. Expone una API JSON, tal como se prueba
en la coleccion de Bruno "Agroseed - Auth".
"""
from flask import Blueprint, request, jsonify, session

from werkzeug.security import generate_password_hash, check_password_hash

from infrastructure import usuario_repository

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["POST"])
def registro():
    """Registra un nuevo usuario con su contrasena cifrada (hash)."""
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario", "").strip()
    contrasena = datos.get("contrasena", "")

    if not usuario or not contrasena:
        return jsonify({"error": "Debes enviar 'usuario' y 'contrasena'."}), 400

    if usuario_repository.obtener_usuario_por_nombre(usuario) is not None:
        return jsonify({"error": f"El usuario '{usuario}' ya existe."}), 409

    contrasena_hash = generate_password_hash(contrasena)
    usuario_repository.crear_usuario(usuario, contrasena_hash)

    return jsonify({"mensaje": f"Usuario '{usuario}' registrado correctamente."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Valida las credenciales de un usuario e inicia su sesion."""
    datos = request.get_json(silent=True) or {}
    usuario = datos.get("usuario", "").strip()
    contrasena = datos.get("contrasena", "")

    usuario_encontrado = usuario_repository.obtener_usuario_por_nombre(usuario)

    if usuario_encontrado is None or not check_password_hash(
        usuario_encontrado.contrasena_hash, contrasena
    ):
        return jsonify({"error": "Usuario o contrasena incorrectos."}), 401

    session["usuario"] = usuario_encontrado.usuario
    return jsonify({"mensaje": f"Bienvenido, {usuario_encontrado.usuario}."}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Cierra la sesion del usuario actual."""
    session.pop("usuario", None)
    return jsonify({"mensaje": "Sesion cerrada."}), 200
