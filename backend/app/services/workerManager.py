from db.database import Database
from services.imageService import ImageService
from services.speechService import SpeechService
from services.imageUtils import ImageUtils


class WorkerManager:


    # ============================================================
    # CREATE → Crear un trabajador con validación de duplicados
    # ============================================================
    @classmethod
    def create(cls, name: str, document: str, role: int, photo: str):

        new_worker = {"name": name,
                      "document": document,
                      "role": role,
                      "photo": photo}

        new_worker = Database.create_worker(new_worker).data[0]

        return new_worker

    # ============================================================
    # READ ALL → Obtener todos los trabajadores
    # ============================================================
    @classmethod
    def read_all(cls):
        return Database.get_worker_list().data

    # ============================================================
    # READ BY ID → Obtener trabajador por ID
    # ============================================================
    @classmethod
    def read_by_id(cls, worker_id: int):
        return Database.get_worker(worker_id).data[0]

    # ============================================================
    # UPDATE → Actualizar trabajador
    # (Incluye validación de duplicado si se cambia "document")
    # ============================================================
    @classmethod
    def update(cls, worker_id: int, **changes):
        workers = Database.get_worker_list().data

        for w in workers:
            if w["id"] == worker_id:

                old_worker = w.copy()

                # Aplicar cambios
                for key, value in changes.items():
                    if key in w:
                        w[key] = value

                Database.update_worker(worker_id, w)
                return old_worker

        return {"id": -1,
                "name": "None",
                "document": "None",
                "role": "None",
                "photo": "None"}

    # ============================================================
    # DELETE → Eliminar trabajador
    # ============================================================
    @classmethod
    def delete(cls, worker_id: int):
        worker = Database.delete_worker(worker_id).data
        if len(worker) == 0:
            return {'id': worker_id,
                    'name': 'Null',
                    'document': 'Null',
                    'role': 0,
                    'photo': 'Null'}
        return worker[0]


# ============================================================
# CHECK WORKER SERVICE → Verificación de identidad por imagen
# ============================================================
class CheckWorkerService:

    @staticmethod
    def check_worker(image_base64: str) -> dict:
        """
        1. Convierte base64 → binario usando ImageUtils.
        2. Usa ImageService para reconocer documento y uniforme.
        3. Busca el worker en Database.
        4. Valida identidad y uniforme.
        5. Retorna {valid, message, audio}.
        """

        # --------------------------
        # 1. Validar y convertir base64
        # --------------------------

        if not image_base64 or not ImageUtils.validate_base64(image_base64):
            message = "La imagen recibida no es válida o no está en formato base64."
            return {
                "valid": False,
                "message": message,
                "audio": SpeechService.text_to_audio(message)
            }

        # Convertir base64 → binario
        image_bytes = ImageUtils.base64_to_binary(image_base64)

        # --------------------------
        # 2. Analizar imagen con IA
        # --------------------------

        image_result = ImageService.check_worker_in_image(image_bytes)

        if not image_result:
            message = "No se pudo procesar la imagen correctamente."
            return {
                "valid": False,
                "message": message,
                "audio": SpeechService.text_to_audio(message)
            }

        detected_doc = image_result.get("document")
        detected_uniform = image_result.get("uniform")

        # Validación mínima
        if not detected_doc:
            message = "No se pudo reconocer el documento del trabajador."
            return {
                "valid": False,
                "message": message,
                "audio": SpeechService.text_to_audio(message)
            }

        # --------------------------
        # 3. Buscar trabajador en la base de datos
        # --------------------------

        workers = Database.get_worker_list().data
        worker = next((w for w in workers if w.get("document") == detected_doc), None)

        if worker is None:
            message = "El documento detectado no corresponde a ningún trabajador registrado."
            return {
                "valid": False,
                "message": message,
                "audio": SpeechService.text_to_audio(message)
            }

        # --------------------------
        # 4. Validar uniforme
        # --------------------------

        expected_uniform = worker.get("role")

        if detected_uniform != expected_uniform:
            message = (
                f"Identidad verificada pero el uniforme es incorrecto. "
                f"El uniforme correcto debe ser: {expected_uniform}."
            )
            return {
                "valid": False,
                "message": message,
                "audio": SpeechService.text_to_audio(message)
            }

        # --------------------------
        # 5. Todo correcto
        # --------------------------

        message = (
            f"Trabajador {worker.get('name')} verificado correctamente. "
            f"Uniforme y documento coinciden."
        )

        return {
            "valid": True,
            "message": message,
            "audio": SpeechService.text_to_audio(message)
        }
