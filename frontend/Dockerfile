# Build Stage
FROM golang:1.23-bookworm AS builder

WORKDIR /app

# Dependencies
COPY go.mod go.sum ./
RUN go mod download

# Source
COPY . .

# Build
# CGO_ENABLED=0 for static binary
RUN CGO_ENABLED=0 GOOS=linux go build -o server main.go

# Run Stage
FROM debian:bookworm-slim

WORKDIR /app

# Install CA certs for HTTPS calls to API
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy Binary and Assets
COPY --from=builder /app/server .
COPY --from=builder /app/templates ./templates
COPY --from=builder /app/assets ./assets

# Env
ENV PORT=8080
ENV GIN_MODE=release

EXPOSE 8080

CMD ["./server"]
