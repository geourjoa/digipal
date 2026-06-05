FROM python:2.7

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Build from repo root context so digipal modules are importable.
COPY . /app

# Minimal runtime for list_features.py.py (Django 1.x for Python 2 compatibility).
RUN pip install --no-cache-dir "Django<2"

# Default command; can be overridden at docker run.
CMD ["python", "/app/ANALYSE/tools/list_features.py"]
