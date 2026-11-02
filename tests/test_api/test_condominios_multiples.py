from common.helpers import api_post, log


def test_condominio_queda_registrado(condominio_registrado, condominio_data):
    assert condominio_registrado is not None
    if condominio_registrado.get("_already_exists"):
        log.info("✓ Condominio '%s' ya existía.", condominio_data["nombre_corto"])
    else:
        log.info("✓ Condominio '%s' registrado en esta sesión.",
                 condominio_data["nombre_corto"])


def test_condominio_duplicado_devuelve_409(condominio_registrado, condominio_data):
    response = api_post(
        "/api/condominio/registrar-administrador/",
        json=condominio_data,
    )
    assert response.status_code in (400, 409)