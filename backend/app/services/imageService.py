import cv2
import numpy as np


class ImageService:
    """Servicio estático para procesamiento de imágenes."""

    @staticmethod
    def _bytes_to_image(img_bytes: bytes):
        """Convierte bytes a un arreglo de imagen usando OpenCV."""
        if not img_bytes:
            raise ValueError("La imagen recibida está vacía.")

        img_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Los bytes no corresponden a una imagen válida.")

        return img

    # ----------------------------------------------------------------------
    # MÉTODO 1: Comparar dos imágenes (exactas o casi iguales)
    # ----------------------------------------------------------------------

    @classmethod
    def check_face(
        cls, compared_image: bytes, worker_image: bytes, *,
        tolerance: float = 0.75
            ) -> bool:
        """
        Compara dos imágenes y retorna True si son suficientemente similares.
        Usa SSIM (Structural Similarity Index).

        tolerance: Valor entre 0 y 1, donde 1 es igualdad absoluta.
        """
        img1 = cls._bytes_to_image(compared_image)
        img2 = cls._bytes_to_image(worker_image)

        # Redimensionamos para poder comparar
        img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        # Convertimos a escala de grises
        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)

        # Importar aquí evita dependencias globales
        from skimage.metrics import structural_similarity as ssim

        score, _ = ssim(img1_gray, img2_gray, full=True)

        return bool(score >= tolerance)
