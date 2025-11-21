from typing import Dict, Any
from db.database import Database
from app.models.worker import Worker


class WorkerManagerService:
    """
    Servicio que delega TODAS las operaciones CRUD al módulo Database.
    Solo valida tipos con Pydantic. No verifica existencia ni hace reglas de negocio.
    """

    # ------------------------------
    # LISTAR TRABAJADORES
    # ------------------------------
    @staticmethod
    async def fetch_workers() -> Any:
        result = Database.getWorkerList()
        return result.get("data")

    # ------------------------------
    # OBTENER TRABAJADOR POR ID
    # ------------------------------
    @staticmethod
    async def get_worker(worker_id: int) -> Any:
        result = Database.getWorker(worker_id)
        return result.get("data")

    # ------------------------------
    # CREAR TRABAJADOR
    # ------------------------------
    @staticmethod
    async def create_worker(worker_data: Dict[str, Any]) -> Any:
        # Validación de tipos mediante Pydantic
        worker = Worker(**worker_data)

        result = Database.createWorker(worker)
        return result.get("data")

    # ------------------------------
    # ACTUALIZAR TRABAJADOR
    # ------------------------------
    @staticmethod
    async def update_worker(worker_id: int, worker_data: Dict[str, Any]) -> Any:
        # Update debe recibir el Worker COMPLETO desde el front
        worker_data["id"] = worker_id
        worker = Worker(**worker_data)

        result = Database.updateWorker(worker)
        return result.get("data")

    # ------------------------------
    # ELIMINAR TRABAJADOR
    # ------------------------------
    @staticmethod
    async def delete_worker(worker_id: int) -> Any:
        result = Database.deleteWorker(worker_id)
        return result.get("data")
