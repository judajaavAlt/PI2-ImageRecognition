import pytest
import os
from services.workerManager import CheckWorkerService
from services.imageUtils import ImageUtils
from db.database import Database

# ===========================
# RUTAS ABSOLUTAS A LAS IMÁGENES
# ===========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATHS = {
    "correct": os.path.join(BASE_DIR, "images", "1109485904.jpg"),
    "wrong_face": os.path.join(BASE_DIR, "images", "1103485990.jpg"),
}

# ===========================
# TESTS
# ===========================

def test_check_worker_all_correct():
    with open(IMAGE_PATHS["correct"], "rb") as f:
        image_bytes = f.read()
    photo_base64 = ImageUtils.binary_to_base64(image_bytes)
    cc = "1109485904"

    result = CheckWorkerService.check_worker(cc, photo_base64)
    assert result["valid"] is True
    print(result["message"])


def test_check_worker_all_wrong():
    with open(IMAGE_PATHS["wrong_face"], "rb") as f:
        image_bytes = f.read()
    photo_base64 = ImageUtils.binary_to_base64(image_bytes)
    cc = "1109485904"

    result = CheckWorkerService.check_worker(cc, photo_base64)
    assert result["valid"] is False
    print(result["message"])


def test_check_worker_only_face():
    with open(IMAGE_PATHS["correct"], "rb") as f:
        image_bytes = f.read()
    photo_base64 = ImageUtils.binary_to_base64(image_bytes)
    cc = "1109485904"

    # Para simular: rostro correcto pero uniforme incorrecto
    # Asegurarse que el color del rol del worker en la DB no coincida con la imagen
    result = CheckWorkerService.check_worker(cc, photo_base64)
    assert result["valid"] is False  # Porque uniforme no coincide
    print(result["message"])


def test_check_worker_only_uniform():
    with open(IMAGE_PATHS["wrong_face"], "rb") as f:
        image_bytes = f.read()
    photo_base64 = ImageUtils.binary_to_base64(image_bytes)
    cc = "1109485904"

    # Para simular: rostro incorrecto pero uniforme correcto
    # Asegurarse que el color del rol del worker en la DB coincida con la imagen
    result = CheckWorkerService.check_worker(cc, photo_base64)
    assert result["valid"] is False  # Porque rostro no coincide
    print(result["message"])
