"""
Helpers compartidos para todas las pruebas.
No depende de pytest; cualquier test lo puede importar.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

import requests


# ============================================================
#   CONFIGURACIÓN
# ============================================================

BASE_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 15


# ============================================================
#   LOGGING
# ============================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"test_{datetime.now():%Y%m%d_%H%M%S}.log"

if not logging.getLogger("api-tests").handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s → %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

log = logging.getLogger("api-tests")


def _mask_headers(headers: dict | None) -> dict:
    if not headers:
        return {}
    return {
        k: (v[:15] + "...(truncado)"
            if k.lower() == "authorization" and isinstance(v, str) and len(v) > 15
            else v)
        for k, v in headers.items()
    }


# ============================================================
#   HELPER api_post
# ============================================================

def api_post(path, json=None, headers=None, timeout=REQUEST_TIMEOUT, **kwargs):
    """POST con logging automático."""
    url = f"{BASE_URL}{path}"
    log.info("→ POST %s", url)
    if json is not None:
        log.info("  payload: %s", json)
    if headers:
        log.info("  headers: %s", _mask_headers(headers))

    try:
        response = requests.post(url, json=json, headers=headers,
                                 timeout=timeout, **kwargs)
    except requests.exceptions.ConnectionError as e:
        log.error("✗ ConnectionError: %s", e)
        # ⚠️ NO usamos pytest.fail aquí para mantener helpers agnósticos
        raise RuntimeError(
            f"No se pudo conectar al backend en {url}. Detalle: {e}"
        ) from e
    except requests.exceptions.Timeout:
        log.error("✗ Timeout tras %ss", timeout)
        raise RuntimeError(f"Timeout de {timeout}s en {url}")

    body_preview = response.text[:300] + ("..." if len(response.text) > 300 else "")
    log.info("← %s %s", response.status_code, body_preview)
    return response