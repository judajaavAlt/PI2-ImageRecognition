from fastapi import APIRouter, status
from pydantic import BaseModel
from services.debug import RoleManager

router = APIRouter(prefix="/roles", tags=["Role managing"])


class RoleCreate(BaseModel):
    name: str
    color: str


class Role(BaseModel):
    id: int
    name: str
    color: str


@router.post(
            "/",
            response_model=Role,
            summary="agregar un nuevo rol a la base de datos",
            status_code=status.HTTP_200_OK)
async def create_role(data: RoleCreate):
    return RoleManager.create(name=data.name, color=data.color)


@router.get(
            "/",
            response_model=list,
            summary="obtener todos los roles de la base de datos",
            status_code=status.HTTP_200_OK)
async def get_roles():
    return RoleManager.read_all()


@router.get(
            "/{id}",
            response_model=Role,
            summary="obtener un rol de la base de datos en base a su id",
            status_code=status.HTTP_200_OK)
async def get_role(id: int):
    return RoleManager.read_by_id(id)


@router.put(
            "/{id}",
            response_model=Role,
            summary="editar un rol de la base de datos en base a su id",
            status_code=status.HTTP_200_OK)
async def update_role(id: int, data: RoleCreate):
    return RoleManager.update(id, name=data.name, color=data.color)


@router.delete(
            "/{id}",
            response_model=Role,
            summary="eliminar un rol de la base de datos en base a su id",
            status_code=status.HTTP_200_OK)
async def delete_role(id: int):
    return RoleManager.delete(id)
