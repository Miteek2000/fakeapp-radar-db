FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    PIP_RETRIES=10

# Parches de seguridad del sistema (p. ej. zlib) y herramientas de empaquetado al día (Trivy fase 11).
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip setuptools wheel

RUN useradd --create-home --uid 1000 app
WORKDIR /migrator

COPY migrator/requirements.txt .
RUN pip install -r requirements.txt

COPY migrator/alembic.ini migrator/seed.py ./
COPY migrator/migrations ./migrations
COPY seeds ./seeds

USER app
# 1) crea/actualiza las tablas  2) carga el catálogo inicial (se puede repetir sin duplicar)
CMD ["sh", "-c", "alembic upgrade head && python seed.py"]
