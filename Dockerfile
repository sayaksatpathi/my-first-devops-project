FROM python:3.12-slim

# Don't write .pyc files; flush stdout/stderr immediately (better container logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install dependencies first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Run as a non-root user
RUN useradd --create-home appuser
USER appuser

EXPOSE 8080

# Use gunicorn in production-like runs; fall back to Flask's server is avoided.
# Here we keep it simple with Flask's built-in server for a first project.
CMD ["python", "app.py"]
