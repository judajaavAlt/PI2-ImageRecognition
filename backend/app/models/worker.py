from pydantic import BaseModel, Field, HttpUrl, field_validator

class Worker(BaseModel):
    id: int | None = None
    name: str = Field(..., min_length=2, max_length=100)

    # ESTE es el correcto para Pydantic v2:
    document: str = Field(..., pattern=r"^\d{1,3}(\.\d{3}){3}$")

    role: str = Field(..., min_length=3, max_length=50)
    photo: HttpUrl | None = None

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str):
        allowed_roles = {"guardia", "supervisor", "operario", "administrador"}
        if value.lower() not in allowed_roles:
            raise ValueError(f"El rol '{value}' no es válido. Roles permitidos: {', '.join(allowed_roles)}")
        return value.lower()
