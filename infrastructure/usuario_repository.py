"""
Modulo infrastructure.usuario_repository
Encapsula el acceso a datos de la tabla 'usuarios' en SQLite.
"""
from infrastructure.database import obtener_conexion
from domain.usuario import Usuario


def crear_usuario(usuario: str, contrasena_hash: str) -> None:
    """Inserta un nuevo usuario en la base de datos."""
    conexion = obtener_conexion()
    conexion.execute(
        "INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)",
        (usuario, contrasena_hash),
    )
    conexion.commit()
    conexion.close()


def obtener_usuario_por_nombre(usuario: str) -> Usuario | None:
    """Busca un usuario por su nombre. Devuelve None si no existe."""
    conexion = obtener_conexion()
    fila = conexion.execute(
        "SELECT usuario, contrasena_hash FROM usuarios WHERE usuario = ?",
        (usuario,),
    ).fetchone()
    conexion.close()

    if fila is None:
        return None
    return Usuario(fila["usuario"], fila["contrasena_hash"])
