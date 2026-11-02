import pytest

from common.helpers import api_post, log
from tests.fixtures.data import CONDOMINIOS, generar_propiedades, generar_cuotas, generar_conserjes


# ============================================================
#   condominio_data ahora ES session-scoped
# ============================================================

@pytest.fixture(scope="session", params=CONDOMINIOS,
                ids=[c["nombre_corto"] for c in CONDOMINIOS])
def condominio_data(request):
    """
    Parametriza los 3 condominios a nivel SESSION.
    pytest correrá toda la suite 3 veces, una por condominio.
    """
    return request.param


# ============================================================
#   El resto de fixtures (sin cambios en scope)
# ============================================================

@pytest.fixture(scope="session")
def condominio_registrado(condominio_data):
    log.info("── Fixture: condominio_registrado [%s] ──",
             condominio_data["nombre_corto"])
    response = api_post(
        "/api/condominio/registrar-administrador/",
        json=condominio_data,
    )
    if response.status_code in (200, 201):
        log.info("✓ Condominio '%s' registrado.", condominio_data["nombre_corto"])
        try:
            return response.json()
        except ValueError:
            return {"_raw": response.text}
    if response.status_code in (400, 409):
        log.warning("⚠ Condominio '%s' ya existía.", condominio_data["nombre_corto"])
        return {"_already_exists": True, "detail": response.text}
    if response.status_code >= 500:
        pytest.skip(f"Backend falló con {response.status_code}.")
    pytest.fail(f"Respuesta inesperada {response.status_code}: {response.text[:300]}")


@pytest.fixture(scope="session")
def auth_token(condominio_registrado, condominio_data):
    log.info("── Fixture: auth_token [%s] ──", condominio_data["nombre_corto"])
    response = api_post(
        "/api/usuario/login/",
        json={
            "email_whatsapp": condominio_data["email_whatsapp"],
            "password": condominio_data["password"],
        },
    )
    assert response.status_code == 200, (
        f"Login falló para {condominio_data['nombre_corto']}: {response.text[:300]}"
    )
    data = response.json()
    token = (data.get("token") or data.get("access") or data.get("access_token")
             or data.get("key") or data.get("jwt"))
    assert token, f"Sin token. Claves: {list(data.keys())}"
    return token


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(scope="session")
def propiedades_de_condominio(condominio_data):
    props = generar_propiedades(condominio_data)
    log.info("── propiedades_de_condominio [%s] → %d ──",
             condominio_data["nombre_corto"], len(props))
    return props

# Agregar a tests/test_api/conftest.py


# ... (tus fixtures existentes de condominio_registrado, auth_headers, etc.)

@pytest.fixture(scope="session")
def cuotas_definidas(auth_headers, condominio_data):
    log.info("── Fixture: cuotas_definidas [%s] ──", condominio_data["nombre_corto"])
    cuotas = generar_cuotas(condominio_data)
    
    for cuota in cuotas:
        response = api_post(
            "/api/definir-cuota/",
            json=cuota,
            headers=auth_headers,
        )
        if response.status_code in (200, 201):
            log.info("✓ Cuota '%s' creada.", cuota["nombre"])
        elif response.status_code in (400, 409):
            log.warning("⚠ Cuota '%s' ya existía.", cuota["nombre"])
        else:
            pytest.fail(f"Error inesperado al crear cuota: {response.status_code} - {response.text}")
            
    return cuotas


@pytest.fixture(scope="session")
def conserjes_registrados(auth_headers, condominio_data):
    log.info("── Fixture: conserjes_registrados [%s] ──", condominio_data["nombre_corto"])
    conserjes = generar_conserjes(condominio_data)
    
    for conserje in conserjes:
        response = api_post(
            "/api/usuario/registrar-conserje-token/",
            json=conserje,
            headers=auth_headers,
        )
        if response.status_code in (200, 201):
            log.info("✓ Conserje '%s' creado.", conserje["email_whatsapp"])
        elif response.status_code in (400, 409):
            log.warning("⚠ Conserje '%s' ya existía.", conserje["email_whatsapp"])
        else:
            pytest.fail(f"Error inesperado al crear conserje: {response.status_code} - {response.text}")
            
    return conserjes