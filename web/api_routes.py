"""
Modulo web.api_routes
Servicio web (API REST) para la gestion de lotes de semillas del proyecto Agroseed.
Expone los lotes en formato JSON, complementando la interfaz web (web/routes.py).
"""
from flask import Blueprint, request, jsonify

from domain.lote_semillas import LoteSemillas
from domain.tipo_semilla import SemillaCertificada, SemillaCriolla
from infrastructure import lote_repository

api_bp = Blueprint("api", __name__, url_prefix="/api")


def lote_a_diccionario(lote: LoteSemillas) -> dict:
    """Convierte un objeto LoteSemillas en un diccionario serializable a JSON."""
    return {
        "id_lote": lote.id_lote,
        "cultivo": lote.cultivo,
        "tipo_semilla": lote.tipo_semilla.describir(),
        "total_semillas": lote.total_semillas,
        "semana_actual": lote.semana_actual,
        "porcentaje_germinacion": lote.calcular_porcentaje_germinacion(),
        "listo_para_evaluacion": lote.esta_listo_para_evaluacion(),
        "apto": lote.es_apto() if lote.esta_listo_para_evaluacion() else None,
    }


@api_bp.route("/lotes", methods=["GET"])
def listar_lotes_api():
    """Devuelve todos los lotes registrados en formato JSON."""
    lotes = lote_repository.listar_lotes()
    return jsonify([lote_a_diccionario(l) for l in lotes]), 200


@api_bp.route("/lotes/<id_lote>", methods=["GET"])
def obtener_lote_api(id_lote):
    """Devuelve un lote especifico por su identificador."""
    lote = lote_repository.obtener_lote_por_id(id_lote)
    if lote is None:
        return jsonify({"mensaje": "Lote no encontrado"}), 404
    return jsonify(lote_a_diccionario(lote)), 200


@api_bp.route("/lotes", methods=["POST"])
def crear_lote_api():
    """Crea un nuevo lote a partir de un JSON con sus datos."""
    datos = request.get_json(silent=True) or {}
    id_lote = datos.get("id_lote")
    cultivo = datos.get("cultivo")
    total_semillas = datos.get("total_semillas")
    nombre_tipo = datos.get("tipo_semilla")

    if not all([id_lote, cultivo, total_semillas, nombre_tipo]):
        return jsonify({"mensaje": "Todos los campos son obligatorios"}), 400

    tipo_semilla = SemillaCertificada() if nombre_tipo == "certificada" else SemillaCriolla()
    lote = LoteSemillas(id_lote, cultivo, int(total_semillas), tipo_semilla)
    lote_repository.crear_lote(lote)

    return jsonify(lote_a_diccionario(lote)), 201


@api_bp.route("/lotes/<id_lote>/germinacion", methods=["POST"])
def registrar_germinacion_api(id_lote):
    """Registra la germinacion de la semana actual para un lote, via API."""
    lote = lote_repository.obtener_lote_por_id(id_lote)
    if lote is None:
        return jsonify({"mensaje": "Lote no encontrado"}), 404

    datos = request.get_json(silent=True) or {}
    cantidad = datos.get("cantidad")
    if cantidad is None:
        return jsonify({"mensaje": "El campo cantidad es obligatorio"}), 400

    lote.avanzar_semana()
    registrado = lote.registrar_germinadas(int(cantidad))
    if not registrado:
        return jsonify({"mensaje": "Cantidad invalida: supera el total sembrado o es negativa"}), 400

    lote_repository.actualizar_lote(lote)
    return jsonify(lote_a_diccionario(lote)), 200


@api_bp.route("/lotes/<id_lote>", methods=["DELETE"])
def eliminar_lote_api(id_lote):
    """Elimina un lote registrado, via API."""
    lote_repository.eliminar_lote(id_lote)
    return jsonify({"mensaje": "Lote eliminado correctamente"}), 200