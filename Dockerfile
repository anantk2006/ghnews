# Build stage for React app
FROM node:18-alpine as build

WORKDIR /app/virsitile
COPY virsitile/package*.json ./
RUN npm install

COPY virsitile/ ./
RUN npm run build

# Production stage
FROM python:3.11-slim

# Install Node.js and npm
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install pm2 -g \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy frontend build from build stage
COPY --from=build /app/virsitile/build /app/virsitile/build

# Install Python dependencies
RUN pip install fastapi gunicorn requests datetime sqlite3

# Copy backend code
COPY backend/ ./backend/

# Copy PM2 config
COPY ecosystem.config.js .

# Expose ports for both services
EXPOSE 80 8000

# Start both services using PM2
CMD ["pm2-runtime", "start", "ecosystem.config.js"]
