# backend/app/models/worker.py
from pydantic import BaseModel, Field, HttpUrl, validator

class Worker(BaseModel):
    id: int | None = None
    name: str = Field(..., min_length=2, max_length=100)
    document: str = Field(..., regex=r"^\d{1,3}(\.\d{3}){2}\.\d{1,3}$")  # formato: 1.234.567.890
    role: str = Field(..., min_length=3, max_length=50)
    photo: HttpUrl | None = None

    @validator("role")
    def validate_role(cls, value):
        allowed_roles = {"guardia", "supervisor", "operario", "administrador"}
        if value.lower() not in allowed_roles:
            raise ValueError(f"El rol '{value}' no es válido.")
        return value.lower()
