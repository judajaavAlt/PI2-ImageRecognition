from pydantic import BaseModel, Field, HttpUrl, field_validator


class Worker(BaseModel):
    id: int | None = None
    name: str = Field(..., min_length=2, max_length=100)

    # Documento con formato 1.234.567.890
    document: str = Field(..., pattern=r"^\d{1,3}(\.\d{3}){3}$")

    # IMPORTANTE → rol debe ser un ID numérico
    role: int = Field(..., ge=1)

    photo: HttpUrl | None = None

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: int):
        if value <= 0:
            raise ValueError("El ID de rol debe ser mayor a 0")
        return value
