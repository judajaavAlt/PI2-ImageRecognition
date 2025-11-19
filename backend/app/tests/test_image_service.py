import pytest
import cv2
import numpy as np
from app.services.imageService import ImageService


# --- Utilidad para convertir imagen numpy a bytes ---
def img_to_bytes(img):
    success, buffer = cv2.imencode(".jpg", img)
    return buffer.tobytes()


# --- Tests del método compare_images ---


def test_compare_images_true_si_son_iguales():
    """Debe retornar True cuando las dos imágenes son idénticas."""
    img = np.full((50, 50, 3), 200, dtype=np.uint8)  # imagen gris
    img_bytes = img_to_bytes(img)

    output = ImageService.compare_images(img_bytes, img_bytes)

    assert isinstance(output, bool)
    assert output is True


def test_compare_images_false_si_son_diferentes():
    """Debe retornar False cuando las dos imágenes no son iguales."""
    img1 = np.full((50, 50, 3), 50, dtype=np.uint8)
    img2 = np.full((50, 50, 3), 200, dtype=np.uint8)

    img1_bytes = img_to_bytes(img1)
    img2_bytes = img_to_bytes(img2)

    output = ImageService.compare_images(img1_bytes, img2_bytes)

    assert isinstance(output, bool)
    assert output is False


def test_compare_images_lanza_error_si_imagen_vacia():
    """Debe lanzar ValueError si alguna imagen está vacía."""
    with pytest.raises(ValueError):
        ImageService.compare_images(b"", b"1234")


def test_compare_images_lanza_error_si_bytes_invalidos():
    """Debe lanzar ValueError si los bytes no corresponden a una imagen."""
    fake_bytes = b"ESTO_NO_ES_IMAGEN"

    with pytest.raises(ValueError):
        ImageService.compare_images(fake_bytes, fake_bytes)
