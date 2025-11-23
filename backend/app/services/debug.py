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

