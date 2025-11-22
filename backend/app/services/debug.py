import json
import os


# ============================================================
#  Base Class to handle file operations (optional but useful)
# ============================================================

class JSONStorage:
    filename = ""

    @classmethod
    def _load(cls):
        """Load the JSON file or return empty list."""
        if not os.path.exists(cls.filename):
            return []
        with open(cls.filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    @classmethod
    def _save(cls, data):
        """Save list of dicts to JSON file."""
        with open(cls.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


# ============================================================
#  ROLE MANAGER
# ============================================================

class RoleManager(JSONStorage):
    filename = "roles.json"

    @classmethod
    def create(cls, name: str, color: str):
        roles = cls._load()

        new_id = (max([r["id"] for r in roles]) + 1) if roles else 1

        new_role = {
            "id": new_id,
            "name": name,
            "color": color
        }

        roles.append(new_role)
        cls._save(roles)

        return new_role

    @classmethod
    def read_all(cls):
        return cls._load()

    @classmethod
    def read_by_id(cls, role_id: int):
        roles = cls._load()
        return next((r for r in roles if r["id"] == role_id), None)

    @classmethod
    def update(cls, role_id: int, **changes):
        roles = cls._load()

        for r in roles:
            if r["id"] == role_id:
                old_role = r.copy()               # store before changes
                for key, value in changes.items():
                    if key in r:
                        r[key] = value
                cls._save(roles)
                return r, old_role                # (updated, previous_state)

        return None, None


    @classmethod
    def delete(cls, role_id: int):
        roles = cls._load()

        for r in roles:
            if r["id"] == role_id:
                deleted_role = r.copy()
                new_roles = [x for x in roles if x["id"] != role_id]
                cls._save(new_roles)
                return deleted_role               # return deleted element

        return None

# ============================================================
#  WORKER MANAGER
# ============================================================

class WorkerManager(JSONStorage):
    filename = "workers.json"

    # ============================================================
    # CREATE → Crear un trabajador con validación de duplicados
    # ============================================================
    @classmethod
    def create(cls, name: str, document: str, role: int, photo: str):
        workers = cls._load()

        # Validación: documento duplicado
        if any(w["document"] == document for w in workers):
            raise ValueError(f"El documento {document} ya está registrado")

        new_id = (max([w["id"] for w in workers]) + 1) if workers else 1

        new_worker = {
            "id": new_id,
            "name": name,
            "document": document,
            "role": role,      # ID del rol
            "photo": photo
        }

        workers.append(new_worker)
        cls._save(workers)

        return new_worker

    # ============================================================
    # READ ALL → Obtener todos los trabajadores
    # ============================================================
    @classmethod
    def read_all(cls):
        return cls._load()

    # ============================================================
    # READ BY ID → Obtener trabajador por ID
    # ============================================================
    @classmethod
    def read_by_id(cls, worker_id: int):
        workers = cls._load()
        return next((w for w in workers if w["id"] == worker_id), None)

    # ============================================================
    # UPDATE → Actualizar trabajador
    # (Incluye validación de duplicado si se cambia "document")
    # ============================================================
    @classmethod
    def update(cls, worker_id: int, **changes):
        workers = cls._load()

        for w in workers:
            if w["id"] == worker_id:

                old_worker = w.copy()

                # 🔍 Validación: no permitir que dos workers tengan el mismo doc
                if "document" in changes:
                    new_doc = changes["document"]
                    if any(x["document"] == new_doc and x["id"] != worker_id for x in workers):
                        raise ValueError(f"El documento {new_doc} ya está registrado")

                # Aplicar cambios
                for key, value in changes.items():
                    if key in w:
                        w[key] = value

                cls._save(workers)
                return w, old_worker

        return None, None

    # ============================================================
    # DELETE → Eliminar trabajador
    # ============================================================
    @classmethod
    def delete(cls, worker_id: int):
        workers = cls._load()

        for w in workers:
            if w["id"] == worker_id:
                deleted_worker = w.copy()
                new_workers = [x for x in workers if x["id"] != worker_id]
                cls._save(new_workers)
                return deleted_worker

        return None
