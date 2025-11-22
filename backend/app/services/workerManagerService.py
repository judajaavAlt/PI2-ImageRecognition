from typing import Dict, Any
from models.worker import Worker
from services.debug import WorkerManager


class WorkerManagerService:
    """
    Servicio intermedio entre FastAPI y WorkerManager.
    Valida datos con Pydantic y normaliza la comunicación.
    """

    # ============================================================
    # LISTAR TRABAJADORES
    # ============================================================
    @staticmethod
    async def fetch_workers():
        """
        Normaliza la salida de WorkerManager.read_all()
        para que siempre sea un diccionario con data, count.
        """
        workers = WorkerManager.read_all()

        return {
            "data": workers,
            "count": len(workers)
        }

    # ============================================================
    # OBTENER TRABAJADOR POR ID
    # ============================================================
    @staticmethod
    async def get_worker(worker_id: int):
        worker = WorkerManager.read_by_id(worker_id)
        return worker

    # ============================================================
    # CREAR TRABAJADOR
    # ============================================================
    @staticmethod
    async def create_worker(worker_data: Dict[str, Any]):
        """
        Valida con Pydantic y crea el worker.
        """
        worker = Worker(**worker_data)

        created = WorkerManager.create(
            name=worker.name,
            document=worker.document,
            role=worker.role,
            photo=str(worker.photo) if worker.photo else None
        )
        return created

    # ============================================================
    # ACTUALIZAR TRABAJADOR
    # ============================================================
    @staticmethod
    async def update_worker(worker_id: int, worker_data: Dict[str, Any]):
        worker_data["id"] = worker_id

        worker = Worker(**worker_data)

        updated, _old = WorkerManager.update(
            worker_id,
            name=worker.name,
            document=worker.document,
            role=worker.role,
            photo=str(worker.photo) if worker.photo else None
        )

        return updated  # <--- solo el worker actualizado

    # ============================================================
    # ELIMINAR TRABAJADOR
    # ============================================================
    @staticmethod
    async def delete_worker(worker_id: int):
        deleted = WorkerManager.delete(worker_id)
        return deleted
