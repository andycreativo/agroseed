"""
Modulo domain.tipo_semilla
Define la clase abstracta TipoSemilla y sus implementaciones concretas.
Cumple el requerimiento de polimorfismo: cada tipo de semilla define
su propio umbral minimo de germinacion.
"""
from abc import ABC, abstractmethod


class TipoSemilla(ABC):
    """Clase base abstracta para cualquier tipo de semilla del sistema."""

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripcion textual del tipo de semilla."""
        pass

    @abstractmethod
    def porcentaje_minimo(self) -> float:
        """Devuelve el porcentaje minimo de germinacion para aprobar el lote."""
        pass


class SemillaCertificada(TipoSemilla):
    """Semilla tratada en laboratorio, con alta resistencia a plagas."""

    def describir(self) -> str:
        return "Semilla Certificada: Tratada en laboratorio, alta resistencia a plagas."

    def porcentaje_minimo(self) -> float:
        return 85.0


class SemillaCriolla(TipoSemilla):
    """Semilla conservada localmente, adaptada al suelo de la region."""

    def describir(self) -> str:
        return "Semilla Criolla: Conservada localmente, adaptada al suelo de la region."

    def porcentaje_minimo(self) -> float:
        return 70.0
    