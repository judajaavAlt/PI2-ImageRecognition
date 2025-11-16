# backend/app/db/database.py
"""
Database wrapper para Supabase (tabla 'workers' por defecto).
Permite inyección de cliente (útil para tests).
"""

import os
from typing import Any, Dict, Optional

# Import create_client desde la librería oficial de supabase
from supabase import create_client, Client


class DatabaseError(Exception):
    """Excepción para errores devueltos por la API de Supabase."""

    def __init__(self, message: str, response: Optional[Any] = None):
        super().__init__(message)
        self.response = response


class Database:
    """
    Clase para operaciones básicas sobre la tabla 'workers'.
    Constructor:
        Database(client=None, table_name="workers")
    Si client es None, se crea con SUPABASE_URL y SUPABASE_KEY.
    """

    def __init__(self, client: Optional[Any] = None, table_name: str = "workers"):
        if client:
            self.client = client
        else:
            # Intentar cargar variables de entorno
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            if not url or not key:
                raise RuntimeError("SUPABASE_URL y SUPABASE_KEY deben estar definidas en las variables de entorno")
            self.client = create_client(url, key)

        self.table_name = table_name

    def _handle_response(self, response: Any) -> Dict:
        """
        Normaliza la respuesta de Supabase a un dict simple:
        - Si response es dict, valida 'status'/'status_code' y 'error'.
        - Si response es un objeto, intenta leer attributes comunes.
        - Si la respuesta indica error (status fuera de 2xx o error presente), lanza DatabaseError.
        Retorna dict con al menos 'status_code' y 'data' cuando sea posible.
        """
        # Caso: ya es dict
        if isinstance(response, dict):
            status = response.get("status_code") or response.get("status")
            error = response.get("error")
            # Si hay error o status no 2xx
            if error or (status is not None and not (200 <= int(status) < 300)):
                raise DatabaseError("Respuesta de Supabase indica error", response)
            # Normalizar claves mínimas
            return {
                "status_code": status if status is not None else 200,
                "data": response.get("data"),
                "error": error,
            }

        # Caso: objeto (algunas versiones devuelven objetos)
        status = getattr(response, "status_code", None) or getattr(response, "status", None)
        data = getattr(response, "data", None)
        error = getattr(response, "error", None)

        if error or (status is not None and not (200 <= int(status) < 300)):
            raise DatabaseError("Respuesta de Supabase indica error (objeto)", {"status": status, "error": error, "data": data})

        # Retorno normalizado
        return {"status_code": status if status is not None else 200, "data": data, "error": error}

    def createWorker(self, worker: Dict) -> Dict:
        """
        Inserta un worker (dict con campos).
        Devuelve el dict tal como lo normalizamos.
        Lanza DatabaseError en caso de que la API lo indique.
        """
        resp = self.client.table(self.table_name).insert(worker).execute()
        return self._handle_response(resp)

    def updateWorker(self, worker: Dict) -> Dict:
        """
        Actualiza un worker. 'worker' debe contener 'id'.
        :raises ValueError: si falta 'id'.
        """
        if "id" not in worker:
            raise ValueError("updateWorker requiere 'id' en el diccionario 'worker'")

        _id = worker["id"]
        payload = {k: v for k, v in worker.items() if k != "id"}
        resp = self.client.table(self.table_name).update(payload).eq("id", _id).execute()
        return self._handle_response(resp)

    def DeleteWorker(self, worker: Dict) -> Dict:
        """
        Elimina un worker por 'id'.
        :raises ValueError: si falta 'id'.
        """
        if "id" not in worker:
            raise ValueError("DeleteWorker requiere 'id' en el diccionario 'worker'")

        _id = worker["id"]
        resp = self.client.table(self.table_name).delete().eq("id", _id).execute()
        return self._handle_response(resp)

    def getWorker(self, worker: Dict) -> Dict:
        """
        Obtiene un worker por 'id'.
        :raises ValueError: si falta 'id'.
        """
        if "id" not in worker:
            raise ValueError("getWorker requiere 'id' en el diccionario 'worker'")

        _id = worker["id"]
        resp = self.client.table(self.table_name).select("*").eq("id", _id).execute()
        return self._handle_response(resp)

    def getWorkerList(self) -> Dict:
        """
        Obtiene todos los workers.
        """
        resp = self.client.table(self.table_name).select("*").execute()
        return self._handle_response(resp)