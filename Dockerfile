FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy uv binary directly from the UV container image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Create the nonroot user and set ownership of the working directory
RUN adduser --disabled-password --gecos "" nonroot && \
    chown nonroot:nonroot /app

# Copy dependency files first for better layer caching
COPY --chown=nonroot:nonroot pyproject.toml uv.lock ./

# Switch to non-root user before installing dependencies
USER nonroot

# Install dependencies using uv sync (runs during build time)
# --frozen: Use exact versions from uv.lock for reproducible builds
# --no-dev: Skip dev dependencies since this is a production image
RUN uv sync --frozen --no-dev

# Copy the rest of the application and set ownership
COPY --chown=nonroot:nonroot . /app

# Run gunicorn using the installed virtual environment
# Note: --no-sync skips dependency installation since we already did it during build
CMD ["uv", "run", "--no-sync", "--", "gunicorn", "-b", "0.0.0.0:8080", "--workers=10", "--preload", "app:server"]
