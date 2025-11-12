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
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

ENV PORT 8000
EXPOSE 8000

# Start uvicorn (use PORT if provided by environment)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
