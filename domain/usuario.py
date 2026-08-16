"""
Modulo domain.usuario
Entidad de dominio que representa a un usuario del sistema Agroseed.
"""


class Usuario:
    """Representa un usuario registrado en el sistema."""

    def __init__(self, usuario: str, contrasena_hash: str):
        self.usuario = usuario
        self.contrasena_hash = contrasena_hash
