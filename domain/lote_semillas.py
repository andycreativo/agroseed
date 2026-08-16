"""
Modulo domain.lote_semillas
Define las clases RegistroGerminacion y LoteSemillas, encargadas de
representar y evaluar el proceso de germinacion de un lote de semillas.
Esta capa no depende de Flask ni de SQLite: solo contiene reglas de negocio.
"""
from domain.tipo_semilla import TipoSemilla


class RegistroGerminacion:
    """Representa la cantidad de semillas que germinaron en una semana especifica."""

    def __init__(self, semana: int, cantidad_germinadas: int):
        self.semana = semana
        self.cantidad_germinadas = cantidad_germinadas


class LoteSemillas:
    """
    Representa un lote de semillas de un cultivo especifico (maiz, frijol, etc.)
    y controla su proceso de germinacion semana a semana.
    """

    SEMANA_EVALUACION = 3  # Numero de semanas requeridas antes del dictamen final

    def __init__(self, id_lote: str, cultivo: str, total_semillas: int, tipo_semilla: TipoSemilla):
        self.id_lote = id_lote
        self.cultivo = cultivo
        self.total_semillas = total_semillas
        self.tipo_semilla = tipo_semilla
        self.semana_actual = 0
        self.registros_germinacion: list[RegistroGerminacion] = []
        self.cantidad_disponible = total_semillas

    def avanzar_semana(self) -> None:
        """Incrementa en uno el contador de semanas transcurridas del lote."""
        self.semana_actual += 1

    def registrar_germinadas(self, cantidad: int) -> bool:
        """
        Registra la cantidad de semillas germinadas en la semana actual.
        Valida que la suma acumulada no supere el total de semillas sembradas.
        Devuelve True si el registro fue exitoso, False si fue rechazado.
        """
        total_registrado = sum(r.cantidad_germinadas for r in self.registros_germinacion)

        if cantidad < 0:
            return False

        if total_registrado + cantidad > self.total_semillas:
            return False

        registro = RegistroGerminacion(self.semana_actual, cantidad)
        self.registros_germinacion.append(registro)
        return True

    def calcular_porcentaje_germinacion(self) -> float:
        """Calcula el porcentaje de germinacion acumulado del lote."""
        if not self.registros_germinacion:
            return 0.0
        total_germinadas = sum(r.cantidad_germinadas for r in self.registros_germinacion)
        return round((total_germinadas / self.total_semillas) * 100, 2)

    def esta_listo_para_evaluacion(self) -> bool:
        """Indica si el lote ya cumplio las semanas minimas para emitir un dictamen."""
        return self.semana_actual >= LoteSemillas.SEMANA_EVALUACION

    def es_apto(self) -> bool:
        """
        Determina si el lote es apto, comparando el porcentaje de germinacion
        contra el minimo requerido segun su tipo de semilla.
        """
        return self.calcular_porcentaje_germinacion() >= self.tipo_semilla.porcentaje_minimo()

    def vender(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero")
        if cantidad > self.cantidad_disponible:
            raise ValueError("No hay suficiente cantidad disponible en el lote")
        self.cantidad_disponible -= cantidad
        return self.cantidad_disponible

    def esta_agotado(self):
        return self.cantidad_disponible <= 0
    