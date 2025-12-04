FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy uv binary directly from the UV container image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies using uv sync (runs during build time)
RUN uv sync --frozen --no-dev

# Copy the rest of the application
COPY . /app

# Create the nonroot user and set permissions
RUN adduser --disabled-password --gecos "" nonroot && \
    chown -R nonroot:nonroot /app && \
    chmod -R 755 /app

# Switch to non-root user
USER nonroot

# Run gunicorn using the installed virtual environment
# Note: --no-sync skips dependency installation since we already did it during build
CMD ["uv", "run", "--no-sync", "--", "gunicorn", "-b", "0.0.0.0:8080", "--workers=10", "--preload", "app:server"]
