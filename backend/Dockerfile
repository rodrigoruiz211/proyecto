# Minimal Dockerfile for FastAPI backend
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system deps needed by opencv and mediapipe
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps
# When Railway builds from the repository root, the build context may be the repo root
# so reference the backend/ path explicitly. This keeps the Dockerfile robust for
# both local 'docker build ./backend' and remote builds that use the repo root context.
COPY backend/requirements.txt ./
# Ensure pip/setuptools/wheel are up-to-date to avoid build issues when
# installing some binary wheels (numpy, mediapipe, etc.). Then install deps.
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# Copy only the backend application files into the image
# Use backend/ as source because the Docker build context may point to the repo root.
COPY backend/ .

ENV PORT 8000
EXPOSE 8000

# Start uvicorn (use PORT if provided by environment)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
