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

    # ----------------------------------------------------------------------
    # MÉTODO 2: Detectar si el color de la camiseta coincide con un color hex
    # ----------------------------------------------------------------------

    @classmethod
    def check_role(
        cls, compared_image: bytes, hex_color: str, *,
        tolerance: int = 25,
        match_threshold: float = 0.15
    ) -> bool:
        """
        Determina si la camiseta de la persona
        coincide con el color hexadecimal dado.

        - hex_color: formato "#RRGGBB" o "RRGGBB"
        - tolerance: margen permitido para H, S y V
        - match_threshold: % mínimo de píxeles que deben coincidir (0.0–1.0)
        """

        img = cls._bytes_to_image(compared_image)

        h, w, _ = img.shape

        # Tomamos el tercio inferior-central
        y1 = int(h * 0.55)
        y2 = int(h * 0.90)
        x1 = int(w * 0.25)
        x2 = int(w * 0.75)

        shirt_region = img[y1:y2, x1:x2]

        # Convertir ROI a HSV
        hsv_img = cv2.cvtColor(shirt_region, cv2.COLOR_BGR2HSV)

        # Convertir hex → BGR
        hex_color = hex_color.lstrip("#")

        # Convertir color a HSV
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        bgr = rgb[::-1]

        target = np.uint8([[bgr]])
        hsv_target = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)[0][0]

        h, s, v = [int(x) for x in hsv_target]

        # Rango mínimo y máximo según tolerancia
        lower = np.array([
            max(h - tolerance, 0),
            max(s - tolerance, 0),
            max(v - tolerance, 0)
        ], dtype=np.uint8)

        upper = np.array([
            min(h + tolerance, 255),
            min(s + tolerance, 255),
            min(v + tolerance, 255)
        ], dtype=np.uint8)

        # Crear máscara
        mask = cv2.inRange(hsv_img, lower, upper)

        # Calcular porcentaje de coincidencia
        match_ratio = np.count_nonzero(mask) / mask.size

        return bool(match_ratio >= match_threshold)
