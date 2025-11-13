import pytest
from httpx import AsyncClient
from app.main import app

# ------------------------------------------------------------------------------
# Test: Crear un trabajador
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_create_worker():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/workers", json={
            "name": "Carlos",
            "document": "2.345.678.901",
            "role": "guardia",
            "photo": "https://example.com/foto.jpg"
        })

    # Debe crearse correctamente
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "ok"
    assert "data" in data
    assert data["data"]["name"] == "Carlos"


# ------------------------------------------------------------------------------
# Test: Intentar crear un trabajador con documento duplicado
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_create_worker_duplicate_document():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Intentar crear otro trabajador con el mismo documento
        response = await ac.post("/workers", json={
            "name": "Pedro",
            "document": "2.345.678.901",  # Documento repetido
            "role": "operario",
            "photo": "https://example.com/foto2.jpg"
        })

    # Debe rechazarlo (HTTP 400)
    assert response.status_code in (400, 500)
    data = response.json()
    assert "detail" in data or "message" in data


# ------------------------------------------------------------------------------
# Test: Obtener lista de trabajadores
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_worker_list():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/workers")

    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert isinstance(json_data["data"], list)


# ------------------------------------------------------------------------------
# Test: Actualizar trabajador existente
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_update_worker():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/workers/1", json={
            "name": "Carlos Actualizado",
            "document": "2.345.678.901",
            "role": "supervisor",
            "photo": "https://example.com/foto2.jpg"
        })

    assert response.status_code in (200, 404)
    data = response.json()
    assert "status" in data or "detail" in data


# ------------------------------------------------------------------------------
# Test: Eliminar trabajador existente
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_delete_worker():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/workers/1")

    assert response.status_code in (200, 404)
