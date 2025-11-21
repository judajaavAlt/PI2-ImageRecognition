from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()  # Carga variables de entorno desde .env si está presente


class Database:
    
    workers_table: str = "Worker"
    roles_table: str = "Role"

    load_dotenv()  
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Metodos para la tabla de trabajadores
    
    @classmethod
    def create_worker(cls, payload):
        return (cls.client.table(cls.workers_table)
                .insert(payload).execute()) 
    
    @classmethod
    def update_worker(cls, worker_id, payload):
        return (cls.client.table(cls.workers_table)
                .update(payload).eq("id", worker_id).execute())
    
    @classmethod
    def delete_worker(cls, worker_id):
        return (cls.client.table(cls.workers_table)
                .delete().eq("id", worker_id).execute())
    
    @classmethod
    def get_worker(cls, worker_id):
        return (cls.client.table(cls.workers_table)
                .select("*").eq("id", worker_id).execute())

    @classmethod
    def get_worker_list(cls):
        return (cls.client.table(cls.workers_table)
                .select("*").execute())
    
    @classmethod
    def get_workers_by_document(cls, document):
        return (cls.client.table(cls.workers_table)
                .select("*").eq("document", document).execute())
    
    # Metodos para la tabla de roles

    @classmethod
    def create_role(cls, payload):
        return (cls.client.table(cls.roles_table)
                .insert(payload).execute())

    @classmethod
    def get_role_list(cls):
        return (cls.client.table(cls.roles_table)
                .select("*").execute())
    
    @classmethod
    def get_role(cls, role_id):
        return (cls.client.table(cls.roles_table)
                .select("*").eq("id", role_id).execute())
    
    @classmethod
    def delete_role(cls, role_id):
        return (cls.client.table(cls.roles_table)
                .delete().eq("id", role_id).execute())
    
    @classmethod
    def update_role(cls, role_id, payload):
        return (cls.client.table(cls.roles_table)
                .update(payload).eq("id", role_id).execute())
    
