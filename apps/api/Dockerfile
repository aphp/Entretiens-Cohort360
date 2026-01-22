# Django API Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv sync

# Copy application code
COPY . .

# Run migrations and start server
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
