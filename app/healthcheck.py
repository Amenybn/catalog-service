"""Sonde de santé : python -m app.healthcheck (code 0 si /health répond)."""
import os
import sys
import urllib.request

try:
    with urllib.request.urlopen(f"http://127.0.0.1:{os.getenv('PORT', '8001')}/health", timeout=3) as res:
        sys.exit(0 if res.status == 200 else 1)
except Exception:
    sys.exit(1)
