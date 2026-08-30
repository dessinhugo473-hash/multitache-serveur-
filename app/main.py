from celery.result import AsyncResult
from fastapi import FastAPI
from pydantic import BaseModel

from app.celery_app import celery_app
from app.tasks import additionner, tache_longue

app = FastAPI(title="Multitask Server")


class AdditionRequest(BaseModel):
    a: int
    b: int


@app.get("/")
def racine():
    return {"status": "ok", "message": "Serveur multitâche opérationnel"}


@app.post("/taches/longue")
def lancer_tache_longue(duree: int = 10):
    """Déclenche une tâche longue en arrière-plan et retourne son identifiant."""
    tache = tache_longue.delay(duree)
    return {"task_id": tache.id}


@app.post("/taches/addition")
def lancer_addition(payload: AdditionRequest):
    tache = additionner.delay(payload.a, payload.b)
    return {"task_id": tache.id}


@app.get("/taches/{task_id}")
def statut_tache(task_id: str):
    """Consulte l'état et le résultat d'une tâche à partir de son identifiant."""
    resultat = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "statut": resultat.status,
        "resultat": resultat.result if resultat.ready() else None,
    }
