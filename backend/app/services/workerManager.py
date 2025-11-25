from db.database import Database
from services.imageService import ImageService
from services.speechService import SpeechService
from services.imageUtils import ImageUtils
import base64

def render_audio(message):
    audio_bytes = SpeechService.text_to_audio(message)
    return base64.b64encode(audio_bytes).decode('utf-8')

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

    @staticmethod
    def check_worker(cc: int, photo_base64: str) -> dict:
        if not photo_base64 or not ImageUtils.validate_base64(photo_base64):
            message = "La imagen recibida no es válida o no está en el formato correcto."
            return {"match": False, "message": render_audio(message)}

        user_img_bytes = ImageUtils.base64_to_binary(photo_base64)

        # Obtener worker por documento
        result = Database.get_workers_by_document(str(cc)).data
        if len(result) == 0:
            message = "No existe ningún trabajador con esa cédula."
            return {"match": False, "message": render_audio(message)}

        worker = result[0]
        worker_photo_b64 = worker.get("photo")
        worker_img_bytes = ImageUtils.base64_to_binary(worker_photo_b64)

        # Comparar rostro
        face_match = ImageService.check_face(compared_image=user_img_bytes,
                                             worker_image=worker_img_bytes,
                                             tolerance=0.30)
        if not face_match:
            message = "El rostro no coincide con el trabajador registrado."
            return {"match": False, "message": render_audio(message)}

        # Validar uniforme según rol
        role_id = worker.get("role")
        role_result = Database.get_role(role_id)
        role_data = role_result.data[0] if hasattr(role_result, "data") and role_result.data else {}
        role_color = role_data.get("color", "#000000")

        uniform_ok = ImageService.check_role(compared_image=user_img_bytes,
                                             hex_color=role_color,
                                             tolerance=30)
        if not uniform_ok:
            message = (f"Rostro verificado, pero el uniforme no coincide con el color "
                       f"asignado al rol.")
            return {"match": False, "message": render_audio(message)}

        # Todo correcto
        message = (f"Trabajador {worker.get('name')} verificado correctamente. "
                   "Identidad y uniforme coinciden.")
        return {"match": True, "message": render_audio(message)}