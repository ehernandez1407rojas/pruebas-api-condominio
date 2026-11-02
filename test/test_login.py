from common.helpers import api_post


def test_login_exitoso(condominio_payload):
    response = api_post(
        "/api/usuario/login/",
        json={
            "email_whatsapp": condominio_payload["email_whatsapp"],
            "password": condominio_payload["password"],
        },
    )
    assert response.status_code == 200
    assert response.json()


def test_login_password_incorrecto(condominio_payload):
    response = api_post(
        "/api/usuario/login/",
        json={
            "email_whatsapp": condominio_payload["email_whatsapp"],
            "password": "password_malo",
        },
    )
    assert response.status_code in (400, 401)