from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import socket
import time

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

# ------------------------------------------------------------------------------
# CORS Configuration
# ------------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se recomienda limitar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Mock service health checks
# ------------------------------------------------------------------------------

def check_database() -> bool:
    """
    Verifica la conexión al servicio de base de datos.
    En producción, esto debería intentar una conexión real (por ejemplo, con SQLAlchemy).
    """
    try:
        # Aquí podrías colocar algo como: session.execute("SELECT 1")
        return True
    except Exception:
        return False


def check_recognition_service() -> bool:
    """
    Verifica si el servicio de reconocimiento (por ejemplo, un microservicio de visión)
    está accesible.
    """
    try:
        # Ejemplo: ping a un servicio externo o interno
        return True
    except Exception:
        return False

# ------------------------------------------------------------------------------
# Basic API Endpoints
# ------------------------------------------------------------------------------

@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz — retorna un mensaje de bienvenida.
    """
    return {"message": "Welcome to the Worker Management API 🚀"}


@app.get("/health", tags=["Monitoring"])
async def health_check():
    """
    Verifica si la API principal está viva.
    Devuelve un estado HTTP 200 si está operativa.
    """
    return {"status": "ok", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}


@app.get("/info", tags=["Monitoring"])
async def system_info():
    """
    Devuelve información básica del servicio y del entorno de ejecución.
    """
    info = {
        "service": "worker-management-backend",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "hostname": socket.gethostname(),
        "python_version": os.sys.version.split()[0],
        "uptime_check": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return info


@app.get("/services/health", tags=["Monitoring"])
async def services_health_check():
    """
    Verifica el estado de los servicios asociados al backend:
    - Base de datos
    - Servicio de reconocimiento
    """
    db_status = check_database()
    rec_status = check_recognition_service()

    all_ok = db_status and rec_status

    response = {
        "database": "ok" if db_status else "down",
        "recognition_service": "ok" if rec_status else "down",
        "overall_status": "ok" if all_ok else "degraded",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    status_code = 200 if all_ok else 503
    return JSONResponse(content=response, status_code=status_code)


@app.get("/status", tags=["Monitoring"])
async def full_status():
    """
    Devuelve un estado general combinando información del sistema y servicios.
    """
    return {
        "api": "ok",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "services": {
            "database": check_database(),
            "recognition_service": check_recognition_service(),
        },
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


# ------------------------------------------------------------------------------
# Error Handlers (Opcional)
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
# Se puede ejecutar localmente con: python app/main.py
# Aunque en Docker se usa: uvicorn app.main:app --host 0.0.0.0 --port 8000
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )
