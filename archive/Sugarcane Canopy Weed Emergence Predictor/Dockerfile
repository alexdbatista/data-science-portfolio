# -------------------------------------------------------------------
# Sugarcane Weed Emergence Predictor — Multi-stage Docker Build
# -------------------------------------------------------------------
# Stage 1: dependency builder (keeps final image lean)
FROM python:3.11-slim AS builder

WORKDIR /install
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/install/deps --no-cache-dir -r requirements.txt


# -------------------------------------------------------------------
# Stage 2: runtime image
# -------------------------------------------------------------------
FROM python:3.11-slim AS runtime

LABEL maintainer="alexdbatista"
LABEL project="sugarcane-weed-emergence-predictor"
LABEL version="1.0.0"

# Copy installed packages from builder
COPY --from=builder /install/deps /usr/local

# Application code
WORKDIR /app
COPY . .

# Create runtime directories
RUN mkdir -p /app/data /app/models /app/reports

# Non-root user for security best practice
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose REST API port
EXPOSE 8000

# Health check for container orchestrator (Kubernetes / ECS)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Default entrypoint — production-grade Uvicorn
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "2", \
     "--log-level", "info"]
