FROM python:3.12-slim

# Don't write .pyc files, and flush logs straight to the console
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first so this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run as a non-root user
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# gunicorn instead of Flask's dev server; create_app() is the app factory
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:create_app()"]