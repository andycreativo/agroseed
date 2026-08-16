"""
Modulo infrastructure.lote_repository
Contiene las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para
persistir los lotes de semillas en la base de datos SQLite.
Esta capa traduce entre los objetos de domain y las filas de la base de datos.
"""
from domain.tipo_semilla import TipoSemilla, SemillaCertificada, SemillaCriolla
from domain.lote_semillas import LoteSemillas, RegistroGerminacion
from infrastructure.database import obtener_conexion


def _crear_tipo_semilla(nombre_tipo: str) -> TipoSemilla:
    """Convierte el nombre guardado en la base de datos en un objeto TipoSemilla."""
    tipos_disponibles = {
        "certificada": SemillaCertificada,
        "criolla": SemillaCriolla,
    }
    clase_tipo = tipos_disponibles.get(nombre_tipo)
    if clase_tipo is None:
        raise ValueError(f"Tipo de semilla no reconocido: {nombre_tipo}")
    return clase_tipo()


def _nombre_tipo_semilla(tipo_semilla: TipoSemilla) -> str:
    """Convierte un objeto TipoSemilla en el nombre que se guarda en la base de datos."""
    if isinstance(tipo_semilla, SemillaCertificada):
        return "certificada"
    if isinstance(tipo_semilla, SemillaCriolla):
        return "criolla"
    raise ValueError("Tipo de semilla no soportado")


def crear_lote(lote: LoteSemillas) -> None:
    """Inserta un nuevo lote de semillas en la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        INSERT INTO lotes_semillas (id_lote, cultivo, total_semillas, tipo_semilla, semana_actual, cantidad_disponible)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            lote.id_lote,
            lote.cultivo,
            lote.total_semillas,
            _nombre_tipo_semilla(lote.tipo_semilla),
            lote.semana_actual,
            lote.cantidad_disponible,
        ),
    )
    conexion.commit()
    conexion.close()


def listar_lotes() -> list[LoteSemillas]:
    """Devuelve todos los lotes de semillas registrados, con sus registros de germinacion."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    filas_lotes = cursor.execute("SELECT * FROM lotes_semillas").fetchall()

    lotes = []
    for fila in filas_lotes:
        lote = LoteSemillas(
            id_lote=fila["id_lote"],
            cultivo=fila["cultivo"],
            total_semillas=fila["total_semillas"],
            tipo_semilla=_crear_tipo_semilla(fila["tipo_semilla"]),
        )
        lote.semana_actual = fila["semana_actual"]
        lote.cantidad_disponible = fila["cantidad_disponible"]

        filas_registros = cursor.execute(
            "SELECT * FROM registros_germinacion WHERE id_lote = ?", (lote.id_lote,)
        ).fetchall()
        lote.registros_germinacion = [
            RegistroGerminacion(r["semana"], r["cantidad_germinadas"]) for r in filas_registros
        ]
        lotes.append(lote)

    conexion.close()
    return lotes


def obtener_lote_por_id(id_lote: str) -> LoteSemillas | None:
    """Busca y devuelve un lote especifico por su identificador, o None si no existe."""
    for lote in listar_lotes():
        if lote.id_lote == id_lote:
            return lote
    return None


def actualizar_lote(lote: LoteSemillas) -> None:
    """Actualiza los datos generales de un lote existente."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        UPDATE lotes_semillas
        SET cultivo = ?, total_semillas = ?, tipo_semilla = ?, semana_actual = ?
        WHERE id_lote = ?
        """,
        (
            lote.cultivo,
            lote.total_semillas,
            _nombre_tipo_semilla(lote.tipo_semilla),
            lote.semana_actual,
            lote.id_lote,
        ),
    )
    conexion.commit()
    conexion.close()


def eliminar_lote(id_lote: str) -> None:
    """Elimina un lote y todos sus registros de germinacion asociados."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM registros_germinacion WHERE id_lote = ?", (id_lote,))
    cursor.execute("DELETE FROM lotes_semillas WHERE id_lote = ?", (id_lote,))
    conexion.commit()
    conexion.close()


def agregar_registro_germinacion(id_lote: str, registro: RegistroGerminacion) -> None:
    """Guarda un nuevo registro semanal de germinacion para un lote."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO registros_germinacion (id_lote, semana, cantidad_germinadas) VALUES (?, ?, ?)",
        (id_lote, registro.semana, registro.cantidad_germinadas),
    )
    conexion.commit()
    conexion.close()


def actualizar_cantidad_disponible(id_lote: str, nueva_cantidad: int) -> None:
    """Actualiza unicamente la cantidad disponible de un lote (usado al vender)."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE lotes_semillas SET cantidad_disponible = ? WHERE id_lote = ?",
        (nueva_cantidad, id_lote),
    )
    conexion.commit()
    conexion.close()