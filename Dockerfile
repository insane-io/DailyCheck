# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install curl for health checks and uv (the modern way)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends curl \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir uv

# Copy your entire project into the container (code only; secrets are excluded via .dockerignore)
COPY . .

# Let uv install everything for the whole workspace (backend + worker)
RUN uv sync --all-packages

# Create and use a non-root user for better security in production
RUN useradd -m appuser \
	&& chown -R appuser /app

USER appuser

# We don't set a CMD here because docker-compose will handle it!