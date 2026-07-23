"""
Modulo infrastructure.database
Encargado de la conexion a la base de datos SQLite y de crear
las tablas necesarias si no existen todavia.
"""
import sqlite3
import os

NOMBRE_BASE_DATOS = "agroseed.db"


def obtener_conexion() -> sqlite3.Connection:
    """Crea y devuelve una conexion a la base de datos SQLite del proyecto."""
    conexion = sqlite3.connect(NOMBRE_BASE_DATOS)
    conexion.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conexion


def inicializar_base_datos() -> None:
    """
    Crea las tablas lotes_semillas y registros_germinacion si no existen.
    Debe llamarse una vez al iniciar la aplicacion (ver main.py).
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lotes_semillas (
            id_lote TEXT PRIMARY KEY,
            cultivo TEXT NOT NULL,
            total_semillas INTEGER NOT NULL,
            tipo_semilla TEXT NOT NULL,
            semana_actual INTEGER NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_germinacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_lote TEXT NOT NULL,
            semana INTEGER NOT NULL,
            cantidad_germinadas INTEGER NOT NULL,
            FOREIGN KEY (id_lote) REFERENCES lotes_semillas (id_lote)
        )
    """)

    conexion.commit()
    conexion.close()
    