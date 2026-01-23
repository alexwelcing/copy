# Marketing Agency Frontend
# Multi-stage build for SvelteKit

# Build stage
FROM node:20-slim AS builder

WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install

# Copy source and build
COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Production stage
FROM node:20-slim

WORKDIR /app

# Copy built application
COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Environment
ENV NODE_ENV=production
ENV PORT=3000
ENV ORIGIN=http://localhost:3000

EXPOSE 3000

# Run the Node.js server
CMD ["sh", "-c", "export ORIGIN=${RENDER_EXTERNAL_URL:-$ORIGIN} && node build"]
