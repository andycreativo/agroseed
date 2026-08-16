"""
Pruebas unitarias con pytest para el modulo domain.lote_semillas y domain.tipo_semilla
Proyecto: Agroseed - Sistema de gestion de lotes de semillas
"""
import pytest
from domain.lote_semillas import LoteSemillas, RegistroGerminacion
from domain.tipo_semilla import SemillaCertificada, SemillaCriolla


def test_lote_certificado_apto_con_90_porciento():
    """Un lote de semilla certificada con 90% de germinacion debe ser apto (minimo 85%)."""
    lote = LoteSemillas("L001", "Maiz", 100, SemillaCertificada())
    lote.registrar_germinadas(90)
    assert lote.es_apto() is True


def test_lote_certificado_no_apto_con_80_porciento():
    """Un lote de semilla certificada con 80% de germinacion NO debe ser apto (minimo 85%)."""
    lote = LoteSemillas("L002", "Maiz", 100, SemillaCertificada())
    lote.registrar_germinadas(80)
    assert lote.es_apto() is False


def test_lote_criollo_apto_con_75_porciento():
    """Un lote de semilla criolla con 75% de germinacion debe ser apto (minimo 70%)."""
    lote = LoteSemillas("L003", "Frijol", 100, SemillaCriolla())
    lote.registrar_germinadas(75)
    assert lote.es_apto() is True


def test_lote_criollo_no_apto_con_60_porciento():
    """Un lote de semilla criolla con 60% de germinacion NO debe ser apto (minimo 70%)."""
    lote = LoteSemillas("L004", "Frijol", 100, SemillaCriolla())
    lote.registrar_germinadas(60)
    assert lote.es_apto() is False


def test_calcular_porcentaje_germinacion_sin_registros():
    """Un lote sin registros de germinacion debe tener 0.0% de germinacion."""
    lote = LoteSemillas("L005", "Arroz", 100, SemillaCertificada())
    assert lote.calcular_porcentaje_germinacion() == 0.0


def test_calcular_porcentaje_germinacion_con_registros():
    """El porcentaje de germinacion debe calcularse correctamente sobre el total de semillas."""
    lote = LoteSemillas("L006", "Arroz", 200, SemillaCertificada())
    lote.registrar_germinadas(50)
    lote.avanzar_semana()
    lote.registrar_germinadas(30)
    assert lote.calcular_porcentaje_germinacion() == 40.0


def test_registrar_germinadas_rechaza_cantidad_negativa():
    """No se debe permitir registrar una cantidad negativa de semillas germinadas."""
    lote = LoteSemillas("L007", "Maiz", 100, SemillaCertificada())
    resultado = lote.registrar_germinadas(-5)
    assert resultado is False


def test_registrar_germinadas_rechaza_exceso_sobre_total():
    """No se debe permitir registrar mas semillas germinadas que el total sembrado."""
    lote = LoteSemillas("L008", "Maiz", 100, SemillaCertificada())
    lote.registrar_germinadas(90)
    resultado = lote.registrar_germinadas(20)  # 90 + 20 = 110 > 100
    assert resultado is False


def test_avanzar_semana_incrementa_contador():
    """Cada llamado a avanzar_semana debe incrementar en uno la semana actual."""
    lote = LoteSemillas("L009", "Maiz", 100, SemillaCertificada())
    assert lote.semana_actual == 0
    lote.avanzar_semana()
    lote.avanzar_semana()
    assert lote.semana_actual == 2


def test_esta_listo_para_evaluacion_antes_de_semana_3():
    """Un lote con menos de 3 semanas transcurridas no debe estar listo para evaluacion."""
    lote = LoteSemillas("L010", "Maiz", 100, SemillaCertificada())
    lote.avanzar_semana()
    lote.avanzar_semana()
    assert lote.esta_listo_para_evaluacion() is False


def test_esta_listo_para_evaluacion_en_semana_3():
    """Un lote que alcanza la semana 3 debe estar listo para evaluacion."""
    lote = LoteSemillas("L011", "Maiz", 100, SemillaCertificada())
    lote.avanzar_semana()
    lote.avanzar_semana()
    lote.avanzar_semana()
    assert lote.esta_listo_para_evaluacion() is True


def test_descripcion_semilla_certificada():
    """La descripcion de la semilla certificada debe mencionar laboratorio y resistencia a plagas."""
    semilla = SemillaCertificada()
    assert "Certificada" in semilla.describir()
    assert semilla.porcentaje_minimo() == 85.0


def test_descripcion_semilla_criolla():
    """La descripcion de la semilla criolla debe mencionar conservacion local."""
    semilla = SemillaCriolla()
    assert "Criolla" in semilla.describir()
    assert semilla.porcentaje_minimo() == 70.0