import pytest
from unittest.mock import patch, MagicMock
from services.roleManager import RoleManager
from pydantic import ValidationError

# ---------------------------------------------------------
# Helper to build fake database response objects
# (Igual que en tu ejemplo)
# ---------------------------------------------------------
class FakeResponse:
    def __init__(self, data):
        self.data = data

# =========================================================
# CREATE
# =========================================================
@patch("services.roleManager.Database")
def test_create_role_success(mock_db):
    """
    Prueba que al crear un rol:
    1. Se llame a la BD.
    2. Los datos se limpien (ej: 'admin' -> 'Admin', '#fff' -> '#FFFFFF').
    """
    
    # Simulamos que la BD devuelve el rol creado
    mock_db.create_role.return_value = FakeResponse([
        {"id": 10, "name": "Admin", "color": "#FFFFFF"}
    ])

    # INTENCIÓN: Enviamos datos "sucios" (minúsculas, espacios, hex corto)
    role = RoleManager.create(name="  admin  ", color="#fff")

    # VERIFICACIÓN 1: El retorno es correcto
    assert role["id"] == 10
    assert role["name"] == "Admin"

    # VERIFICACIÓN 2: La BD recibió los datos YA LIMPIOS
    # Esto confirma que tu RoleValidator está funcionando dentro del Manager
    mock_db.create_role.assert_called_once_with({
        "name": "Admin", 
        "color": "#FFFFFF"
    })

@patch("services.roleManager.Database")
def test_create_role_invalid_color(mock_db):
    """
    Prueba de validación: Si el color es inválido, debe fallar ANTES de llamar a la BD.
    """
    with pytest.raises(ValidationError):
        RoleManager.create(name="Admin", color="azul-patata")
    
    # La base de datos NUNCA debió ser llamada
    mock_db.create_role.assert_not_called()

# =========================================================
# READ ALL
# =========================================================
@patch("services.roleManager.Database")
def test_read_all_roles(mock_db):
    
    mock_db.get_role_list.return_value = FakeResponse([
        {"id": 1, "name": "Admin", "color": "#FF0000"},
        {"id": 2, "name": "User", "color": "#0000FF"}
    ])

    roles = RoleManager.read_all()

    assert len(roles) == 2
    mock_db.get_role_list.assert_called_once()

# =========================================================
# READ BY ID
# =========================================================
@patch("services.roleManager.Database")
def test_read_by_id(mock_db):
    
    mock_db.get_role.return_value = FakeResponse([
        {"id": 5, "name": "Supervisor", "color": "#00FF00"}
    ])

    role = RoleManager.read_by_id(5)

    assert role["id"] == 5
    assert role["name"] == "Supervisor"
    mock_db.get_role.assert_called_once_with(5)

# =========================================================
# UPDATE
# =========================================================
@patch("services.roleManager.Database")
def test_update_role_success(mock_db):
    """
    Prueba actualizar un rol existente.
    Verifica que se mezclen los datos viejos con los nuevos y se validen.
    """
    
    # 1. Simulamos que el rol original existe en la BD
    original_role = {"id": 1, "name": "Vendedor", "color": "#000000"}
    mock_db.get_role.return_value = FakeResponse([original_role])
    
    # 2. update_role en la BD no suele retornar nada, o retorna status
    mock_db.update_role.return_value = None

    # LLAMADA: Cambiamos solo el color (y lo enviamos en minúsculas para probar validación)
    old_role_returned = RoleManager.update(1, color="#abc")

    # VERIFICACIÓN:
    # El método retorna el estado ANTERIOR del objeto (según tu lógica actual)
    assert old_role_returned["color"] == "#000000"

    # La BD debió ser llamada con el objeto actualizado y validado (#ABC -> #AABBCC)
    mock_db.update_role.assert_called_once_with(
        1,
        {"id": 1, "name": "Vendedor", "color": "#AABBCC"}
    )

# =========================================================
# UPDATE NOT FOUND
# =========================================================
@patch("services.roleManager.Database")
def test_update_role_not_found(mock_db):
    
    # Simulamos que no encuentra el rol (lista vacía)
    mock_db.get_role.return_value = FakeResponse([])

    result = RoleManager.update(99, name="Nuevo")

    # Verificamos el objeto "sentinel" de error que definiste
    assert result["id"] == -1
    assert result["name"] == "None"
    
    # No se debió intentar actualizar nada
    mock_db.update_role.assert_not_called()

# =========================================================
# DELETE
# =========================================================
@patch("services.roleManager.Database")
def test_delete_role(mock_db):
    
    # Simulamos que la BD devuelve el rol eliminado
    mock_db.delete_role.return_value = FakeResponse([
        {"id": 1, "name": "Admin", "color": "#000"}
    ])

    deleted_role = RoleManager.delete(1)

    assert deleted_role["id"] == 1
    mock_db.delete_role.assert_called_once_with(1)

# =========================================================
# DELETE NOT FOUND
# =========================================================
@patch("services.roleManager.Database")
def test_delete_role_not_found(mock_db):
    
    # Simulamos respuesta vacía al intentar borrar
    mock_db.delete_role.return_value = FakeResponse([])

    result = RoleManager.delete(7)

    assert result["id"] == 7
    assert result["name"] == "Null"
    # Nota: validamos también el color dummy que agregamos para evitar errores de validación
    assert result["color"] == "#000000"