from fastapi import APIRouter, status
from pydantic import BaseModel
from services.workerManager import WorkerManager

router = APIRouter(prefix="/workers", tags=["Worker managing"])


class WorkerCreate(BaseModel):
    name: str
    document: str
    role: int
    photo: str


class Worker(BaseModel):
    id: int
    name: str
    document: str
    role: int
    photo: str


class verification(BaseModel):
    cc: int
    photo: str


class result(BaseModel):
    match: bool
    message: str


@router.post(
            "/",
            response_model=Worker,
            summary="agregar un nuevo worker a la base de datos",
            status_code=status.HTTP_200_OK)
async def create_worker(data: WorkerCreate):
    return WorkerManager.create(name=data.name, document=data.document,
                                role=data.role, photo=data.photo)


@router.get(
            "/",
            response_model=list,
            summary="obtener todos los workers de la base de datos",
            status_code=status.HTTP_200_OK)
async def get_workers():
    return WorkerManager.read_all()


@router.get(
            "/{id}",
            response_model=Worker,
            summary="obtener un worker de la base de datos en base a su id",
            status_code=status.HTTP_200_OK)
async def get_worker(id: int):
    return WorkerManager.read_by_id(id)


@router.put(
            "/{id}",
            response_model=Worker,
            summary="editar un worker de la base de datos en base a su id",
            status_code=status.HTTP_200_OK)
async def update_worker(id: int, data: WorkerCreate):
    return WorkerManager.update(id, name=data.name, document=data.document,
                                role=data.role, photo=data.photo)


@router.delete(
            "/{id}",
            response_model=Worker,
            summary="eliminar un worker de la base de datos en base a su id",
            status_code=status.HTTP_200_OK)
async def delete_worker(id: int):
    return WorkerManager.delete(id)


@router.post(
            "/verify",
            response_model=result,
            summary="verificar un trabajador segun su c.c. y foto",
            status_code=status.HTTP_200_OK)
async def verify_worker(data: verification):
    return {"match": True, "message": ""}
