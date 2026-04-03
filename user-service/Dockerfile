# Use a small official Python base image.
FROM python:3.12-slim

# Keep Python logs unbuffered and avoid .pyc files in container.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first to maximize Docker layer cache reuse.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app after dependencies.
COPY app.py .

# Run as non-root user for better container security.
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
