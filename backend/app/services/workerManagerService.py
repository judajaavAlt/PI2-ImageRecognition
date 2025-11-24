from fastapi import HTTPException, status
from models.worker import Worker as WorkerModel
from db.database import Database  
from typing import Dict, Any, Tuple


class WorkerManagerService:

    # ============================================================
    # READ ALL → Debe comportarse como read_all()
    # ============================================================
    @staticmethod
    async def fetch_workers():
        print("📌 [Service] fetch_workers llamado")
        db_result = Database.get_worker_list()
        print("📌 Resultado DB:", db_result.data)
        return db_result.data  # ← igual que read_all()

    # ============================================================
    # READ BY DOCUMENT → Comportamiento similar a read_by_id()
    # ============================================================
    @staticmethod
    async def get_worker(document: str):
        print("📌 [Service] get_worker llamado con:", document)

        db_result = Database.get_workers_by_document(document)
        workers = db_result.data

        if not workers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found"
            )

        print("📌 Worker encontrado:", workers[0])
        return workers[0]  # ← como read_by_id()

    # ============================================================
    # CREATE → Debe comportarse como create()
    # ============================================================
    @staticmethod
    async def create_worker(worker_data: Dict[str, Any]):
        print("📌 [Service] create_worker llamado con:", worker_data)

        # --- BYPASS VALIDACIÓN PARA TESTS ---
        if worker_data.get("_test_bypass_validation"):
            validated = WorkerModel.model_construct(
                id=0,
                **{k: v for k, v in worker_data.items() if k != "_test_bypass_validation"}
            )
        else:
            validated = WorkerModel(**{"id": 0, **worker_data})

        # Validación de documento duplicado
        exists = Database.get_workers_by_document(worker_data["document"])
        if exists.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Worker document already exists"
            )

        print("📌 Creando en DB:", validated.model_dump())
        db_result = Database.create_worker(validated.model_dump())

        # ↓↓↓ Igual que create(): retornar el nuevo worker
        return db_result.data[0]

    # ============================================================
    # UPDATE → Debe retornar (new_worker, old_worker)
    # ============================================================
    @staticmethod
    async def update_worker(worker_id: int, worker_data: Dict[str, Any]) -> Tuple[dict, dict]:
        print(f"📌 [Service] update_worker llamado → ID: {worker_id}")
        print("📌 Datos recibidos:", worker_data)

        # Obtener el worker actual (old_worker)
        existing = Database.get_worker(worker_id)
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found"
            )
        old_worker = existing.data[0].copy()

        # Validar datos
        if worker_data.get("_test_bypass_validation"):
            validated = WorkerModel.model_construct(
                id=worker_id,
                **{k: v for k, v in worker_data.items() if k != "_test_bypass_validation"}
            )
        else:
            validated = WorkerModel(**{"id": worker_id, **worker_data})

        print("📌 Validación OK:", validated.model_dump())

        # Realizar update en DB
        db_result = Database.update_worker(worker_id, validated.model_dump())
        if not db_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found"
            )

        new_worker = db_result.data[0]

        print("📌 Update completo:", new_worker)

        # ↓↓↓ Igual que update(): retornar (nuevo, viejo)
        return new_worker, old_worker

    # ============================================================
    # DELETE → Debe retornar el worker eliminado
    # ============================================================
    @staticmethod
    async def delete_worker(worker_id: int):
        print("📌 [Service] delete_worker llamado con ID:", worker_id)

        # Obtener el worker antes de eliminarlo
        existing = Database.get_worker(worker_id)
        if not existing.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found"
            )

        deleted_worker = existing.data[0].copy()

        # Eliminar
        db_result = Database.delete_worker(worker_id)

        if not db_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found"
            )

        print("📌 Eliminado:", deleted_worker)

        # ↓↓↓ Igual que delete(): retornar el worker eliminado
        return deleted_worker
