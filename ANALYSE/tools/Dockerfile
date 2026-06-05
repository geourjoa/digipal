# Laucnhed from root folder

# docker build -f ANALYSE/tools/Dockerfile . -t digipal-list-features:test
# docker run --rm digipal-list-features:test

FROM python:2.7



ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Build from repo root context so digipal modules are importable.
# Example: docker build -f ANALYSE/tools/Dockerfile .
COPY . /app

RUN pip install -r ANALYSE/tools/requirements.txt

# Fail fast if the image was built with the wrong context.
RUN test -f /app/ANALYSE/tools/list_features.py || \
    (echo "ERROR: build context must be repository root (.)" && exit 1)

# Default command; can be overridden at docker run.
CMD ["python", "/app/ANALYSE/tools/list_features.py"]
