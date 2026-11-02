from common.helpers import api_post


def test_registrar_propiedad_con_propietario(auth_headers):
    payload = {
        "nombre_propiedad": "casa de don Luis",
        "direccion": "casa 12",
        "email_whatsapp": "5524120900",
        "nombre_completo": "luis hernandez",
    }
    response = api_post(
        "/api/propiedad/registrar-propietario-token/",
        json=payload,
        headers=auth_headers,
    )
    assert response.status_code in (200, 201, 409)


def test_registrar_propiedad_sin_token():
    payload = {
        "nombre_propiedad": "casa sin auth",
        "direccion": "casa 99",
        "email_whatsapp": "5500000000",
        "nombre_completo": "sin token",
    }
    response = api_post("/api/propiedad/registrar-propietario-token/", json=payload)
    assert response.status_code == 401