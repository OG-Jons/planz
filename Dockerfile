# syntax=docker/dockerfile:1.4

# Stage 1: Frontend build
FROM node:22-alpine AS frontend-build

WORKDIR /frontend

# Copy only package files to install dependencies first (for better caching)
COPY frontend/package*.json ./

RUN npm ci

# Copy the rest of the frontend code and build it
COPY frontend/ ./
RUN chmod +x node_modules/.bin/* && npm run build

# Stage 2: Backend with FastAPI
FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.4.15 /uv /bin/uv

# Copy project files
COPY backend/pyproject.toml backend/uv.lock ./
COPY backend/app ./app

RUN mkdir ./media

# Copy frontend build output into the backend
COPY --from=frontend-build /frontend/dist /frontend/dist

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Optional: Sync project if needed (e.g., if app-level dependencies not included above)
# RUN --mount=type=cache,target=/root/.cache/uv \
#     uv sync

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]