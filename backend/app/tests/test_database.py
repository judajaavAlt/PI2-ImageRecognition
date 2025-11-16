# backend/app/tests/test_database.py
import pytest
from app.db.database import Database, DatabaseError

# Todos los tests usan el fixture `mocker` de pytest-mock.
# Asegúrate de ejecutar pytest desde la carpeta `backend` (cd backend && pytest -q)


def test_create_worker_success(mocker):
    fake_response = {"data": [{"id": 1, "name": "Alice"}], "status_code": 201}
    mock_table = mocker.Mock()
    mock_table.insert.return_value.execute.return_value = fake_response

    mock_client = mocker.Mock()
    mock_client.table.return_value = mock_table

    db = Database(client=mock_client)
    result = db.createWorker({"name": "Alice"})
    assert result["data"][0]["name"] == "Alice"
    assert result["status_code"] == 201


def test_create_worker_failure_raises_database_error(mocker):
    fake_response = {"data": None, "status_code": 400, "error": {"message": "Bad request"}}
    mock_table = mocker.Mock()
    mock_table.insert.return_value.execute.return_value = fake_response

    mock_client = mocker.Mock()
    mock_client.table.return_value = mock_table

    db = Database(client=mock_client)
    with pytest.raises(DatabaseError) as excinfo:
        db.createWorker({"name": ""})
    # Comprobamos que la excepción contiene la respuesta
    assert excinfo.value.response["status_code"] == 400
    assert "Bad request" in str(excinfo.value.response["error"]["message"])


def test_update_worker_success(mocker):
    fake_response = {"data": [{"id": 1, "name": "Alice", "role": "dev"}], "status_code": 200}
    mock_table = mocker.Mock()
    mock_table.update.return_value.eq.return_value.execute.return_value = fake_response

    mock_client = mocker.Mock()
    mock_client.table.return_value = mock_table

    db = Database(client=mock_client)
    result = db.updateWorker({"id": 1, "role": "dev"})
    assert result["data"][0]["role"] == "dev"
    assert result["status_code"] == 200


def test_update_worker_missing_id_raises_value_error(mocker):
    mock_client = mocker.Mock()
    db = Database(client=mock_client)
    with pytest.raises(ValueError):
        db.updateWorker({"role": "dev"})  # falta id


def test_delete_worker_success(mocker):
    fake_response = {"data": [{"id": 2}], "status_code": 200}
    mock_table = mocker.Mock()
    mock_table.delete.return_value.eq.return_value.execute.return_value = fake_response

    mock_client = mocker.Mock()
    mock_client.table.return_value = mock_table

    db = Database(client=mock_client)
    result = db.DeleteWorker({"id": 2})
    assert result["data"][0]["id"] == 2
    assert result["status_code"] == 200


def test_get_worker_success(mocker):
    fake_response = {"data": [{"id": 3, "name": "Bob"}], "status_code": 200}
    mock_table = mocker.Mock()
    mock_table.select.return_value.eq.return_value.execute.return_value = fake_response

    mock_client = mocker.Mock()
    mock_client.table.return_value = mock_table

    db = Database(client=mock_client)
    result = db.getWorker({"id": 3})
    assert result["data"][0]["id"] == 3
    assert result["data"][0]["name"] == "Bob"


def test_get_worker_list_success(mocker):
    fake_response = {"data": [{"id": 1}, {"id": 2}], "status_code": 200}
    mock_table = mocker.Mock()
    mock_table.select.return_value.execute.return_value = fake_response

    mock_client = mocker.Mock()
    mock_client.table.return_value = mock_table

    db = Database(client=mock_client)
    result = db.getWorkerList()
    assert isinstance(result["data"], list)
    assert len(result["data"]) == 2


def test_handle_object_like_response(mocker):
    """
    Simula que .execute() devuelve un objeto (no dict) con attributes status_code/data,
    que es soportado por _handle_response.
    """
    class FakeResp:
        def __init__(self):
            self.status_code = 200
            self.data = [{"id": 9, "name": "Obj"}]
            self.error = None

    fake_response = FakeResp()
    mock_table = mocker.Mock()
    mock_table.select.return_value.execute.return_value = fake_response

    mock_client = mocker.Mock()
    mock_client.table.return_value = mock_table

    db = Database(client=mock_client)
    result = db.getWorkerList()
    assert result["status_code"] == 200
    assert result["data"][0]["name"] == "Obj"
