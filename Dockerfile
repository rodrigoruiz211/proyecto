# Root Dockerfile to support Railway builds for a monorepo.
# This file copies the backend/ folder into the image and starts uvicorn.
FROM python:3.11-slim

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

# Copy and install Python deps (take from backend/ to support repo-root build context)
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend app sources
COPY backend/ .

ENV PORT 8000
EXPOSE 8000

# Start uvicorn using PORT env var injected by Railway
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
