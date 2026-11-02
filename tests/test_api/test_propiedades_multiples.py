from common.helpers import api_post, log


def test_registrar_todas_las_propiedades(
    condominio_data, propiedades_de_condominio, auth_headers
):
    nombre_corto = condominio_data["nombre_corto"]
    total = len(propiedades_de_condominio)

    log.info("=" * 60)
    log.info("Registrando %d propiedades para [%s]", total, nombre_corto)
    log.info("=" * 60)

    creadas = 0
    ya_existian = 0
    errores = []

    for idx, propiedad in enumerate(propiedades_de_condominio, start=1):
        response = api_post(
            "/api/propiedad/registrar-propietario-token/",
            json=propiedad,
            headers=auth_headers,
        )

        if response.status_code == 201:
            creadas += 1
            log.info("  [%d/%d] ✓ Creada: %s", idx, total, propiedad["nombre_propiedad"])
        elif response.status_code == 409:
            ya_existian += 1
            log.warning("  [%d/%d] ⚠ Ya existía: %s",
                        idx, total, propiedad["nombre_propiedad"])
        else:
            errores.append({
                "indice": idx,
                "propiedad": propiedad["nombre_propiedad"],
                "status": response.status_code,
                "detalle": response.text[:200],
            })
            log.error("  [%d/%d] ✗ FALLÓ: %s (status %s)",
                      idx, total, propiedad["nombre_propiedad"], response.status_code)

    log.info("-" * 60)
    log.info("Resumen [%s]: creadas=%d, ya_existían=%d, errores=%d",
             nombre_corto, creadas, ya_existian, len(errores))
    log.info("-" * 60)

    assert not errores, (
        f"Fallaron {len(errores)} propiedades en [{nombre_corto}]:\n"
        + "\n".join(
            f"  - [{e['indice']}] {e['propiedad']} → {e['status']}: {e['detalle']}"
            for e in errores
        )
    )
    assert creadas + ya_existian == total