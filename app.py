#!/usr/bin/env python3
"""AgroCalc Web - Ponto de entrada principal."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    app.logger.info("Iniciando AgroCalc Web na porta %d (debug=%s)", port, debug)
    app.run(host="0.0.0.0", port=port, debug=debug)
