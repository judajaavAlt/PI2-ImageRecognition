import pytest
from unittest.mock import patch, MagicMock
from services.workerManager import WorkerManager


# ---------------------------------------------------------
# Helper to build fake database response objects
# ---------------------------------------------------------
class FakeResponse:
    def __init__(self, data):
        self.data = data


# =========================================================
# CREATE
# =========================================================
@patch("services.workerManager.Database")
def test_create_worker(mock_db):

    mock_db.create_worker.return_value = FakeResponse([
        {"id": 1, "name": "Alex", "document": "123", "role": 2, "photo": "img.jpg"}
    ])

    worker = WorkerManager.create("Alex", "123", 2, "img.jpg")

    assert worker["id"] == 1
    mock_db.create_worker.assert_called_once()


# =========================================================
# READ ALL
# =========================================================
@patch("services.workerManager.Database")
def test_read_all_workers(mock_db):

    mock_db.get_worker_list.return_value = FakeResponse([
        {"id": 1, "name": "Alex"},
        {"id": 2, "name": "Maria"}
    ])

    workers = WorkerManager.read_all()

    assert len(workers) == 2
    mock_db.get_worker_list.assert_called_once()


# =========================================================
# READ BY ID
# =========================================================
@patch("services.workerManager.Database")
def test_read_by_id(mock_db):

    mock_db.get_worker.return_value = FakeResponse([
        {"id": 5, "name": "Mario"}
    ])

    worker = WorkerManager.read_by_id(5)

    assert worker["id"] == 5
    mock_db.get_worker.assert_called_once_with(5)


# =========================================================
# UPDATE
# =========================================================
@patch("services.workerManager.Database")
def test_update_worker(mock_db):

    # Initial list
    mock_db.get_worker_list.return_value = FakeResponse([
        {"id": 1, "name": "Alex", "document": "123", "role": 1, "photo": "a.jpg"},
        {"id": 2, "name": "Maria", "document": "456", "role": 2, "photo": "b.jpg"},
    ])

    mock_db.update_worker.return_value = None

    old_worker = WorkerManager.update(1, name="ALEX-UPDATED")

    assert old_worker["name"] == "Alex"
    mock_db.update_worker.assert_called_once_with(
        1,
        {"id": 1, "name": "ALEX-UPDATED", "document": "123", "role": 1, "photo": "a.jpg"}
    )


# =========================================================
# UPDATE NOT FOUND
# =========================================================
@patch("services.workerManager.Database")
def test_update_worker_not_found(mock_db):

    mock_db.get_worker_list.return_value = FakeResponse([])

    result = WorkerManager.update(99, name="New")

    assert result["id"] == -1  # sentinel value


# =========================================================
# DELETE
# =========================================================
@patch("services.workerManager.Database")
def test_delete_worker(mock_db):

    mock_db.delete_worker.return_value = FakeResponse([
        {"id": 1, "name": "Alex"}
    ])

    worker = WorkerManager.delete(1)

    assert worker["id"] == 1
    mock_db.delete_worker.assert_called_once_with(1)


# =========================================================
# DELETE NOT FOUND
# =========================================================
@patch("services.workerManager.Database")
def test_delete_worker_not_found(mock_db):

    mock_db.delete_worker.return_value = FakeResponse([])

    worker = WorkerManager.delete(7)

    assert worker["id"] == 7
    assert worker["name"] == "Null"
