# --- Étape 1 : Build ---
FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Dépendances système pour Pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Étape 2 : Production ---
FROM python:3.12-slim

WORKDIR /app

# On ne copie que ce qui est nécessaire du builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Dépendances runtime pour Pillow
RUN apt-get update && apt-get install -y \
    libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Permissions pour le script d'entrée
RUN chmod +x /app/entrypoint.sh

# Port par défaut
EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
