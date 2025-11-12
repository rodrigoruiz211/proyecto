#!/usr/bin/env bash
set -euo pipefail

# Simple start script for Railway / Railpack to run the backend inside a monorepo.
# It installs Python deps and launches uvicorn from the backend/ directory.

# Move to backend directory
cd backend

# Ensure pip is available and upgrade
python3 -m pip install --upgrade pip setuptools

# Install requirements
pip install --no-cache-dir -r requirements.txt

# Default CAMERA_SOURCE to 'none' if not set
export CAMERA_SOURCE=${CAMERA_SOURCE:-none}

# Start Uvicorn on the configured PORT
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
