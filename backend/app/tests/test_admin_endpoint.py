import pytest
from fastapi.testclient import TestClient

# importa la app desde tu módulo principal
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    """
    Fixture que mantiene las variables de entorno
    del admin durante las pruebas.
    Se aplica automáticamente a cada test.
    """
    monkeypatch.setenv("ADMIN_USER", "admin_user_test")
    monkeypatch.setenv("ADMIN_PASSWORD", "admin_pass_test")


def test_validate_credentials_success():
    payload = {"username": "admin_user_test", "password": "admin_pass_test"}
    response = client.post("/admin/validate-credentials", json=payload)
    assert response.status_code == 200
    # El endpoint retorna un booleano en el body (True)
    assert response.json() is True


def test_validate_credentials_wrong_user():
    payload = {"username": "wrong_user", "password": "admin_pass_test"}
    response = client.post("/admin/validate-credentials", json=payload)
    assert response.status_code == 200
    assert response.json() is False


def test_validate_credentials_wrong_password():
    payload = {"username": "admin_user_test", "password": "wrong_pass"}
    response = client.post("/admin/validate-credentials", json=payload)
    assert response.status_code == 200
    assert response.json() is False


def test_validate_credentials_missing_field():
    # Si falta un campo, FastAPI responde 422 (validación pydantic)
    payload = {"username": "admin_user_test"}
    response = client.post("/admin/validate-credentials", json=payload)
    assert response.status_code == 422
