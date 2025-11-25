import base64
from typing import Union


class ImageUtils:
    """Utilidades para manejar conversión de imágenes entre binario y base64"""

    @staticmethod
    def binary_to_base64(binary_data: bytes) -> str:
        """
        Convierte datos binarios de imagen a string base64
        
        Args:
            binary_data: Datos binarios de la imagen
            
        Returns:
            String en formato base64
        """
        if not binary_data:
            return ""
        
        return base64.b64encode(binary_data).decode('utf-8')

    @staticmethod
    def base64_to_binary(base64_string: str) -> bytes:
        """
        Convierte string base64 a datos binarios
        
        Args:
            base64_string: String en formato base64
            
        Returns:
            Datos binarios de la imagen
        """
        if not base64_string:
            return b""
        
        # Remover prefijo 'data:image/...;base64,' si existe
        if ',' in base64_string and base64_string.startswith('data:'):
            base64_string = base64_string.split(',', 1)[1]
        
        return base64.b64decode(base64_string)

    @staticmethod
    def validate_base64(base64_string: str) -> bool:
        """
        Valida si un string es base64 válido
        
        Args:
            base64_string: String a validar
            
        Returns:
            True si es base64 válido, False en caso contrario
        """
        try:
            if not base64_string:
                return False
            
            # Remover prefijo si existe
            if ',' in base64_string and base64_string.startswith('data:'):
                base64_string = base64_string.split(',', 1)[1]
            
            # Intentar decodificar
            base64.b64decode(base64_string)
            return True
        except Exception:
            return False

    @staticmethod
    def ensure_base64_prefix(base64_string: str, mime_type: str = "image/jpeg") -> str:
        """
        Asegura que el string base64 tenga el prefijo data URI correcto
        
        Args:
            base64_string: String base64
            mime_type: Tipo MIME de la imagen (default: image/jpeg)
            
        Returns:
            String base64 con prefijo data URI
        """
        if not base64_string:
            return ""
        
        # Si ya tiene prefijo, retornarlo tal cual
        if base64_string.startswith('data:'):
            return base64_string
        
        # Agregar prefijo
        return f"data:{mime_type};base64,{base64_string}"
