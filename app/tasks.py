import time

from app.celery_app import celery_app


@celery_app.task(name="app.tasks.tache_longue")
def tache_longue(duree: int = 10) -> str:
    """Exemple de tâche longue exécutée en arrière-plan par un worker."""
    time.sleep(duree)
    return f"Tâche terminée après {duree} secondes"


@celery_app.task(name="app.tasks.additionner", bind=True, max_retries=3)
def additionner(self, a: int, b: int) -> int:
    """Exemple de tâche simple avec gestion de reprise en cas d'échec."""
    try:
        return a + b
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)


@celery_app.task(name="app.tasks.tache_planifiee_exemple")
def tache_planifiee_exemple() -> str:
    """Exemple de tâche exécutée automatiquement par le scheduler (celery beat)."""
    return "Nettoyage effectué"
