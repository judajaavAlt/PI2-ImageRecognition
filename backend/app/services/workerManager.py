from db.database import Database
from services.imageService import ImageService
from services.speechService import SpeechService

class WorkerManager:
    filename = "workers.json"

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
    # CHECK WORKER → Verificar identidad mediante imagen,
    # validar uniforme y generar audio de respuesta
    # ============================================================
    @classmethod
    def check_worker(cls, image_bytes: bytes):
        """
        1. Usa ImageService para reconocer documento y uniforme.
        2. Busca el worker en BDD.
        3. Valida identidad y uniforme.
        4. Retorna {valid, message, audio}.
        """

        # 1. Analizar imagen con IA
        image_result = ImageService.check_worker_in_image(image_bytes)
        """
        Se espera que image_result retorne algo como:
        {
            "document": "1032456789",
            "uniform": 2,
            "confidence": 0.94
        }
        """

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

        # 2. Buscar trabajador en la base de datos
        workers = Database.get_worker_list().data
        worker = next((w for w in workers if w["document"] == detected_doc), None)

        if worker is None:
            message = (
                "El documento detectado no corresponde a ningún trabajador registrado."
            )
            return {
                "valid": False,
                "message": message,
                "audio": SpeechService.text_to_audio(message)
            }

        # 3. Validar uniforme
        if worker["role"] != detected_uniform:
            message = (
                f"Identidad verificada pero el uniforme es incorrecto. "
                f"El uniforme correcto debe ser: {worker['role']}."
            )
            return {
                "valid": False,
                "message": message,
                "audio": SpeechService.text_to_audio(message)
            }

        # 4. Todo correcto
        message = (
            f"Trabajador {worker['name']} verificado correctamente. "
            f"Uniforme y documento coinciden."
        )
        return {
            "valid": True,
            "message": message,
            "audio": SpeechService.text_to_audio(message)
        }
