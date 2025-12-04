FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Switch to root user to install dependencies
USER root

# Create the nonroot user and set permissions
RUN adduser --disabled-password --gecos "" nonroot && chown -R nonroot /app

# Copy everything into the working directory
COPY . /app

# Copy uv binary directly from the UV container image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set ownership and permissions in a single step
RUN chown -R nonroot:nonroot /app && chmod -R 755 /app

# Switch back to non-root user
USER nonroot

# Use uv run to lock, sync, then invoke Gunicorn
#    Note the “--” to separate uv flags from the Gunicorn command
CMD ["uv", "run", "--", "gunicorn", "-b", "0.0.0.0:8080", "-k", "gevent", "--workers=10", "--preload", "app:server"]