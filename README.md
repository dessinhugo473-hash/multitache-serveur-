# Serveur multitâche avec Docker

Architecture prête à l'emploi pour exécuter plusieurs tâches en parallèle (API web + workers en arrière-plan + tâches planifiées), basée sur **FastAPI**, **Celery** et **Redis**, orchestrée via **Docker Compose**.

## Structure du projet

```
multitask-server/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .env.example
└── app/
    ├── main.py          # API FastAPI (points d'entrée HTTP)
    ├── celery_app.py    # Configuration Celery + planification
    ├── tasks.py         # Définition des tâches asynchrones
    └── config.py        # Configuration centralisée
```

## Services Docker

| Service     | Rôle                                                        |
|-------------|--------------------------------------------------------------|
| `web`       | API FastAPI qui reçoit les requêtes et déclenche les tâches |
| `worker`    | Exécute les tâches en arrière-plan (parallélisable)          |
| `scheduler` | Déclenche les tâches périodiques (type cron)                 |
| `flower`    | Interface web de suivi des tâches (http://localhost:5555)    |
| `redis`     | Broker de messages + stockage des résultats                  |

## Démarrage

```bash
# 1. Copier le fichier d'environnement
cp .env.example .env

# 2. Construire et lancer tous les services
docker compose up --build
```

L'API est alors disponible sur `http://localhost:8000` et l'interface Flower sur `http://localhost:5555`.

## Utilisation

Lancer une tâche longue :
```bash
curl -X POST "http://localhost:8000/taches/longue?duree=5"
```

Lancer une addition :
```bash
curl -X POST http://localhost:8000/taches/addition \
  -H "Content-Type: application/json" \
  -d '{"a": 3, "b": 4}'
```

Consulter le résultat (remplacer `<task_id>` par l'identifiant retourné) :
```bash
curl http://localhost:8000/taches/<task_id>
```

## Scalabilité

Pour lancer plusieurs workers en parallèle (plus de "multitâche") :
```bash
docker compose up --build --scale worker=3
```

## Notes

- Le fichier `.env` (à créer à partir de `.env.example`) ne doit **pas** être commité (ajoutez-le à `.gitignore`).
- La planification des tâches périodiques se configure dans `app/celery_app.py` (`beat_schedule`).
- Ajoutez vos propres tâches dans `app/tasks.py`, puis exposez-les via un nouvel endpoint dans `app/main.py`.
