from pydantic import BaseModel, Field, field_validator

class Role(BaseModel):
    id: int | None = None
    
    name: str = Field(..., min_length=2, max_length=50)

    # Regex permite 3 o 6 caracteres
    color: str = Field(..., pattern=r"^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$")

    @field_validator("color")
    @classmethod
    def standard_color_format(cls, v: str):
        """
        1. Convierte a mayúsculas.
        2. Si viene en formato corto (#F00), lo expande a largo (#FF0000).
        """
        v = v.upper()
        
        # Si tiene 4 caracteres (ej: #FFF), duplicamos cada carácter
        if len(v) == 4:
            # v[0] es '#', v[1] es 'F', etc.
            return f"#{v[1]*2}{v[2]*2}{v[3]*2}"
            
        return v

    @field_validator("name")
    @classmethod
    def title_case_name(cls, v: str):
        return v.strip().title()