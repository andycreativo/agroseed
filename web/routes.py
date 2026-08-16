"""
Modulo web.routes
Define las rutas (endpoints) de Flask que exponen la funcionalidad
del sistema agroseed a traves del navegador.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from domain.lote_semillas import LoteSemillas, RegistroGerminacion
from domain.tipo_semilla import SemillaCertificada, SemillaCriolla
from infrastructure import lote_repository

bp = Blueprint("web", __name__, template_folder="templates")


@bp.route("/")
def index():
    """Muestra la lista de todos los lotes de semillas registrados."""
    lotes = lote_repository.listar_lotes()
    return render_template("index.html", lotes=lotes)


@bp.route("/lotes/nuevo", methods=["GET", "POST"])
def nuevo_lote():
    """Muestra el formulario de creacion y procesa el registro de un nuevo lote."""
    if request.method == "POST":
        id_lote = request.form["id_lote"]
        cultivo = request.form["cultivo"]
        total_semillas = int(request.form["total_semillas"])
        nombre_tipo = request.form["tipo_semilla"]

        tipo_semilla = SemillaCertificada() if nombre_tipo == "certificada" else SemillaCriolla()
        lote = LoteSemillas(id_lote, cultivo, total_semillas, tipo_semilla)

        lote_repository.crear_lote(lote)
        return redirect(url_for("web.index"))

    return render_template("nuevo_lote.html")


@bp.route("/lotes/<id_lote>/eliminar", methods=["POST"])
def eliminar_lote(id_lote):
    """Elimina un lote de semillas registrado."""
    lote_repository.eliminar_lote(id_lote)
    return redirect(url_for("web.index"))


@bp.route("/lotes/<id_lote>/registrar", methods=["POST"])
def registrar_germinacion(id_lote):
    """Registra la germinacion de la semana actual para un lote especifico."""
    lote = lote_repository.obtener_lote_por_id(id_lote)
    if lote is None:
        return redirect(url_for("web.index"))

    cantidad = int(request.form["cantidad"])
    lote.avanzar_semana()

    if lote.registrar_germinadas(cantidad):
        registro = RegistroGerminacion(lote.semana_actual, cantidad)
        lote_repository.agregar_registro_germinacion(id_lote, registro)

    lote_repository.actualizar_lote(lote)
    return redirect(url_for("web.index"))


@bp.route("/lotes/<id_lote>/vender", methods=["POST"])
def vender_lote(id_lote):
    """Registra una venta, descontando la cantidad vendida del lote."""
    lote = lote_repository.obtener_lote_por_id(id_lote)
    if lote is None:
        return redirect(url_for("web.index"))

    cantidad = int(request.form["cantidad"])
    try:
        lote.vender(cantidad)
        lote_repository.actualizar_cantidad_disponible(id_lote, lote.cantidad_disponible)
        if lote.esta_agotado():
            flash(f"El lote {id_lote} quedo agotado.", "warning")
        else:
            flash(f"Venta registrada. Quedan {lote.cantidad_disponible} unidades disponibles.", "success")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for("web.index"))


@bp.route("/tienda")
def tienda():
    """Vista simplificada para que un cliente vea los lotes disponibles y compre."""
    lotes = lote_repository.listar_lotes()
    return render_template("tienda.html", lotes=lotes)