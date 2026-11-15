"""
WSGI entry point for production deployments (Render, Railway, PythonAnywhere, etc.)
"""

import sys
from pathlib import Path

# Add project root to Python search path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from web.app import app

if __name__ == "__main__":
    app.run()
