FROM python:3.12-slim

WORKDIR /app

# Installer dépendances système pour OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip et installer setuptools et wheel
RUN pip install --upgrade pip setuptools wheel

# Copier requirements et installer packages Python
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=900 -r requirements.txt

# Copier le projet
COPY . .

# Créer dossier pour uploads
RUN mkdir -p uploads

# Exposer port FastAPI
EXPOSE 8000

# Lancer FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

