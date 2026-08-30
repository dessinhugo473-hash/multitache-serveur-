FROM python:3.12-slim

# Empêche Python d'écrire des .pyc et force l'affichage immédiat des logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances système minimales (build tools retirés ensuite pour alléger l'image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python (mise en cache du layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code de l'application
COPY ./app ./app

# Utilisateur non-root pour la sécurité
RUN useradd -m appuser
USER appuser

EXPOSE 8000

# Commande par défaut : lance l'API web (surchargée par docker-compose pour le worker)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
