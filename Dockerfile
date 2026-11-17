# Use official lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5002

# Set working directory
WORKDIR /app

# Install system dependencies (curl for healthcheck, portaudio for audio if needed, gcc for C extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    portaudio19-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose default port
EXPOSE 5002

# Health check to ensure the service is online
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-5002}/api/status || exit 1

# Launch production WSGI server (gunicorn) respecting dynamic $PORT
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5002} --workers 2 --threads 4 --timeout 60 app:app"]
