# Build Stage
FROM golang:1.24-bookworm AS builder

WORKDIR /app

# Dependencies
COPY frontend/go.mod frontend/go.sum ./
RUN go mod download

# Source
COPY frontend/ ./

# Build
# CGO_ENABLED=0 for static binary
RUN CGO_ENABLED=0 GOOS=linux go build -o server main.go

# Data files
WORKDIR /data
COPY campaign_data.json campaign_visuals.json campaign_visuals_updated.json ./
COPY law_campaign_data.json law_campaign_visuals.json ./

# Run Stage
FROM debian:bookworm-slim

WORKDIR /app

# Install CA certs for HTTPS calls to API
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy Binary, Assets, and Data Files
COPY --from=builder /app/server .
COPY --from=builder /app/templates ./templates
COPY --from=builder /app/assets ./assets
COPY --from=builder /data ./data

# Env
ENV PORT=8080
ENV GIN_MODE=release

EXPOSE 8080

CMD ["./server"]
