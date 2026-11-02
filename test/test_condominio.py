from common.helpers import api_post, log


def test_registrar_condominio(condominio_registrado):
    assert condominio_registrado is not None
    if condominio_registrado.get("_already_exists"):
        log.warning("Test corrió sobre condominio preexistente.")


def test_registrar_condominio_payload_invalido():
    response = api_post("/api/condominio/registrar-administrador/", json={})
    assert response.status_code == 400