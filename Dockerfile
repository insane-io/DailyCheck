# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install uv (the modern way)
RUN pip install uv

# Copy your entire project into the container
COPY . .

# Let uv install exactly what is in your lockfile
RUN uv sync

# We don't set a CMD here because docker-compose will handle it!