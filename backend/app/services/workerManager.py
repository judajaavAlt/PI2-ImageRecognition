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
    def check_worker(cc: str, photo_base64: str) -> dict:
        """
        1. Convierte base64 → bytes usando ImageUtils.
        2. Busca el worker en Database.
        3. Compara rostro con ImageService.check_face.
        4. Valida uniforme con ImageService.check_role.
        5. Retorna {valid, message, audio}.
        """

        # --------------------------
        # 1. Validar y convertir base64
        # --------------------------

        if not photo_base64 or not ImageUtils.validate_base64(photo_base64):
            message = "La imagen recibida no es válida o no está en formato base64."
            return {
                "valid": False,
                "message": message,
                "audio": SpeechService.text_to_audio(message)
            }

        # Convertir base64 → bytes
        user_img_bytes = ImageUtils.base64_to_binary(photo_base64)

        # --------------------------
        # 2. Buscar worker por CC
        # --------------------------

        result = Database.get_workers()
        workers = result.get("content", [])

        worker = next((w for w in workers if w.get("document") == str(cc)), None)

        if worker is None:
            message = "No existe ningún trabajador con esa cédula."
            return {
                "valid": False,
                "message": message,
                "audio": SpeechService.text_to_audio(message)
            }

        # --------------------------
        # 3. Obtener foto del worker (base64 → bytes)
        # --------------------------

        worker_photo_b64 = worker.get("photo")

        if not ImageUtils.validate_base64(worker_photo_b64):
            message = "La foto almacenada del trabajador no es válida."
            return {
                "valid": False,
                "message": message,
                "audio": SpeechService.text_to_audio(message)
            }

        worker_img_bytes = ImageUtils.base64_to_binary(worker_photo_b64)

        # --------------------------
        # 4. Comparar rostro
        # --------------------------

        face_match = ImageService.check_face(
            compared_image=user_img_bytes,
            worker_image=worker_img_bytes
        )

        if not face_match:
            message = "El rostro no coincide con el trabajador registrado."
            return {
                "valid": False,
                "message": message,
                "audio": SpeechService.text_to_audio(message)
            }

        # --------------------------
        # 5. Validar uniforme según el rol
        # --------------------------

        role = worker.get("role")
        role_color = Database.get_role_color(role)

        uniform_ok = ImageService.check_role(
            compared_image=user_img_bytes,
            hex_color=role_color
        )

        if not uniform_ok:
            message = (
                "Rostro verificado, pero el uniforme no coincide con el color "
                f"asignado al rol ({role_color})."
            )
            return {
                "valid": False,
                "message": message,
                "audio": SpeechService.text_to_audio(message)
            }

        # --------------------------
        # 6. Todo correcto
        # --------------------------

        message = (
            f"Trabajador {worker.get('name')} verificado correctamente. "
            "Identidad y uniforme coinciden."
        )

        return {
            "valid": True,
            "message": message,
            "audio": SpeechService.text_to_audio(message)
        }
