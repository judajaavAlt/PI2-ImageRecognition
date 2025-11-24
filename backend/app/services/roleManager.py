from db.database import Database
# Importamos tu modelo fuerte para validar los datos aquí
# Asegúrate de que la ruta de importación sea correcta según tu estructura de carpetas
from models.role import Role as RoleValidator 

class RoleManager:

    # ============================================================
    # CREATE
    # ============================================================
    @classmethod
    def create(cls, name: str, color: str):
        # 1. VALIDACIÓN Y LIMPIEZA
        # Creamos una instancia del modelo Role. Esto disparará:
        # - El error si el color no es Hex válido.
        # - La conversión a Title Case del nombre.
        # - La conversión a Mayúsculas del color.
        validated_data = RoleValidator(name=name, color=color)

        new_role = {
            "name": validated_data.name,   # Usamos el nombre ya limpio (Title)
            "color": validated_data.color  # Usamos el color ya validado (Upper)
        }

        # 2. Llamada a la base de datos
        created_role = Database.create_role(new_role).data[0]

        return created_role

    # ============================================================
    # READ ALL
    # ============================================================
    @classmethod
    def read_all(cls):
        return Database.get_role_list().data

    # ============================================================
    # READ BY ID
    # ============================================================
    @classmethod
    def read_by_id(cls, role_id: int):
        response = Database.get_role(role_id).data
        if response:
            return response[0]
        # OJO: La API espera un modelo Role. Si retornas None, la API podría
        # lanzar un error 500 de validación de respuesta.
        # Lo ideal sería retornar None y que la API lance 404, pero como no podemos
        # tocar la API, asegúrate de que tu frontend maneje el null o error.
        return None 

    # ============================================================
    # UPDATE
    # ============================================================
    @classmethod
    def update(cls, role_id: int, **changes):
        current_data = Database.get_role(role_id).data

        if current_data:
            old_role = current_data[0].copy()
            role_to_update = current_data[0]

            # VALIDACIÓN PARCIAL
            # Si vienen cambios, los validamos con el modelo RoleValidator
            # Creamos un objeto temporal mezclando lo viejo con lo nuevo para validar integridad
            temp_data = role_to_update.copy()
            temp_data.update(changes)
            
            # Esto validará que el nuevo color o nuevo nombre sean correctos
            validated_obj = RoleValidator(**temp_data)

            # Actualizamos el diccionario real con los datos validados/limpios
            if "name" in changes:
                role_to_update["name"] = validated_obj.name
            if "color" in changes:
                role_to_update["color"] = validated_obj.color
            
            Database.update_role(role_id, role_to_update)
            
            # NOTA: Tu código original devuelve el 'old_role'. 
            # Generalmente en APIs REST se devuelve el objeto YA actualizado.
            # Pero si esa es la lógica de negocio deseada, está bien.
            return old_role

        # Objeto dummy si no encuentra nada (para que la API no explote)
        return {
            "id": -1,
            "name": "None",
            "color": "#000000" # Puse un color hex válido por si el response_model valida
        }

    # ============================================================
    # DELETE
    # ============================================================
    @classmethod
    def delete(cls, role_id: int):
        role = Database.delete_role(role_id).data
        
        if len(role) == 0:
            return {
                'id': role_id,
                'name': 'Null',
                'color': '#000000' # Color dummy válido
            }
            
        return role[0]