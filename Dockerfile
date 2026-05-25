# ============================================================
# Multi-stage build for optimized production image
# ============================================================

# Stage 1: Builder
FROM python:3.11-slim as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libsndfile1-dev \
    libsox-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

# ============================================================
# Stage 2: Runtime
# ============================================================

FROM python:3.11-slim

LABEL maintainer="AI Karaoke Music Studio"
LABEL description="Production-ready AI Karaoke Music Studio with stem separation"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    PATH="/venv/bin:$PATH"

# Install runtime dependencies only (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    sox \
    ffmpeg \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app /app/uploads /app/projects && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copy wheels from builder stage
COPY --from=builder /build/wheels /wheels

# Install Python dependencies from wheels
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache /wheels/* && \
    rm -rf /wheels

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port (7860 for HF Spaces, 5000 for local development)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Run with gunicorn (production WSGI server)
# For HF Spaces: 2 workers, reduced connections due to shared resources
CMD ["gunicorn", \
     "--workers", "2", \
     "--worker-class", "sync", \
     "--worker-connections", "500", \
     "--bind", "0.0.0.0:7860", \
     "--timeout", "120", \
     "--graceful-timeout", "30", \
     "--keep-alive", "5", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "app:app"]
