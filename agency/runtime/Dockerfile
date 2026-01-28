# Sprite Runtime Container
# Lightweight Python container for running agent sprites on Fly.io

FROM python:3.12-slim

# Create non-root user for security
RUN useradd -m -u 1000 sprite

# Set working directory
WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy runtime code
COPY *.py .

# Copy agent personas (mounted from parent directory during build)
COPY agents/ /app/agents/

# Switch to non-root user
USER sprite

# Environment defaults
ENV PYTHONUNBUFFERED=1
ENV IDLE_TIMEOUT=300
ENV HEARTBEAT_INTERVAL=30

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('/tmp/sprite_healthy') else 1)"

# Run the sprite
CMD ["python", "sprite.py"]
