import pytest
from unittest.mock import MagicMock, patch
from app.db.database import Database


@pytest.fixture
def mock_client():
    """Mock supabase client injected into the Database class."""
    fake_client = MagicMock()
    Database.client = fake_client
    return fake_client


# ======================
#      WORKERS
# ======================

def test_create_worker(mock_client):
    payload = {"name": "Juan"}

    mock_table = mock_client.table.return_value
    Database.create_worker(payload)

    mock_client.table.assert_called_once_with("Worker")
    mock_table.insert.assert_called_once_with(payload)
    mock_table.insert.return_value.execute.assert_called_once()


def test_update_worker(mock_client):
    mock_table = mock_client.table.return_value
    worker_id = 123
    payload = {"name": "Nuevo"}

    Database.update_worker(worker_id, payload)

    mock_client.table.assert_called_once_with("Worker")
    mock_table.update.assert_called_once_with(payload)
    mock_table.update.return_value.eq.assert_called_once_with("id", worker_id)
    mock_table.update.return_value.eq.return_value.execute.assert_called_once()


def test_delete_worker(mock_client):
    mock_table = mock_client.table.return_value
    worker_id = 55

    Database.delete_worker(worker_id)

    mock_client.table.assert_called_once_with("Worker")
    mock_table.delete.assert_called_once()
    mock_table.delete.return_value.eq.assert_called_once_with("id", worker_id)
    mock_table.delete.return_value.eq.return_value.execute.assert_called_once()


def test_get_worker(mock_client):
    mock_table = mock_client.table.return_value
    worker_id = 10

    Database.get_worker(worker_id)

    mock_client.table.assert_called_once_with("Worker")
    mock_table.select.assert_called_once_with("*")
    mock_table.select.return_value.eq.assert_called_once_with("id", worker_id)
    mock_table.select.return_value.eq.return_value.execute.assert_called_once()


def test_get_worker_list(mock_client):
    mock_table = mock_client.table.return_value

    Database.get_worker_list()

    mock_client.table.assert_called_once_with("Worker")
    mock_table.select.assert_called_once_with("*")
    mock_table.select.return_value.execute.assert_called_once()


def test_get_workers_by_document(mock_client):
    mock_table = mock_client.table.return_value
    document = "ABC123"

    Database.get_workers_by_document(document)

    mock_client.table.assert_called_once_with("Worker")
    mock_table.select.assert_called_once_with("*")
    mock_table.select.return_value.eq.assert_called_once_with("document", document)
    mock_table.select.return_value.eq.return_value.execute.assert_called_once()


# ======================
#        ROLES
# ======================

def test_create_role(mock_client):
    payload = {"name": "Admin"}

    mock_table = mock_client.table.return_value
    Database.create_role(payload)

    mock_client.table.assert_called_once_with("Role")
    mock_table.insert.assert_called_once_with(payload)
    mock_table.insert.return_value.execute.assert_called_once()


def test_get_role_list(mock_client):
    mock_table = mock_client.table.return_value

    Database.get_role_list()

    mock_client.table.assert_called_once_with("Role")
    mock_table.select.assert_called_once_with("*")
    mock_table.select.return_value.execute.assert_called_once()


def test_get_role(mock_client):
    mock_table = mock_client.table.return_value
    role_id = 8

    Database.get_role(role_id)

    mock_client.table.assert_called_once_with("Role")
    mock_table.select.assert_called_once_with("*")
    mock_table.select.return_value.eq.assert_called_once_with("id", role_id)
    mock_table.select.return_value.eq.return_value.execute.assert_called_once()


def test_delete_role(mock_client):
    mock_table = mock_client.table.return_value
    role_id = 40

    Database.delete_role(role_id)

    mock_client.table.assert_called_once_with("Role")
    mock_table.delete.assert_called_once()
    mock_table.delete.return_value.eq.assert_called_once_with("id", role_id)
    mock_table.delete.return_value.eq.return_value.execute.assert_called_once()


def test_update_role(mock_client):
    mock_table = mock_client.table.return_value
    role_id = 22
    payload = {"name": "Editor"}

    Database.update_role(role_id, payload)

    mock_client.table.assert_called_once_with("Role")
    mock_table.update.assert_called_once_with(payload)
    mock_table.update.return_value.eq.assert_called_once_with("id", role_id)
    mock_table.update.return_value.eq.return_value.execute.assert_called_once()
