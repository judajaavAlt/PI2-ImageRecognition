from typing import Dict, Any
from app.models.worker import Worker


class Database:
    """
    Mock temporal que imita el comportamiento del futuro módulo Supabase.
    Siempre retorna diccionarios con llaves: data, count.
    """

    _WORKERS = {
        1: {
            "id": 1,
            "name": "Pepito",
            "document": "1.234.567.890",
            "role": "guardia",
            "photo": "https://example.com/foto.jpg",
        }
    }

    _next_id = 2

    # ------------------------------------------------------------
    # LISTAR
    # ------------------------------------------------------------
    @classmethod
    def getWorkerList(cls) -> Dict[str, Any]:
        data = list(cls._WORKERS.values())
        return {"data": data, "count": len(data)}

    # ------------------------------------------------------------
    # OBTENER POR ID
    # ------------------------------------------------------------
    @classmethod
    def getWorker(cls, worker_id: int) -> Dict[str, Any]:
        worker = cls._WORKERS.get(worker_id)
        return {"data": worker, "count": 1 if worker else 0}

    # ------------------------------------------------------------
    # CREAR
    # ------------------------------------------------------------
    @classmethod
    def createWorker(cls, worker: Worker) -> Dict[str, Any]:
        worker_dict = worker.model_dump(mode="json")
        worker_dict["id"] = cls._next_id

        cls._WORKERS[cls._next_id] = worker_dict
        cls._next_id += 1

        return {"data": worker_dict, "count": None}

    # ------------------------------------------------------------
    # ACTUALIZAR
    # ------------------------------------------------------------
    @classmethod
    def updateWorker(cls, worker: Worker) -> Dict[str, Any]:
        worker_dict = worker.model_dump(mode="json")

        if worker.id in cls._WORKERS:
            cls._WORKERS[worker.id].update(worker_dict)

        return {"data": cls._WORKERS.get(worker.id), "count": None}

    # ------------------------------------------------------------
    # ELIMINAR
    # ------------------------------------------------------------
    @classmethod
    def deleteWorker(cls, worker_id: int) -> Dict[str, Any]:
        deleted = cls._WORKERS.pop(worker_id, None)
        return {"data": deleted, "count": None}
