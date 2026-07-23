# ============================================================
#  SISTEMA AGROSEED — Gestión de Lotes de Semillas
# ============================================================
from abc import ABC, abstractmethod

print("Bienvenido al Sistema AGROSEED")
print("=" * 45)


# --- 1. TIPOS DE SEMILLAS (POLIMORFISMO) ---
class TipoSemilla(ABC):
    """Clase base para cualquier tipo de semilla."""

    @abstractmethod
    def describir(self) -> str:
        pass

    @abstractmethod
    def porcentaje_minimo(self) -> float:
        pass


class SemillaCertificada(TipoSemilla):
    def describir(self) -> str:
        return "Semilla Certificada: Tratada en laboratorio, alta resistencia a plagas."

    def porcentaje_minimo(self) -> float:
        return 85.0


class SemillaCriolla(TipoSemilla):
    def describir(self) -> str:
        return "Semilla Criolla: Conservada localmente, adaptada al suelo de la región."

    def porcentaje_minimo(self) -> float:
        return 70.0


class SemillaHibrida(TipoSemilla):
    def describir(self) -> str:
        return "Semilla Híbrida: Cruce controlado entre variedades, mayor rendimiento por hectárea."

    def porcentaje_minimo(self) -> float:
        return 90.0


class SemillaOrganica(TipoSemilla):
    def describir(self) -> str:
        return "Semilla Orgánica: Sin tratamientos químicos, apta para cultivo ecológico certificado."

    def porcentaje_minimo(self) -> float:
        return 75.0


class SemillaTratada(TipoSemilla):
    def describir(self) -> str:
        return "Semilla Tratada: Recubierta con fungicida/insecticida para protección inicial."

    def porcentaje_minimo(self) -> float:
        return 88.0


# --- 2. REGISTRO SEMANAL DE GERMINACIÓN ---
class RegistroGerminacion:
    """Guarda cuántas semillas brotaron en una semana específica."""

    def __init__(self, semana: int, cantidad_germinadas: int):
        self.semana = semana
        self.cantidad_germinadas = cantidad_germinadas


# --- 3. CLASE PRINCIPAL: LOTE DE SEMILLAS ---
class LoteSemillas:
    SEMANA_EVALUACION = 3

    def __init__(self, id_lote: str, cultivo: str, total_semillas: int, tipo_semilla: TipoSemilla):
        self.id_lote = id_lote
        self.cultivo = cultivo
        self.total_semillas = total_semillas
        self.tipo_semilla = tipo_semilla
        self.semana_actual = 0
        self.registros_germinacion: list[RegistroGerminacion] = []

        print(f"\n[SISTEMA] Lote '{id_lote}' — Cultivo: {cultivo}")
        print(f"[INFO]    {tipo_semilla.describir()}")
        print(f"[INFO]    Semillas sembradas: {total_semillas}")

    def avanzar_semana(self):
        self.semana_actual += 1
        print(f"\n--- Semana {self.semana_actual} ---")

    def registrar_germinadas(self, cantidad: int):
        total_registrado = sum(r.cantidad_germinadas for r in self.registros_germinacion)
        if total_registrado + cantidad > self.total_semillas:
            print(f"  [ERROR] Cantidad inválida: superaría el total de {self.total_semillas} semillas.")
            return

        registro = RegistroGerminacion(self.semana_actual, cantidad)
        self.registros_germinacion.append(registro)
        print(f"  Plántulas viables esta semana: {cantidad}")

    def calcular_porcentaje_germinacion(self) -> float:
        if not self.registros_germinacion:
            return 0.0
        total_germinadas = sum(r.cantidad_germinadas for r in self.registros_germinacion)
        return round((total_germinadas / self.total_semillas) * 100, 2)

    def evaluar_lote(self):
        print(f"\n{'=' * 45}")
        print(f"  INFORME DE EVALUACIÓN — LOTE: {self.id_lote}")
        print(f"  Cultivo: {self.cultivo}")
        print(f"{'=' * 45}")

        if self.semana_actual < LoteSemillas.SEMANA_EVALUACION:
            faltantes = LoteSemillas.SEMANA_EVALUACION - self.semana_actual
            print(f"  Estado: En desarrollo. Faltan {faltantes} semana(s) para evaluación.")
            return

        porcentaje = self.calcular_porcentaje_germinacion()
        minimo = self.tipo_semilla.porcentaje_minimo()
        total_germinadas = sum(r.cantidad_germinadas for r in self.registros_germinacion)

        print(f"  Semillas sembradas  : {self.total_semillas}")
        print(f"  Total germinadas    : {total_germinadas}")
        print(f"  Tasa de germinación : {porcentaje}%")
        print(f"  Mínimo requerido    : {minimo}%")

        if porcentaje >= minimo:
            print(f"\n  ✅ DICTAMEN: LOTE APTO — Pasar a bandejas de levante.")
        else:
            print(f"\n  ❌ DICTAMEN: LOTE RECHAZADO — Rendimiento inferior al mínimo.")
        print(f"{'=' * 45}")


