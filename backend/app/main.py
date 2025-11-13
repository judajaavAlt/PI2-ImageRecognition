from app.core.CORS import setup_cors
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
from app.api import monitoringApi, adminApi

# ------------------------------------------------------------------------------
# Application Metadata
# ------------------------------------------------------------------------------

app = FastAPI(
    title="Worker Management API",
    description=(
        "API principal del sistema de gestión de trabajadores. "
        "Provee endpoints para reconocimiento de entrada, salida y uniformes, "
        "así como utilidades de monitoreo y diagnóstico."
    ),
    version="1.0.0",
    contact={
        "name": "Worker Management Team",
        "url": "https://github.com/your-org/worker-management-app",
        "email": "support@yourorg.com",
    },
)

setup_cors(app)

# ------------------------------------------------------------------------------
# Basic API Endpoints
# ------------------------------------------------------------------------------


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz — retorna un mensaje de bienvenida.
    """
    return {"message": "Welcome to the Worker Management API 🚀"}

app.include_router(monitoringApi.router)
app.include_router(adminApi.router)


# ------------------------------------------------------------------------------
# Error Handlers
# ------------------------------------------------------------------------------

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Manejo genérico de errores no controlados.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "path": str(request.url),
        },
    )

# ------------------------------------------------------------------------------
# Run command (for local debug)
# ------------------------------------------------------------------------------
# Se puede ejecutar localmente con:
#   cd backend/app
#   python -m main
# Aunque en Docker se usa: uvicorn app.main:app --host 0.0.0.0 --port 8000
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )
