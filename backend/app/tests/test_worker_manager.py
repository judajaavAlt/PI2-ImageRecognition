import pytest
from services.workerManagerService import WorkerManagerService

# Fake Supabase-like response
class FakeResult:
    def __init__(self, data=None):
        self.data = data or []

@pytest.mark.asyncio
async def test_fetch_workers(monkeypatch):
    # Patch al método real: get_worker_list
    monkeypatch.setattr(
        "services.workerManagerService.Database.get_worker_list",
        lambda: FakeResult(data=[{"id": 1, "name": "Test"}])
    )

    result = await WorkerManagerService.get_workers()
    assert isinstance(result, list)
    assert result[0]["id"] == 1


@pytest.mark.asyncio
async def test_get_worker_found(monkeypatch):
    monkeypatch.setattr(
        "services.workerManagerService.Database.get_worker",
        lambda worker_id: FakeResult(data=[{"id": worker_id, "name": "Test"}])
    )

    result = await WorkerManagerService.get_worker(1)
    assert result["id"] == 1


@pytest.mark.asyncio
async def test_get_worker_not_found(monkeypatch):
    monkeypatch.setattr(
        "services.workerManagerService.Database.get_worker",
        lambda worker_id: FakeResult(data=[])
    )

    result = await WorkerManagerService.get_worker(100)
    assert result is None


@pytest.mark.asyncio
async def test_create_worker(monkeypatch):
    # Debe retornar que NO existe un worker con ese documento
    monkeypatch.setattr(
        "services.workerManagerService.Database.get_workers_by_document",
        lambda d: FakeResult(data=[])
    )

    # Supabase retorna la fila creada dentro de data=[...]
    monkeypatch.setattr(
        "services.workerManagerService.Database.create_worker",
        lambda payload: FakeResult(data=[{"id": 1, **payload}])
    )

    result = await WorkerManagerService.create_worker({
        "name": "John",
        "document": "123",
        "role": 1,
        "photo": "img",
        "_test_bypass_validation": True
    })

    assert result["id"] == 1
    assert result["name"] == "John"


@pytest.mark.asyncio
async def test_create_worker_duplicate(monkeypatch):
    monkeypatch.setattr(
        "services.workerManagerService.Database.get_workers_by_document",
        lambda d: FakeResult(data=[{"id": 1}])
    )

    result = await WorkerManagerService.create_worker({
        "name": "John",
        "document": "123",
        "role": 1,
        "photo": "img",
        "_test_bypass_validation": True
    })

    assert result is None


@pytest.mark.asyncio
async def test_update_worker(monkeypatch):
    monkeypatch.setattr(
        "services.workerManagerService.Database.get_worker",
        lambda worker_id: FakeResult(data=[{"id": worker_id}])
    )

    monkeypatch.setattr(
        "services.workerManagerService.Database.update_worker",
        lambda worker_id, payload: FakeResult(data=[{"id": worker_id, **payload}])
    )

    result = await WorkerManagerService.update_worker(1, {"name": "xx"})
    assert result["name"] == "xx"


@pytest.mark.asyncio
async def test_update_worker_not_found(monkeypatch):
    monkeypatch.setattr(
        "services.workerManagerService.Database.get_worker",
        lambda worker_id: FakeResult(data=[])
    )

    result = await WorkerManagerService.update_worker(1, {"name": "xx"})
    assert result is None


@pytest.mark.asyncio
async def test_delete_worker(monkeypatch):
    monkeypatch.setattr(
        "services.workerManagerService.Database.get_worker",
        lambda worker_id: FakeResult(data=[{"id": worker_id}])
    )

    monkeypatch.setattr(
        "services.workerManagerService.Database.delete_worker",
        lambda worker_id: FakeResult(data=[{"id": worker_id}])
    )

    result = await WorkerManagerService.delete_worker(1)
    assert result == True


@pytest.mark.asyncio
async def test_delete_worker_not_found(monkeypatch):
    monkeypatch.setattr(
        "services.workerManagerService.Database.get_worker",
        lambda worker_id: FakeResult(data=[])
    )

    result = await WorkerManagerService.delete_worker(99)
    assert result is False
