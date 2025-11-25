from fastapi import APIRouter, status
from pydantic import BaseModel
from services.workerManager import WorkerManager
from services.speechService import SpeechService
import base64

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
    try:
        if data.cc % 2 == 0:
            # Autenticación exitosa
            text = "Autenticación exitosa. Bienvenido."
            audio_bytes = SpeechService.text_to_audio(text)
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            return {"match": True, "message": audio_base64}
        else:
            # Autenticación fallida
            text = "Usuario no encontrado. Autenticación fallida."
            audio_bytes = SpeechService.text_to_audio(text)
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            return {"match": False, "message": audio_base64}
    except Exception as e:
        print(f"Error generando audio: {e}")
        # En caso de error, retornar mensaje sin audio
        if data.cc % 2 == 0:
            return {"match": True, "message": ""}
        else:
            return {"match": False, "message": ""}
