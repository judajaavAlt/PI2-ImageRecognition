from fastapi import APIRouter, status
from pydantic import BaseModel
import os

router = APIRouter(prefix="/admin", tags=["Admin"])


class Credentials(BaseModel):
    username: str
    password: str


@router.post(
        "/validate-credentials",
        response_model=bool,
        status_code=status.HTTP_200_OK)
async def validate_credentials(creds: Credentials) -> bool:
    """
    Recibe JSON { "username": "...", "password": "..." } y retorna True si
    coinciden exactamente con las variables de
    ambiente ADMIN_USER y ADMIN_PASSWORD.
    """
    admin_user = os.getenv("ADMIN_USER", "")
    admin_password = os.getenv("ADMIN_PASSWORD", "")

    is_valid = (
        creds.username == admin_user) and (creds.password == admin_password)
    return is_valid
