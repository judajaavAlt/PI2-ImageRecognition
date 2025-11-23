import json
import os
from services.imageUtils import ImageUtils


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

    @classmethod
    def create(cls, name: str, document: str, role: int, photo: str):
        workers = cls._load()

        new_id = (max([w["id"] for w in workers]) + 1) if workers else 1

        # Convertir photo a base64 si es necesario
        if photo and isinstance(photo, bytes):
            photo = ImageUtils.binary_to_base64(photo)

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

    @classmethod
    def read_all(cls):
        return cls._load()

    @classmethod
    def read_by_id(cls, worker_id: int):
        workers = cls._load()
        return next((w for w in workers if w["id"] == worker_id), None)

    @classmethod
    def update(cls, worker_id: int, **changes):
        workers = cls._load()

        # Convertir photo a base64 si está presente y es binario
        if 'photo' in changes and changes['photo']:
            if isinstance(changes['photo'], bytes):
                changes['photo'] = ImageUtils.binary_to_base64(changes['photo'])

        for w in workers:
            if w["id"] == worker_id:
                old_worker = w.copy()
                for key, value in changes.items():
                    if key in w:
                        w[key] = value
                cls._save(workers)
                return w, old_worker              # (updated, previous_state)

        return None, None

    @classmethod
    def delete(cls, worker_id: int):
        workers = cls._load()

        for w in workers:
            if w["id"] == worker_id:
                deleted_worker = w.copy()
                new_workers = [x for x in workers if x["id"] != worker_id]
                cls._save(new_workers)
                return deleted_worker              # return deleted element

        return None
