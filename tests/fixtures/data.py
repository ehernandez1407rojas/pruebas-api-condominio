# tests/fixtures/data.py
"""
Datos de prueba centralizados.

Cada condominio define su propio `prefijo_telefono` para garantizar
que los email_whatsapp (unique=True) NO colisionen entre condominios.
Formato final: {prefijo_telefono}{secuencial} → 10 dígitos.
"""

CONDOMINIOS = [
    {
        "nombre": "condominio uno",
        "nombre_corto": "uno",
        "direccion": "domicilio uno",
        "inicio_servicio": "2026-10-08",
        "propiedad_cantidad": 16,
        "email_whatsapp": "administrador_uno@correo.uno",
        "nombre_completo": "administrador uno",
        "password": "Qaz971",
        "prefijo_telefono": "5511",     # 👈 nuevo
    },
    {
        "nombre": "condominio dos",
        "nombre_corto": "dos",
        "direccion": "domicilio dos",
        "inicio_servicio": "2026-10-08",
        "propiedad_cantidad": 6,
        "email_whatsapp": "administrador_dos@correo.dos",
        "nombre_completo": "administrador dos",
        "password": "Qaz971",
        "prefijo_telefono": "5522",     # 👈 nuevo
    },
    {
        "nombre": "condominio tres",
        "nombre_corto": "tres",
        "direccion": "domicilio tres",
        "inicio_servicio": "2026-10-08",
        "propiedad_cantidad": 7,
        "email_whatsapp": "administrador_tres@correo.tres",
        "nombre_completo": "administrador tres",
        "password": "Qaz971",
        "prefijo_telefono": "5533",     # 👈 nuevo
    },
]


def generar_propiedades(condominio: dict) -> list[dict]:
    """
    Genera N propiedades para un condominio dado.

    email_whatsapp = f"{prefijo_telefono}{i:06d}"
    → "5511" + "000001" = "5511000001"  (10 dígitos)
    → "5522" + "000001" = "5522000001"
    → "5533" + "000001" = "5533000001"

    Así cada condominio tiene su bloque de teléfonos y no colisiona.
    """
    cantidad = condominio["propiedad_cantidad"]
    nombre_cond = condominio["nombre"]              # "condominio uno"
    nombre_corto = condominio["nombre_corto"]       # "uno"
    prefijo = condominio["prefijo_telefono"]        # "5511"

    propiedades = []
    for i in range(1, cantidad + 1):
        num = f"{i:02d}"                             # "01", "02", ..., "16"
        telefono = f"{prefijo}{i:06d}"               # 4 + 6 = 10 dígitos
        propiedades.append({
            "nombre_propiedad": f"{nombre_cond} casa {num}",
            "direccion": f"casa {num}",
            "email_whatsapp": telefono,
            "nombre_completo": f"propietario {nombre_corto} {num}",
        })
    return propiedades

    # Agregar al final de tests/fixtures/data.py

def generar_cuotas(condominio: dict) -> list[dict]:
    """Genera las cuotas ordinaria y extraordinaria para un condominio."""
    nombre_corto = condominio["nombre_corto"]
    return [
        {
            "tipo_cuota": 1,
            "nombre": f"codominio {nombre_corto} cuota ordinaria ejercicio 2026",
            "importe": "4000",
            "aplica_desde": "2026-10-17",
            "aplica_hasta": "2027-10-17",
        },
        {
            "tipo_cuota": 2,
            "nombre": f"codominio {nombre_corto} cuota extraordinaria 12 diciembre 2026",
            "importe": "5000",
            "aplica_desde": "2026-12-01",
            "aplica_hasta": "2027-10-12",
        }
    ]

def generar_conserjes(condominio: dict) -> list[dict]:
    """Genera dos conserjes para un condominio."""
    nombre_corto = condominio["nombre_corto"]
    ## prefijo = condominio["prefijo_telefono"] # Usamos el mismo prefijo para no colisionar voy a usar correo
    
    return [
        {
            "email_whatsapp": f"condominio_{nombre_corto}_conserje_uno@correo.com", # lo cambie a correos
            "nombre_completo": f"condominio {nombre_corto} conserje uno"
        },
        {
            "email_whatsapp": f"condominio_{nombre_corto}_conserje_dos@correo.com",
            "nombre_completo": f"condominio {nombre_corto} conserje dos"
        }
    ]