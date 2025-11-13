from typing import Dict, Any

# Simulación temporal de base de datos
_FAKE_DB = {
    1: {"id": 1, "name": "Pepito", "document": "1.234.567.890", "role": "guardia", "photo": "https://example.com/foto.jpg"}
}
_next_id = 2


class WorkerManagerService:
    """
    Servicio encargado de gestionar los trabajadores:
    creación, lectura, actualización y eliminación.
    """

    @staticmethod
    async def fetch_workers() -> Dict[str, Any]:
        try:
            data = list(_FAKE_DB.values())
            return {"data": data, "count": len(data)}
        except Exception as e:
            raise Exception(f"Error al obtener trabajadores: {e}")

    @staticmethod
    async def get_worker(worker_id: int) -> Dict[str, Any] | None:
        try:
            return _FAKE_DB.get(worker_id)
        except Exception as e:
            raise Exception(f"Error al obtener trabajador: {e}")

    @staticmethod
    async def create_worker(worker_data: Dict[str, Any]) -> Dict[str, Any]:
        global _next_id
        try:
            # Verificar duplicado por documento
            for w in _FAKE_DB.values():
                if w["document"] == worker_data["document"]:
                    raise ValueError(f"Ya existe un trabajador con documento {worker_data['document']}")

            # Crear nuevo trabajador
            worker_data["id"] = _next_id
            _FAKE_DB[_next_id] = worker_data
            _next_id += 1
            return worker_data
        except Exception as e:
            raise Exception(f"Error al crear trabajador: {e}")

    @staticmethod
    async def update_worker(worker_id: int, worker_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if worker_id not in _FAKE_DB:
                raise ValueError("Trabajador no encontrado")

            # Verificar duplicado por documento (excluyendo al mismo)
            for existing_id, w in _FAKE_DB.items():
                if existing_id != worker_id and w["document"] == worker_data["document"]:
                    raise ValueError(f"Ya existe otro trabajador con documento {worker_data['document']}")

            _FAKE_DB[worker_id].update(worker_data)
            return _FAKE_DB[worker_id]
        except Exception as e:
            raise Exception(f"Error al actualizar trabajador: {e}")

    @staticmethod
    async def delete_worker(worker_id: int) -> Dict[str, Any]:
        try:
            if worker_id not in _FAKE_DB:
                raise ValueError("Trabajador no encontrado")
            deleted = _FAKE_DB.pop(worker_id)
            return deleted
        except Exception as e:
            raise Exception(f"Error al eliminar trabajador: {e}")
