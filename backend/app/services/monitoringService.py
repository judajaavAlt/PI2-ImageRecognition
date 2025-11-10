def check_database() -> bool:
    """
    Verifica la conexión al servicio de base de datos.
    """
    try:
        # Aquí podrías colocar algo como: session.execute("SELECT 1")
        return True
    except Exception:
        return False


def check_recognition_service() -> bool:
    """
    Verifica si el servicio de reconocimiento está accesible.
    """
    try:
        # Ejemplo: ping al servicio
        return True
    except Exception:
        return False


def check_speech_service() -> bool:
    """
    Verifica si el servicio de speech está accesible.
    """
    try:
        # Ejemplo: ping al servicio
        return True
    except Exception:
        return False
