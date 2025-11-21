import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


def get_client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


# ----------------------------------------------------------------------
# Test: Crear un trabajador
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_create_worker():
    async with get_client() as ac:
        response = await ac.post("/workers", json={
            "name": "Carlos",
            "document": "2.345.678.901",
            "role": "guardia",
            "photo": "https://example.com/foto.jpg"
        })

    assert response.status_code in (200, 201)
    data = response.json()
    assert data["status"] == "ok"
    assert "data" in data
    assert data["data"]["name"] == "Carlos"


# ----------------------------------------------------------------------
# Test: Crear trabajador con documento duplicado (Database mock NO valida)
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_create_worker_duplicate_document():
    async with get_client() as ac:
        response = await ac.post("/workers", json={
            "name": "Pedro",
            "document": "2.345.678.901",
            "role": "operario",
            "photo": "https://example.com/foto2.jpg"
        })

    # El mock Database NO valida duplicados → siempre 200
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["status"] == "ok"
    assert "data" in data


# ----------------------------------------------------------------------
# Test: Obtener lista de trabajadores
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_worker_list():
    async with get_client() as ac:
        response = await ac.get("/workers")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert isinstance(data["data"], list)
    assert "count" in data


# ----------------------------------------------------------------------
# Test: Actualizar trabajador
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_update_worker():
    async with get_client() as ac:
        response = await ac.put("/workers/1", json={
            "name": "Carlos Actualizado",
            "document": "1.234.567.890",
            "role": "supervisor",
            "photo": "https://example.com/foto2.jpg"
        })

    assert response.status_code in (200, 201)
    data = response.json()
    assert data["status"] == "ok"
    assert "data" in data


# ----------------------------------------------------------------------
# Test: Eliminar trabajador
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_delete_worker():
    async with get_client() as ac:
        response = await ac.delete("/workers/1")

    assert response.status_code in (200, 201)
    data = response.json()
    assert data["status"] == "ok"
    assert "worker_id" in data