# ============================================================
#  SIMULACIÓN: CICLO PRODUCTIVO — 5 CULTIVOS
# ============================================================

if __name__ == "__main__":

    # — Lote 1: Maíz — Semilla Certificada —
    lote_maiz = LoteSemillas("LOT-MAIZ-2026", "Maíz", 1200, SemillaCertificada())
    lote_maiz.avanzar_semana()
    lote_maiz.registrar_germinadas(350)
    lote_maiz.avanzar_semana()
    lote_maiz.registrar_germinadas(500)
    lote_maiz.avanzar_semana()
    lote_maiz.registrar_germinadas(200)
    lote_maiz.evaluar_lote()

    # — Lote 2: Frijol — Semilla Criolla —
    lote_frijol = LoteSemillas("LOT-FRIJOL-2026", "Frijol", 800, SemillaCriolla())
    lote_frijol.avanzar_semana()
    lote_frijol.registrar_germinadas(180)
    lote_frijol.avanzar_semana()
    lote_frijol.registrar_germinadas(300)
    lote_frijol.avanzar_semana()
    lote_frijol.registrar_germinadas(220)
    lote_frijol.evaluar_lote()

    # — Lote 3: Arroz — Semilla Híbrida —
    lote_arroz = LoteSemillas("LOT-ARROZ-2026", "Arroz", 2000, SemillaHibrida())
    lote_arroz.avanzar_semana()
    lote_arroz.registrar_germinadas(600)
    lote_arroz.avanzar_semana()
    lote_arroz.registrar_germinadas(800)
    lote_arroz.avanzar_semana()
    lote_arroz.registrar_germinadas(500)
    lote_arroz.evaluar_lote()

    # — Lote 4: Tomate — Semilla Orgánica —
    lote_tomate = LoteSemillas("LOT-TOMATE-2026", "Tomate", 500, SemillaOrganica())
    lote_tomate.avanzar_semana()
    lote_tomate.registrar_germinadas(120)
    lote_tomate.avanzar_semana()
    lote_tomate.registrar_germinadas(200)
    lote_tomate.avanzar_semana()
    lote_tomate.registrar_germinadas(80)
    lote_tomate.evaluar_lote()

    # — Lote 5: Pimentón — Semilla Tratada —
    lote_pimenton = LoteSemillas("LOT-PIMENTON-2026", "Pimentón", 600, SemillaTratada())
    lote_pimenton.avanzar_semana()
    lote_pimenton.registrar_germinadas(150)
    lote_pimenton.avanzar_semana()
    lote_pimenton.registrar_germinadas(280)
    lote_pimenton.avanzar_semana()
    lote_pimenton.registrar_germinadas(160)
    lote_pimenton.evaluar_lote()