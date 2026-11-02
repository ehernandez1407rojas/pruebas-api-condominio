import pytest
from common.helpers import log

def test_definir_cuotas(condominio_data, cuotas_definidas):
    """
    Prueba la creación de la cuota ordinaria y extraordinaria.
    """
    nombre_corto = condominio_data["nombre_corto"]
    
    log.info("=" * 60)
    log.info("Definiendo cuotas para [%s]", nombre_corto)
    log.info("=" * 60)
    
    assert len(cuotas_definidas) == 2, f"Se esperaban 2 cuotas en [{nombre_corto}]"
    
    for cuota in cuotas_definidas:
        log.info("✓ Cuota validada: %s", cuota["nombre"])
        
    log.info("-" * 60)
    log.info("Resumen [%s]: cuotas procesadas correctamente.", nombre_corto)
    log.info("-" * 60)


def test_registrar_conserjes(condominio_data, conserjes_registrados):
    """
    Prueba la creación de los dos conserjes.
    """
    nombre_corto = condominio_data["nombre_corto"]
    
    log.info("=" * 60)
    log.info("Registrando conserjes para [%s]", nombre_corto)
    log.info("=" * 60)
    
    assert len(conserjes_registrados) == 2, f"Se esperaban 2 conserjes en [{nombre_corto}]"
    
    for conserje in conserjes_registrados:
        log.info("✓ Conserje validado: %s", conserje["nombre_completo"])
        
    log.info("-" * 60)
    log.info("Resumen [%s]: conserjes procesados correctamente.", nombre_corto)
    log.info("-" * 60)