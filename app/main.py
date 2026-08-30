from pathlib import Path

from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.celery_app import celery_app
from app.tasks import additionner, tache_longue

app = FastAPI(title="Multitask Server")

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class AdditionRequest(BaseModel):
    a: int
    b: int


@app.get("/")
def racine():
    """Sert le tableau de bord web si présent, sinon un statut JSON simple."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"status": "ok", "message": "Serveur multitâche opérationnel"}


@app.get("/api")
def statut_api():
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
