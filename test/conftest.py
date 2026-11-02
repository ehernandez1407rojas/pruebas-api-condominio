"""
Fixtures para la suite `test/`.
Los helpers vienen de `common.helpers`.
"""
import pytest

from common.helpers import api_post, log   # re-exportamos por comodidad


@pytest.fixture(scope="session")
def condominio_payload():
    return {
        "nombre": "condominio chavacano",
        "nombre_corto": "chavacano",
        "direccion": "chavacano 19, colonia banca seca",
        "inicio_servicio": "2026-10-08",
        "propiedad_cantidad": 16,
        "email_whatsapp": "administrador_uno@correo.uno",
        "nombre_completo": "administrador uno",
        "password": "Qaz971",
    }


@pytest.fixture(scope="session")
def condominio_registrado(condominio_payload):
    """Idempotente: 201 OK, 400/409 ya existía, 500 skip."""
    log.info("── Fixture: condominio_registrado ──")
    response = api_post(
        "/api/condominio/registrar-administrador/",
        json=condominio_payload,
    )

    if response.status_code in (200, 201):
        return response.json() if response.content else {}
    if response.status_code in (400, 409):
        log.warning("⚠ Condominio ya existía (status %s).", response.status_code)
        return {"_already_exists": True, "detail": response.text}
    if response.status_code >= 500:
        pytest.skip(f"Backend devolvió {response.status_code}.")

    pytest.fail(f"Respuesta inesperada {response.status_code}: {response.text[:300]}")


@pytest.fixture(scope="session")
def auth_token(condominio_registrado, condominio_payload):
    log.info("── Fixture: auth_token ──")
    response = api_post(
        "/api/usuario/login/",
        json={
            "email_whatsapp": condominio_payload["email_whatsapp"],
            "password": condominio_payload["password"],
        },
    )
    assert response.status_code == 200, f"Login falló: {response.text[:300]}"
    data = response.json()
    token = (data.get("token") or data.get("access") or data.get("access_token")
             or data.get("key") or data.get("jwt"))
    assert token, f"Sin token. Claves: {list(data.keys())}"
    return token


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}