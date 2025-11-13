import socket
import time
import os
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from app.services.monitoringService import check_database
from app.services.monitoringService import check_recognition_service
from app.services.monitoringService import check_speech_service

router = APIRouter()


@router.get("/health", tags=["Monitoring"])
async def health_check():
    """
    Verifica si la API principal está viva.
    Devuelve un estado HTTP 200 si está operativa.
    """
    return {"status": "ok", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}


@router.get("/info", tags=["Monitoring"])
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


@router.get("/services/health", tags=["Monitoring"])
async def services_health_check():
    """
    Verifica el estado de los servicios asociados al backend:
    - Base de datos
    - Servicio de reconocimiento
    """
    db_status = check_database()
    rec_status = check_recognition_service()
    sp_status = check_speech_service()

    all_ok = db_status and rec_status and sp_status

    response = {
        "database": "ok" if db_status else "down",
        "recognition_service": "ok" if rec_status else "down",
        "speech_service": "ok" if sp_status else "down",
        "overall_status": "ok" if all_ok else "degraded",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    status_code = 200 if all_ok else 503
    return JSONResponse(content=response, status_code=status_code)


@router.get("/status", tags=["Monitoring"])
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
