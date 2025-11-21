from typing import Dict, Any
from models.worker import Worker

class Database:
    """
    Mock temporal de la capa de base de datos.
    Cada método devuelve información estática solo para pruebas internas.
    """

    # Datos fake estáticos
    _WORKERS = {
        1: {
            "id": 1,
            "name": "Pepito",
            "document": "1.234.567.890",
            "role": "guardia",
            "photo": "https://example.com/foto.jpg",
        }
    }

    _ROLES = {
        1: {"id": 1, "name": "guardia"},
        2: {"id": 2, "name": "supervisor"},
    }

    # ------------------------------------------------------------
    # WORKERS
    # ------------------------------------------------------------
    @classmethod
    def createWorker(cls, worker: Worker) -> Dict[str, Any]:
        """
        Mock: Crea un trabajador (respuesta estática).
        """
        return {
            "status": "ok",
            "message": "Mock: Worker creado",
            "data": worker.model_dump()
        }

    @classmethod
    def updateWorker(cls, worker: Worker) -> Dict[str, Any]:
        """
        Mock: Actualiza un trabajador (respuesta estática).
        """
        return {
            "status": "ok",
            "message": "Mock: Worker actualizado",
            "data": worker.model_dump()
        }

    @classmethod
    def DeleteWorker(cls, worker: Worker) -> Dict[str, Any]:
        """
        Mock: Elimina un trabajador (respuesta estática).
        """
        return {
            "status": "ok",
            "message": "Mock: Worker eliminado",
            "worker_id": worker.id
        }

    @classmethod
    def getWorker(cls, worker: Worker) -> Dict[str, Any]:
        """
        Mock: Obtiene un trabajador por ID (respuesta estática).
        """
        return {
            "status": "ok",
            "data": cls._WORKERS.get(worker.id, None)
        }

    @classmethod
    def getWorkerList(cls) -> Dict[str, Any]:
        """
        Mock: Retorna lista de trabajadores.
        """
        return {
            "status": "ok",
            "count": len(cls._WORKERS),
            "data": list(cls._WORKERS.values())
        }

    @classmethod
    def getWorkerByCC(cls) -> Dict[str, Any]:
        """
        Mock: Busca por documento estático.
        """
        return {
            "status": "ok",
            "data": cls._WORKERS.get(1)  # siempre retorna Pepito
        }

