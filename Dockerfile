
FROM python:3.13-bookworm
# FROM python:3.12-bookworm

WORKDIR /app

# Variables recomendadas por Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Instalar dependencias del sistema (GEOS, PROJ, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libproj-dev proj-bin proj-data \
        libgeos-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias
# RUN pip install --no-cache-dir -r requirements-docker.txt
RUN pip install --no-cache-dir -r requirements.txt


# (Opcional pero recomendado) Instalar dependencias necesarias de Playwright
RUN pip install playwright==1.55.0 && \
    playwright install --with-deps

# Copiar el proyecto completo
COPY . .

# Exponer puerto
EXPOSE 8010

# Ejecutar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]