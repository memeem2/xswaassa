#!/usr/bin/env python3
"""Run Charger Monitor server (dev or Pi)."""

from __future__ import annotations

import sys
from pathlib import Path

import uvicorn

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

from app.config import load_settings  # noqa: E402


def main() -> None:
    settings = load_settings()
    ssl_cert = Path(settings.ssl_cert)
    ssl_key = Path(settings.ssl_key)

    kwargs: dict = {
        "app": "app.main:app",
        "host": settings.host,
        "port": settings.port,
        "log_level": "info",
    }

    if ssl_cert.is_file() and ssl_key.is_file():
        kwargs["ssl_certfile"] = str(ssl_cert)
        kwargs["ssl_keyfile"] = str(ssl_key)
        print(f"HTTPS: https://0.0.0.0:{settings.port}")
    else:
        print(f"HTTP (no SSL certs found): http://0.0.0.0:{settings.port}")
        print("Phones need HTTPS for camera - run scripts/generate-cert.sh on Pi")

    uvicorn.run(**kwargs)


if __name__ == "__main__":
    main()