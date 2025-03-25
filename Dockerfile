# Use the official uv image as a base image
FROM ghcr.io/astral-sh/uv:python3.10-alpine

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv
RUN uv sync --frozen

# Copy remaining project files
COPY . .

# Expose port
EXPOSE 8000

# Set health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Command to run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 