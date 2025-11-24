from db.database import Database


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
