# Marketing Agency API Service
# Optimized for Google Cloud Run

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy skills (these are the core content)
COPY skills/ ./skills/

# Copy service code
COPY service/ ./service/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Cloud Run sets PORT environment variable
ENV PORT=8080

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8080/health')" || exit 1

# Run the service with Gunicorn for production reliability
# -k uvicorn.workers.UvicornWorker: Use Uvicorn for async
# --timeout 300: Allow 5 minutes for LLM generation (critical for reliability)
# --workers 1: Single worker for container environment (prevents OOM)
CMD ["gunicorn", "service.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080", "--timeout", "300"]
