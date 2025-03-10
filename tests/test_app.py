import pytest
import sqlite3
from app.app import app, init_db, DB_PATH

@pytest.fixture
def client():
    """ Configura un cliente de pruebas para Flask y reinicia la base de datos antes de cada prueba. """
    app.testing = True
    client = app.test_client()
    
    # Reiniciar la base de datos antes de cada prueba
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees")
        conn.commit()
    
    return client

def test_create_employee_success(client):
    """ Prueba la creación de un empleado exitosamente. """
    response = client.post("/employees", json={
        "name": "Daniel",
        "position": "Backend Engineer",
        "salary": 1200
    })
    data = response.get_json()
    assert response.status_code == 201
    assert "id" in data

def test_create_employee_invalid_data(client):
    """ Prueba la creación de un empleado con datos inválidos. """
    response = client.post("/employees", json={
        "name": "",
        "position": "Backend Engineer",
        "salary": "invalid"
    })
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_list_employees(client):
    """ Prueba la obtención de la lista de empleados. """
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_employee_not_found(client):
    """ Prueba obtener un empleado que no existe. """
    response = client.get("/employees/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Employee not found"

def test_update_employee_not_found(client):
    """ Prueba actualizar un empleado que no existe. """
    response = client.put("/employees/999", json={
        "name": "Updated Name",
        "position": "Updated Position",
        "salary": 2000
    })
    assert response.status_code == 404
    assert response.get_json()["error"] == "Employee not found"

def test_delete_employee_not_found(client):
    """ Prueba eliminar un empleado que no existe. """
    response = client.delete("/employees/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Employee not found"

def test_full_employee_lifecycle(client):
    """ Prueba el ciclo completo de un empleado (crear, leer, actualizar, eliminar). """
    # Crear empleado
    response = client.post("/employees", json={
        "name": "Test User",
        "position": "Developer",
        "salary": 1500
    })
    assert response.status_code == 201
    employee_id = response.get_json()["id"]
    
    # Obtener empleado
    response = client.get(f"/employees/{employee_id}")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Test User"
    
    # Actualizar empleado
    response = client.put(f"/employees/{employee_id}", json={
        "name": "Updated User",
        "position": "Senior Developer",
        "salary": 2000
    })
    assert response.status_code == 200
    
    # Obtener empleado actualizado
    response = client.get(f"/employees/{employee_id}")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Updated User"
    
    # Eliminar empleado
    response = client.delete(f"/employees/{employee_id}")
    assert response.status_code == 200
    
    # Verificar que ya no existe
    response = client.get(f"/employees/{employee_id}")
    assert response.status_code == 404
