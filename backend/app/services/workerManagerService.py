from typing import Dict, Any
from models.worker import Worker
from db.database import Database


class WorkerManagerService:

    # ------------------------------
    # LISTAR TRABAJADORES
    # ------------------------------
    @staticmethod
    async def fetch_workers() -> Dict[str, Any]:
        result = Database.get_worker_list()

        return {
            "data": result.data or [],
            "count": result.count or 0
        }

    # ------------------------------
    # OBTENER TRABAJADOR POR ID
    # ------------------------------
    @staticmethod
    async def get_worker(worker_id: int) -> Any:
        result = Database.get_worker(worker_id)

        if not result.data:
            return None

        return result.data[0]

    # ------------------------------
    # CREAR TRABAJADOR
    # ------------------------------
    @staticmethod
    async def create_worker(worker_data: Dict[str, Any]) -> Any:
        worker = Worker(**worker_data)

        # Convertir HttpUrl → str
        payload = worker.model_dump()
        if "photo" in payload:
            payload["photo"] = str(payload["photo"])

        result = Database.create_worker(payload)

        return result.data[0] if result.data else None

    # ------------------------------
    # ACTUALIZAR TRABAJADOR
    # ------------------------------
    @staticmethod
    async def update_worker(worker_id: int, worker_data: Dict[str, Any]) -> Any:
        worker_data["id"] = worker_id
        worker = Worker(**worker_data)

        payload = worker.model_dump()
        if "photo" in payload:
            payload["photo"] = str(payload["photo"])

        result = Database.update_worker(worker_id, payload)

        return result.data[0] if result.data else None

    # ------------------------------
    # ELIMINAR TRABAJADOR
    # ------------------------------
    @staticmethod
    async def delete_worker(worker_id: int) -> Any:
        result = Database.delete_worker(worker_id)

        return result.data[0] if result.data else None
