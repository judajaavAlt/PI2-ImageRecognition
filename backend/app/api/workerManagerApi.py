import time
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services.workerManagerService import WorkerManagerService

router = APIRouter()

@router.get("/workers", tags=["Workers"])
async def get_all_workers():
    """
    Devuelve la lista completa de trabajadores registrados en el sistema.
    """
    try:
        data = await WorkerManagerService.fetch_workers()
        response = {
            "status": "ok",
            "count": len(data.get("data", [])),
            "data": data.get("data", []),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workers/{worker_id}", tags=["Workers"])
async def get_worker_by_id(worker_id: int):
    """
    Obtiene la información de un trabajador específico por su ID.
    """
    try:
        worker = await WorkerManagerService.get_worker(worker_id)
        if not worker:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado")
        return {
            "status": "ok",
            "data": worker,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workers", tags=["Workers"])
async def create_worker(worker: dict):
    """
    Registra un nuevo trabajador en el sistema.
    """
    try:
        result = await WorkerManagerService.create_worker(worker)
        response = {
            "status": "ok",
            "message": "Trabajador creado exitosamente",
            "data": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return JSONResponse(content=response, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/workers/{worker_id}", tags=["Workers"])
async def update_worker(worker_id: int, worker: dict):
    """
    Actualiza la información de un trabajador existente.
    """
    try:
        result = await WorkerManagerService.update_worker(worker_id, worker)
        response = {
            "status": "ok",
            "message": "Trabajador actualizado exitosamente",
            "data": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return JSONResponse(content=response, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/workers/{worker_id}", tags=["Workers"])
async def delete_worker(worker_id: int):
    """
    Elimina un trabajador del sistema por su ID.
    """
    try:
        result = await WorkerManagerService.delete_worker(worker_id)
        response = {
            "status": "ok",
            "message": "Trabajador eliminado exitosamente",
            "data": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return JSONResponse(content=response, status_code=200)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
